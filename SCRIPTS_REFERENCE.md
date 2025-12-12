# DS Trading Bot - Scripts Reference Guide

## Overview

The DS Trading Bot project contains four main Python scripts that represent different versions and capabilities of the trading system. Each script builds upon the previous one, adding more sophisticated features and capabilities.

## Script Comparison Matrix

| Feature | deepseek.py | deepseek_ok版本.py | deepseek_ok_带指标plus版本.py | deepseek_ok_带市场情绪+指标版本.py |
|---------|-------------|-------------------|------------------------------|-----------------------------------|
| Exchange | Binance | OKX | OKX | OKX |
| Technical Indicators | Basic (SMA) | Basic (SMA) | Comprehensive (RSI, MACD, BB, etc.) | Comprehensive (RSI, MACD, BB, etc.) |
| Market Sentiment | No | No | No | Yes |
| Intelligent Position Sizing | No | No | Yes | Yes |
| Advanced Risk Management | Basic | Basic | Advanced | Advanced |
| Position Adjustment | Fixed | Fixed | Dynamic (add/reduce) | Dynamic (add/reduce) |

## Script Details

### 1. deepseek.py (Basic Binance Version)

**Purpose**: The foundational trading bot using Binance exchange API.

**Key Features**:
- Uses Binance exchange for trading
- Basic technical analysis with simple moving averages
- Fixed position sizing
- Standard trading logic with BUY/SELL/HOLD signals
- Basic risk management with stop-loss and take-profit

**Main Functions**:
- `get_btc_ohlcv()`: Fetches K-line data from Binance
- `analyze_with_deepseek()`: Generates signals using DeepSeek
- `execute_trade()`: Executes trades on Binance
- `setup_exchange()`: Configures Binance API connection

**Best For**: Beginners or those wanting to use Binance exchange

### 2. deepseek_ok版本.py (Basic OKX Version)

**Purpose**: The foundational trading bot using OKX exchange API.

**Key Features**:
- Uses OKX exchange for trading
- Basic technical analysis with simple moving averages
- Fixed position sizing
- Standard trading logic with BUY/SELL/HOLD signals
- Basic risk management with stop-loss and take-profit

**Main Functions**:
- `get_btc_ohlcv()`: Fetches K-line data from OKX
- `analyze_with_deepseek()`: Generates signals using DeepSeek
- `execute_trade()`: Executes trades on OKX
- `setup_exchange()`: Configures OKX API connection with cross-margin mode

**Best For**: Users preferring OKX exchange with basic functionality

### 3. deepseek_ok_带指标plus版本.py (Enhanced OKX Version)

**Purpose**: Advanced trading bot with comprehensive technical indicators.

**Key Features**:
- Uses OKX exchange for trading
- Comprehensive technical analysis:
  - Moving Averages (SMA 5, 20, 50)
  - Exponential Moving Averages (EMA 12, 26)
  - MACD with signal line
  - RSI (Relative Strength Index)
  - Bollinger Bands
  - Volume analysis
  - Support and resistance levels
- Intelligent position sizing based on:
  - Signal confidence
  - Market trend strength
  - RSI overbought/oversold conditions
- Dynamic position management (add/reduce positions)
- Advanced risk management

**Main Functions**:
- `calculate_technical_indicators()`: Calculates comprehensive indicators
- `get_market_trend()`: Analyzes multi-timeframe trends
- `get_support_resistance_levels()`: Identifies key price levels
- `calculate_intelligent_position()`: Calculates optimal position size
- `execute_intelligent_trade()`: Executes trades with dynamic sizing
- `get_btc_ohlcv_enhanced()`: Fetches data with indicators
- `generate_technical_analysis_text()`: Formats indicators for AI analysis

**Best For**: Users wanting sophisticated technical analysis with intelligent position sizing

### 4. deepseek_ok_带市场情绪+指标版本.py (Advanced OKX Version with Sentiment)

**Purpose**: Most advanced trading bot with technical indicators and market sentiment.

**Key Features**:
- All features from the enhanced version
- Market sentiment integration using external API
- Sentiment analysis combined with technical analysis
- More sophisticated position management logic
- Additional risk controls for sentiment-based trading
- Trend strength considerations in position sizing

**Additional Functions**:
- `get_sentiment_indicators()`: Fetches market sentiment data
- Enhanced `analyze_with_deepseek()`: Incorporates sentiment data
- Additional position management rules based on sentiment
- Sentiment data validation and error handling

**Best For**: Advanced users wanting the most comprehensive analysis with market sentiment

## Function Descriptions

### Core Functions (Present in all scripts)

#### `setup_exchange()`
- Configures the exchange connection
- Sets leverage and margin mode
- Verifies account balance
- Handles exchange-specific settings

#### `get_current_position()`
- Fetches current position status
- Returns position side (long/short), size, entry price, PnL
- Handles exchange-specific position format

#### `analyze_with_deepseek(price_data)`
- Sends market data to DeepSeek API
- Formats prompt with technical analysis
- Parses AI response for trading signal
- Returns structured signal data

#### `execute_trade(signal_data, price_data)`
- Executes trades based on signals
- Handles position management (enter/exit/reverse)
- Implements exchange-specific order types
- Includes error handling and validation

#### `trading_bot()`
- Main trading loop function
- Coordinates data fetching, analysis, and execution
- Handles timing and scheduling
- Logs trading activities

### Advanced Functions (Enhanced and Advanced versions)

#### `calculate_technical_indicators(df)`
- Calculates multiple technical indicators
- Returns DataFrame with all indicators
- Handles NaN values and edge cases

#### `calculate_intelligent_position(signal_data, price_data, current_position)`
- Calculates optimal position size
- Considers confidence, trend strength, and RSI
- Respects account balance limits
- Returns position size in contracts

#### `get_market_trend(df)`
- Analyzes multi-timeframe trends
- Combines SMA, MACD, and price action
- Returns trend assessment for different timeframes

#### `get_sentiment_indicators()` (Advanced version only)
- Fetches market sentiment from external API
- Handles API authentication and rate limits
- Returns sentiment scores and data quality metrics

## Configuration Differences

### Exchange Settings
- **Binance versions**: Use `ccxt.binance()` with futures options
- **OKX versions**: Use `ccxt.okx()` with swap options and password

### Position Management
- **Basic versions**: Fixed position size from config
- **Enhanced/Advanced**: Dynamic position sizing based on market conditions

### Risk Controls
- **Basic versions**: Simple stop-loss/take-profit
- **Enhanced/Advanced**: Multiple risk factors and position adjustments

## Choosing the Right Script

### For New Users
Start with `deepseek_ok版本.py` (Basic OKX version) to understand the system before moving to more complex versions.

### For Technical Analysis Focus
Use `deepseek_ok_带指标plus版本.py` for comprehensive technical analysis without external dependencies.

### For Maximum Performance
Use `deepseek_ok_带市场情绪+指标版本.py` for the most sophisticated analysis, but be aware that sentiment API may have availability issues.

### For Binance Users
Use `deepseek.py` if you prefer Binance exchange over OKX.

## Migration Path

Users can migrate between versions as follows:
1. Basic → Enhanced: Add technical indicators and intelligent position sizing
2. Enhanced → Advanced: Add market sentiment analysis
3. Binance → OKX: Switch exchange API integration

Each migration adds complexity but potentially improves performance.