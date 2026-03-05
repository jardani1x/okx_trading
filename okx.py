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

# Demo/Testnet vs Live
USE_DEMO = os.getenv("OKX_DEMO", "true").lower() == "true"

if USE_DEMO:
    BASE_URL = "https://www.okx.com"
    # Demo trading endpoints
    DEMO_URL = "https://www.okx.com"
else:
    BASE_URL = "https://www.okx.com"
    DEMO_URL = BASE_URL

class OKXClient:
    def __init__(self, demo: bool = None):
        # Override with parameter if provided
        if demo is not None:
            self.use_demo = demo
        else:
            self.use_demo = USE_DEMO
        
        self.api_key = os.getenv("OKX_API_KEY", "")
        self.secret_key = os.getenv("OKX_SECRET_KEY", "")
        self.passphrase = os.getenv("OKX_PASSPHRASE", "")
        
        # Demo accounts have different API
        if self.use_demo:
            print("🔶 Using DEMO/TESTNET mode")
        else:
            print("🔴 Using LIVE trading mode")
    
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
        
        # Demo mode uses different URL
        if self.use_demo:
            # For demo, we'll use the demo-sso endpoint
            url = f"https://demo-sso.okx.com{endpoint}" if self.use_demo else BASE_URL + endpoint
        else:
            url = BASE_URL + endpoint
        
        # Try demo endpoint first if enabled
        if self.use_demo:
            # Demo trading API
            url = f"https://www.okx.com{endpoint}"
            headers["x-simulated-trading"] = "1"  # Demo trading header
        
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
    
    # Check for demo flag
    demo = True
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    
    if '--live' in flags:
        demo = False
    
    client = OKXClient(demo=demo)
    
    if len(args) < 1:
        print("Usage: python okx.py <command> [args]")
        print("")
        print("Commands: balance, buy, sell, ticker")
        print("")
        print("Examples:")
        print("  python okx.py balance              # Check balance (demo)")
        print("  python okx.py buy BTC-USDT 0.01   # Buy BTC (demo)")
        print("  python okx.py sell ETH-USDT 0.1   # Sell ETH (demo)")
        print("  python okx.py ticker BTC-USDT     # Get BTC price")
        print("")
        print("  python okx.py --live buy BTC-USDT 0.01  # LIVE trading")
        sys.exit(1)
    
    cmd = args[0].lower()
    
    if cmd == "balance":
        result = client.get_balance()
        print(result)
    
    elif cmd == "buy":
        symbol = args[1] if len(args) > 1 else "BTC-USDT"
        amount = float(args[2]) if len(args) > 2 else 0.01
        result = client.buy(symbol, amount)
        print(result)
    
    elif cmd == "sell":
        symbol = args[1] if len(args) > 1 else "BTC-USDT"
        amount = float(args[2]) if len(args) > 2 else 0.01
        result = client.sell(symbol, amount)
        print(result)
    
    elif cmd == "ticker":
        symbol = args[1] if len(args) > 1 else "BTC-USDT"
        result = client.get_ticker(symbol)
        print(result)
    
    else:
        print(f"Unknown command: {cmd}")
