# PrimeTrade — Binance Futures (Testnet) CLI

A small, well-structured Python CLI that places MARKET and LIMIT orders on the Binance Futures Testnet (USDT-M). This repository contains a simple client wrapper, order handling, input validation, and logging intended for testing and evaluation against Binance's Testnet.

Key goals:

- Demonstrate secure API usage patterns for testnet trading
- Provide a clear CLI for placing MARKET / LIMIT orders
- Log requests, responses and errors for auditing and debugging

## Features

- Place MARKET and LIMIT orders (BUY / SELL)
- CLI-driven usage via `cli.py`
- Input validation to prevent malformed requests
- Structured logging to `logs/` for requests and errors
- Minimal, dependency-light implementation for easy review

## Requirements

- Python 3.10+
- Install dependencies from `requirements.txt`

Contents of `requirements.txt` in this repo should include the runtime dependencies used (example packages shown):

```
python-binance
python-dotenv
typer
requests
```

## Quickstart (Windows / PowerShell)

1. Clone the repository and enter the project directory:

```powershell
git clone git@github.com:Pritam-25/futures-testnet-trading-bot.git
cd futures-testnet-trading-bot
```

2. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Add your testnet API credentials in a `.env` file at the project root:

```
BINANCE_API_KEY=your_testnet_api_key
BINANCE_SECRET_KEY=your_testnet_secret
```

By default the code targets Binance Futures Testnet. If a BASE_URL override is supported by the client, document it in the code or `.env`.

## Usage

Basic MARKET order example:

```powershell
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Basic LIMIT order example:

```powershell
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000
```

Notes:

- `--symbol` expects the symbol string (e.g. `BTCUSDT`).
- `--side` must be `BUY` or `SELL`.
- `--type` must be `MARKET` or `LIMIT`.
- `--price` is required for `LIMIT` orders.

For a quick connectivity check (if provided):

```powershell
python test_connection.py
```

## Logging

The application writes a single log file to `logs/trading_bot.log`. This file contains:

- API request/response payloads
- Validation errors and user-facing errors
- Network and unexpected exceptions

Inspect or tail `logs/trading_bot.log` when troubleshooting request failures or validation errors.

## Project Layout

Top-level files and folders:

```
.
├── bot/
│   ├── __init__.py
│   ├── client.py         # Binance client wrapper and configuration
│   ├── orders.py         # Order placement logic (MARKET / LIMIT)
│   ├── validators.py     # CLI / input validation
│   └── logging_config.py # Logging configuration
├── logs/                 # Runtime logs
├── cli.py                # CLI entrypoint (uses Typer / argparse)
├── requirements.txt
├── test_connection.py    # Optional: connectivity / smoke test
└── README.md
```

Links:

- CLI entrypoint: [cli.py](cli.py)
- Client wrapper: [bot/client.py](bot/client.py)
- Order logic: [bot/orders.py](bot/orders.py)

## Validation & Error Handling

The CLI enforces required fields and validates basic constraints (positive quantity, limit price required for `LIMIT` orders, allowed sides/types). API and network errors are logged and surfaced to the user with readable messages.

## Development & Testing

- Activate your virtualenv then run the commands above to install dependencies.
- Use `test_connection.py` to verify credentials and connectivity if present.
- Add unit tests as needed — keep them small and isolated from live API calls (use mocking for Binance responses).

## Contact

For questions or submission details, contact: maityp394@gmail.com
