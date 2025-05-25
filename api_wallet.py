from fastapi import FastAPI
from fastapi import Query
from pydantic import BaseModel
from utils.workaround_cli import create_wallet_with_kagami, get_asset_balance, register_account_and_asset, list_assets_with_account
import subprocess
import json
import shutil

app = FastAPI()

class AssetIdWithBalance(BaseModel):
    asset_id: str
    balance: int
class BalanceResponse(BaseModel):
    account_id: str
    asset_id: str
    balance: str
class WalletResponse(BaseModel):
    account_id: str
    public_key: str
    private_key: str
    asset_ids: list[AssetIdWithBalance]
        
class AssetsByAccountResponse(BaseModel):
    account_id: str
    assets: list

@app.post("/wallet", response_model=WalletResponse)
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
    
@app.get("/balance", response_model=BalanceResponse)
def get_balance(
    public_key: str = Query(..., description="The public key of the account"),
    asset_id: str = Query(..., description="The asset id (e.g. usd#hivefund)"),
    private_key: str = Query(..., description="The private key of the account")
):
    # Compose account_id from public_key and domain (assuming domain is always hivefund)
    account_id = f"{asset_id}##{public_key}@hivefund"
    balance = get_asset_balance(account_id, "hivefund", public_key, private_key)

    return BalanceResponse(
        account_id=account_id,
        asset_id=asset_id,
        balance=balance
    )
    
@app.get("/assets-by-account", response_model=AssetsByAccountResponse)
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