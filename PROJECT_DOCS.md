# DS (DeepSeek) Trading Bot - Project Documentation

## Project Overview

The DS Trading Bot is an AI-powered cryptocurrency trading system that uses the DeepSeek language model to analyze market data and execute trades on cryptocurrency exchanges (Binance and OKX). The system is designed to automatically analyze market conditions, generate trading signals, and execute trades based on technical analysis and market sentiment.

## Project Structure

The project consists of 4 main Python scripts that represent different versions/iterations of the trading bot:

1. `deepseek.py` - Basic version using Binance API
2. `deepseek_ok版本.py` - Basic version using OKX API
3. `deepseek_ok_带指标plus版本.py` - Enhanced version with technical indicators using OKX API
4. `deepseek_ok_带市场情绪+指标版本.py` - Advanced version with technical indicators and market sentiment using OKX API

## Core Components

### 1. API Integration
- **DeepSeek API**: Used for market analysis and generating trading signals
- **Exchange APIs**: Binance and/or OKX for market data and trade execution
- **Market Sentiment API**: External API for market sentiment analysis (optional)

### 2. Technical Analysis
- **K-line Analysis**: Historical price data analysis (15m, 1h timeframes)
- **Technical Indicators**: 
  - Moving Averages (SMA, EMA)
  - MACD (Moving Average Convergence Divergence)
  - RSI (Relative Strength Index)
  - Bollinger Bands
  - Support and Resistance levels
- **Volume Analysis**: Volume trends and ratios

### 3. Trading Logic
- **Signal Generation**: BUY, SELL, or HOLD based on DeepSeek analysis
- **Position Management**: Long/short position tracking and management
- **Risk Management**: Stop-loss and take-profit levels
- **Confidence Scoring**: High/Medium/Low confidence in trading signals

### 4. Execution System
- **Order Management**: Market orders for entry/exit
- **Position Sizing**: Dynamic position sizing based on confidence and market conditions
- **Risk Controls**: Leverage management and position limits

## Key Features

### Trading Strategies
1. **Trend Following**: Identifies and follows market trends
2. **Momentum Analysis**: Uses RSI and MACD for momentum signals
3. **Support/Resistance**: Identifies key price levels
4. **Sentiment Integration**: Incorporates market sentiment data (in advanced versions)
5. **Smart Position Sizing**: Adjusts position size based on confidence and risk

### Risk Management
- **Stop-Loss**: Automatic stop-loss based on technical analysis
- **Take-Profit**: Automatic profit-taking based on technical analysis
- **Position Limits**: Maximum position size controls
- **Confidence-Based Execution**: Only executes high-confidence signals

## Configuration

### Environment Variables (.env file)
```
DEEPSEEK_API_KEY=your_deepseek_api_key
BINANCE_API_KEY=your_binance_api_key (for Binance version)
BINANCE_SECRET=your_binance_secret (for Binance version)
OKX_API_KEY=your_okx_api_key (for OKX versions)
OKX_SECRET=your_okx_secret (for OKX versions)
OKX_PASSWORD=your_okx_password (for OKX versions)
```

### Trading Configuration
- **Symbol**: BTC/USDT (default, can be modified)
- **Leverage**: 10x (default, can be modified)
- **Timeframe**: 15m (default, can be modified to 1h)
- **Amount**: Trade amount in BTC (in basic versions)
- **Position Size**: Dynamic calculation (in advanced versions)

## Script Descriptions

### 1. deepseek.py (Binance Basic Version)
- Uses Binance exchange API
- Basic technical analysis with simple moving averages
- Fixed position sizing
- Standard BUY/SELL/HOLD signals

### 2. deepseek_ok版本.py (OKX Basic Version)
- Uses OKX exchange API
- Basic technical analysis
- Fixed position sizing
- Standard trading logic

### 3. deepseek_ok_带指标plus版本.py (OKX Enhanced Version)
- Uses OKX exchange API
- Comprehensive technical indicators (RSI, MACD, Bollinger Bands, etc.)
- Intelligent position sizing based on confidence and market conditions
- Advanced risk management
- Dynamic position adjustment (add/reduce positions)

### 4. deepseek_ok_带市场情绪+指标版本.py (OKX Advanced Version)
- Uses OKX exchange API
- All features from the enhanced version
- Market sentiment integration
- More sophisticated position management
- Trend strength consideration
- RSI-based position adjustment

## Technical Architecture

### Data Flow
1. **Data Collection**: Fetches K-line data from exchange
2. **Technical Analysis**: Calculates indicators and analyzes trends
3. **Sentiment Analysis**: (Advanced versions) Retrieves market sentiment data
4. **AI Analysis**: DeepSeek analyzes data and generates trading signal
5. **Risk Assessment**: Evaluates position and risk parameters
6. **Execution**: Places orders on exchange based on signal

### Key Functions
- `get_btc_ohlcv_enhanced()`: Fetches market data with technical indicators
- `analyze_with_deepseek()`: Generates trading signals using AI
- `execute_trade()`: Executes trades based on signals
- `calculate_intelligent_position()`: Calculates optimal position size
- `get_current_position()`: Retrieves current position status

## Setup Instructions

1. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Create Environment File**:
   Create a `.env` file in the project root with required API keys

3. **Choose Trading Script**:
   Select the appropriate script based on your needs:
   - Basic functionality: `deepseek.py` or `deepseek_ok版本.py`
   - Technical indicators: `deepseek_ok_带指标plus版本.py`
   - Advanced features: `deepseek_ok_带市场情绪+指标版本.py`

4. **Configure Trading Parameters**:
   Modify the `TRADE_CONFIG` dictionary in the chosen script

5. **Run the Bot**:
   ```
   python [chosen_script_name].py
   ```

## Important Notes

- **Risk Warning**: This is a high-risk trading system. Only use with money you can afford to lose.
- **Testing**: Always test in simulation mode first (`test_mode: True`)
- **Monitoring**: Monitor the bot actively during operation
- **API Limits**: Be aware of API rate limits for both DeepSeek and exchange APIs
- **Market Conditions**: Performance may vary significantly based on market conditions

## Maintenance

- Monitor logs for errors and unusual behavior
- Ensure API keys remain valid and have sufficient permissions
- Keep dependencies updated
- Review and adjust trading parameters based on performance
- Monitor account balances and position sizes regularly