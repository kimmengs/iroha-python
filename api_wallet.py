from fastapi import FastAPI
from pydantic import BaseModel
from utils.workaround_cli import create_wallet_with_kagami, register_account_and_asset
import subprocess
import json
import shutil

app = FastAPI()


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