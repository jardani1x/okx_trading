# OKX Trading Bot (Python)

Simple Python scripts for OKX trading.

## Setup

```bash
# Install dependencies
pip install requests python-dotenv
```

2. Copy `.env.example` to `.env` and add your API keys

## Usage

```bash
# Check balance
python okx.py balance

# Buy
python okx.py buy BTC-USDT 0.01

# Sell
python okx.py sell ETH-USDT 0.1

# Get price
python okx.py ticker BTC-USDT
```
