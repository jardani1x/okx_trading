import os
import json
import time
import hmac
import hashlib
import base64
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OKX_API_KEY")
API_SECRET = os.getenv("OKX_API_SECRET")
PASSPHRASE = os.getenv("OKX_PASSPHRASE")
FLAG = "0"  # 0: demo trading, 1: live trading

BASE_URL = "https://www.okx.com"

def sign(message, secret):
    mac = hmac.new(secret.encode(), message.encode(), hashlib.sha256)
    return base64.b64encode(mac.digest()).decode()

def get_timestamp():
    return str(int(time.time() * 1000))

def build_headers(method, endpoint, body=""):
    timestamp = get_timestamp()
    message = timestamp + method + endpoint + body
    signature = sign(message, API_SECRET)
    
    return {
        "OK-ACCESS-KEY": API_KEY,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

def request_api(method, endpoint, data=None):
    url = BASE_URL + endpoint
    body = json.dumps(data) if data else ""
    headers = build_headers(method, endpoint, body)
    
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=body)
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    return response.json()

def get_balance():
    endpoint = "/api/v5/account/balance"
    return request_api("GET", endpoint)

def place_order(instId, side, ordType, sz, px=None):
    endpoint = "/api/v5/trade/order"
    data = {
        "instId": instId,
        "tdMode": "cash",
        "side": side,
        "ordType": ordType,
        "sz": str(sz)
    }
    if px:
        data["px"] = str(px)
    return request_api("POST", endpoint, data)

def get_ticker(instId):
    endpoint = f"/api/v5/market/ticker?instId={instId}"
    return request_api("GET", endpoint)

def buy_market(instId, size):
    return place_order(instId, "buy", "market", size)

def sell_market(instId, size):
    return place_order(instId, "sell", "market", size)

def buy_limit(instId, size, price):
    return place_order(instId, "buy", "limit", size, price)

def sell_limit(instId, size, price):
    return place_order(instId, "sell", "limit", size, price)

if __name__ == "__main__":
    if not all([API_KEY, API_SECRET, PASSPHRASE]):
        print("❌ Missing API credentials. Check .env file.")
        exit(1)
    
    print("✅ OKX Trading Bot Ready")
    print(f"📊 API Key: {API_KEY[:10]}...")
    
    # Example: Get BTC/USDT balance
    # balance = get_balance()
    # print(balance)
    
    # Example: Buy 10 USDT of BTC
    # order = buy_market("BTC-USDT", "10")
    # print(order)
