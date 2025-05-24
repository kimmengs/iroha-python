from fastapi import FastAPI
from fastapi import Query
from pydantic import BaseModel
from utils.workaround_cli import create_wallet_with_kagami, get_asset_balance, register_account_and_asset
import subprocess
import json
import shutil

app = FastAPI()

class BalanceResponse(BaseModel):
    account_id: str
    asset_id: str
    balance: str
class WalletResponse(BaseModel):
    account_id: str
    public_key: str
    private_key: str
    asset_id: str

@app.post("/wallet", response_model=WalletResponse)
def create_wallet():
    DOMAIN = "hivefund"
    ASSET_NAME = "usd"
    public_key, private_key = create_wallet_with_kagami()
    account_id, asset_id = register_account_and_asset(public_key, DOMAIN, ASSET_NAME)
    return WalletResponse(
        account_id=account_id,
        public_key=public_key,
        private_key=private_key,
        asset_id=asset_id
    )
    
@app.get("/balance", response_model=BalanceResponse)
def get_balance(
    public_key: str = Query(..., description="The public key of the account"),
    asset_id: str = Query(..., description="The asset id (e.g. usd#hivefund)")
):
    # Compose account_id from public_key and domain (assuming domain is always hivefund)
    account_id = f"{asset_id}##{public_key}@hivefund"
    balance = get_asset_balance(account_id, "hivefund", public_key)

    return BalanceResponse(
        account_id=account_id,
        asset_id=asset_id,
        balance=balance
    )