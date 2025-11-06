# DeepSeek Trading Bot

## Project Overview

A unified AI-driven cryptocurrency trading bot that integrates:
- DeepSeek AI market analysis
- Technical indicators analysis
- Market sentiment data
- Multiple exchange support (OKX, Binance)

## Quick Start

1. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. Run the bot:
   ```bash
   python main.py
   ```

## Architecture

```
src/
├── config/          # Configuration management
├── exchanges/       # Exchange adapters
├── analysis/        # AI analysis modules
├── execution/        # Trading execution
├── utils/           # Utility functions
└── trading_engine.py # Main engine
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Change Log](docs/CHANGELOG.md)
