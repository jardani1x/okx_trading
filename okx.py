"""
OKX Trading Client
Simple Python buy/sell script for OKX
"""

import os
import hmac
import hashlib
import base64
import time
import requests
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Skip if dotenv not installed

BASE_URL = "https://www.okx.com"

class OKXClient:
    def __init__(self):
        self.api_key = os.getenv("OKX_API_KEY", "")
        self.secret_key = os.getenv("OKX_SECRET_KEY", "")
        self.passphrase = os.getenv("OKX_PASSPHRASE", "")
    
    def sign(self, message: str, timestamp: str) -> str:
        mac = hmac.new(
            self.secret_key.encode(),
            (timestamp + message).encode(),
            hashlib.sha256
        )
        return base64.b64encode(mac.digest()).decode()
    
    def request(self, method: str, endpoint: str, params: dict = None):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + "Z"
        body = params and str(params) or ""
        
        sign = self.sign(method + endpoint + body, timestamp)
        
        headers = {
            "Content-Type": "application/json",
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": sign,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase
        }
        
        url = BASE_URL + endpoint
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            else:
                response = requests.post(url, headers=headers, json=params)
            
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            raise
    
    def get_balance(self):
        return self.request("GET", "/api/v5/account/balance")
    
    def place_order(self, inst_id: str, side: str, sz: float, ord_type: str = "market"):
        params = {
            "instId": inst_id,
            "tdMode": "cash",
            "side": side,
            "ordType": ord_type,
            "sz": str(sz)
        }
        return self.request("POST", "/api/v5/trade/order", params)
    
    def buy(self, inst_id: str, sz: float):
        return self.place_order(inst_id, "buy", sz, "market")
    
    def sell(self, inst_id: str, sz: float):
        return self.place_order(inst_id, "sell", sz, "market")
    
    def get_ticker(self, inst_id: str):
        return self.request("GET", f"/api/v5/market/ticker?instId={inst_id}")


if __name__ == "__main__":
    import sys
    client = OKXClient()
    
    if len(sys.argv) < 2:
        print("Usage: python okx.py <command> [args]")
        print("Commands: balance, buy, sell, ticker")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "balance":
        result = client.get_balance()
        print(result)
    
    elif cmd == "buy":
        symbol = sys.argv[2] if len(sys.argv) > 2 else "BTC-USDT"
        amount = float(sys.argv[3]) if len(sys.argv) > 3 else 0.01
        result = client.buy(symbol, amount)
        print(result)
    
    elif cmd == "sell":
        symbol = sys.argv[2] if len(sys.argv) > 2 else "BTC-USDT"
        amount = float(sys.argv[3]) if len(sys.argv) > 3 else 0.01
        result = client.sell(symbol, amount)
        print(result)
    
    elif cmd == "ticker":
        symbol = sys.argv[2] if len(sys.argv) > 2 else "BTC-USDT"
        result = client.get_ticker(symbol)
        print(result)
    
    else:
        print(f"Unknown command: {cmd}")
