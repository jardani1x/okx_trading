# OKX Trading Bot

Basic Python script for OKX spot trading.

## Setup

```bash
# Clone
git clone https://github.com/jardani1x/okx_trading.git
cd okx_trading

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your OKX API credentials
```

## Get OKX API Keys

1. Go to [OKX](https://www.okx.com/) → Account → API
2. Create API Key with **Trade** permissions
3. Copy keys to `.env`

## Usage

```python
from main import buy_market, sell_market, buy_limit, sell_limit, get_balance, get_ticker

# Check balance
print(get_balance())

# Get BTC price
print(get_ticker("BTC-USDT"))

# Buy 10 USDT of BTC at market price
buy_market("BTC-USDT", "10")

# Sell 0.001 BTC at market price
sell_market("BTC-USDT", "0.001")

# Buy limit order
buy_limit("BTC-USDT", "10", "50000")

# Sell limit order
sell_limit("BTC-USDT", "0.001", "60000")
```

## Disclaimer

⚠️ Trade at your own risk. Always test on demo trading first (FLAG="0").
