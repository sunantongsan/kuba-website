from fastapi import FastAPI
from tonutils import Client, WalletV4R2
import sqlite3

app = FastAPI()
client = Client('https://toncenter.com/api/v2/jsonRPC')
TEAM_WALLET = 'UQAfUj__LHqowEqTCKk2xaTFG8L2t_Pv46BiezvgeBnyRVTa'

@app.post('/verify-transaction')
async def verify_transaction(tx_id: str, user_address: str, ton_amount: float):
    wallet = WalletV4R2(client, mnemonic='YOUR_MNEMONIC')  # แทนที่ด้วย mnemonic ของทีม
    kuba_amount = ton_amount * 96700 + ton_amount * 9670  # 96,700 KUBA + 10% bonus
    await wallet.transfer(user_address, kuba_amount, 'EQDCCMpdq2lab20fVNcXTx44TrGfAnNDvWiFWt9wDfDUY5YT')
    return {'status': 'success', 'kuba_amount': kuba_amount}