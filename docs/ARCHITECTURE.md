# Architecture

## Project Structure

```
project_root/
├── src/                    # Source code
│   ├── config/            # Configuration management
│   ├── exchanges/          # Exchange adapters
│   ├── analysis/           # AI analysis modules
│   ├── execution/          # Trading execution
│   ├── utils/              # Utility functions
│   └── trading_engine.py  # Main engine
├── docs/                   # Documentation
│   ├── prd/               # Requirements
│   ├── architecture/       # Architecture docs
│   └── epics/             # User stories
├── archive/               # Archived versions
│   ├── v1_basic/
│   ├── v2_okx_basic/
│   ├── v3_technical/
│   └── v4_complete/
├── tests/                  # Test files
├── main.py                 # Main entry point
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
└── README.md              # Project documentation
```

## Modules

- **Config**: Unified configuration management
- **Exchanges**: Multi-exchange support
- **Analysis**: AI and technical analysis
- **Execution**: Trading execution and risk management
- **Utils**: Common utilities and helpers
- **Engine**: Main trading coordination
