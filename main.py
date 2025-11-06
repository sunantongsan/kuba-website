from fastapi import FastAPI
from pytonutils import Client, WalletV4R2
import sqlite3

app = FastAPI()
client = Client('https://toncenter.com/api/v2/jsonRPC')
TEAM_WALLET = 'UQAfUj__LHqowEqTCKk2xaTFG8L2t_Pv46BiezvgeBnyRVTa'
wallet = WalletV4R2(client, mnemonic='YOUR_MNEMONIC')  # แทนที่ด้วย mnemonic ของทีม (24 คำ)

@app.post('/submit-swap')
async def submit_swap(user_address: str, ton_amount: float, kuba_amount: float):
    try:
        # ตรวจสอบว่าได้ TON เข้ากระเป๋าทีมงาน (สมมติตรวจจาก TONScan หรือ API)
        # กรณีนี้ใช้การตรวจสอบง่าย ๆ (ควรใช้ API TON เพื่อความแม่นยำ)
        conn = sqlite3.connect('transactions.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS swaps (tx_id TEXT, user_address TEXT, ton_amount REAL, kuba_amount REAL, status TEXT)')
        c.execute('INSERT INTO swaps (tx_id, user_address, ton_amount, kuba_amount, status) VALUES (?, ?, ?, ?, ?)',
                  ('manual_' + str(hash(user_address + str(ton_amount))), user_address, ton_amount, kuba_amount, 'pending'))
        conn.commit()
        conn.close()

        # โอน KUBA (สมมติว่าตรวจสอบ TON เสร็จแล้ว)
        await wallet.transfer(user_address, int(kuba_amount), 'EQDCCMpdq2lab20fVNcXTx44TrGfAnNDvWiFWt9wDfDUY5YT')
        return {'status': 'success', 'message': 'Swap processed'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
