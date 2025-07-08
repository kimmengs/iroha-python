from fastapi import FastAPI
from fastapi import Query
from pydantic import BaseModel
from utils.workaround_cli import create_wallet_with_kagami, get_asset_balance, register_account_and_asset, list_assets_with_account, transfer_asset

from fastapi import Header, HTTPException, Depends
from fastapi import HTTPException

API_KEY = "683dc455-acca-4722-af47-709174f6fce3"  # Change this to your actual API key

def api_key_auth(api_key: str = Header(..., alias="api-key")):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    
app = FastAPI()

class AssetIdWithBalance(BaseModel):
    asset_id: str
    balance: float
class BalanceResponse(BaseModel):
    account_id: str
    asset_id: str
    balance: float
class WalletResponse(BaseModel):
    account_id: str
    public_key: str
    private_key: str
    asset_ids: list[AssetIdWithBalance]
        
class AssetsByAccountResponse(BaseModel):
    account_id: str
    assets: list[AssetIdWithBalance]

class TransferResponse(BaseModel):
    source: str
    destination: str
    object: int
    asset_id: str
    hash: str
class TransferRequest(BaseModel):
    public_key: str
    domain: str = "hivefund"
    private_key: str
    asset_id: str
    to_account_id: str
    quantity: float

@app.post("/wallet", response_model=WalletResponse, dependencies=[Depends(api_key_auth)])
def create_wallet():
    DOMAIN = "hivefund"
    ASSET_NAME = "usd|khr"
    public_key, private_key = create_wallet_with_kagami()
    account_id, asset_ids = register_account_and_asset(public_key, DOMAIN, ASSET_NAME)
    asset_ids_with_balance = [{"asset_id": aid, "balance": 0} for aid in asset_ids]
    return WalletResponse(
        account_id=account_id,
        public_key=public_key,
        private_key=private_key,
        asset_ids=asset_ids_with_balance
    )
    
@app.get("/balance", response_model=BalanceResponse, dependencies=[Depends(api_key_auth)])
def get_balance(
    public_key: str = Query(..., description="The public key of the account"),
    asset_id: str = Query(..., description="The asset id (e.g. usd#hivefund)"),
    private_key: str = Query(..., description="The private key of the account")
):
    account_id = f"{asset_id}##{public_key}@hivefund"
    balance = get_asset_balance(account_id, "hivefund", public_key, private_key)
    try:
        balance_int = float(balance)
    except Exception:
        balance_int = 0

    return BalanceResponse(
        account_id=account_id,
        asset_id=asset_id,
        balance=float(balance_int) 
    )
    
@app.get("/assets-by-account", response_model=AssetsByAccountResponse, dependencies=[Depends(api_key_auth)])
def get_assets_by_account(
    public_key: str = Query(..., description="The public key of the account"),
    domain: str = Query("hivefund", description="The domain of the account"),
    private_key: str = Query(..., description="The private key of the account")
):
    account_id = f"{public_key}@{domain}"
    assets = list_assets_with_account(domain, public_key, private_key)
    return AssetsByAccountResponse(
        account_id=account_id,
        assets=assets
    )


@app.post("/transfer", response_model=TransferResponse, dependencies=[Depends(api_key_auth)])
def transfer_asset_(payload: TransferRequest):
    print("✅ Received payload:")
    print("  public_key:", payload.public_key)
    print("  private_key:", payload.private_key)
    print("  domain:", payload.domain)
    print("  asset_id:", payload.asset_id)
    print("  to_account_id:", payload.to_account_id)
    print("  quantity:", payload.quantity)
    hash_value = transfer_asset(
        payload.domain,
        payload.public_key,
        payload.private_key,
        payload.asset_id,
        payload.to_account_id,
        payload.quantity
    )
    if not hash_value:
        raise HTTPException(status_code=400, detail="Transfer failed or CLI error")
    return TransferResponse(
        source=payload.public_key,
        destination=payload.to_account_id,
        object=payload.quantity,
        asset_id=payload.asset_id,
        hash=hash_value
    )