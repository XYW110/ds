# DS Trading Bot - Configuration Guide

## Environment Configuration (.env File)

The trading bot uses environment variables to securely store sensitive API keys and configuration parameters. This guide explains all required configuration settings.

### Creating the .env File

Create a file named `.env` in the project root directory with the following format:

```env
# DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Binance API Configuration (for Binance versions)
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_SECRET=your_binance_secret_here

# OKX API Configuration (for OKX versions)
OKX_API_KEY=your_okx_api_key_here
OKX_SECRET=your_okx_secret_here
OKX_PASSWORD=your_okx_password_here
```

## API Key Configuration

### DeepSeek API Key

**Purpose**: Used for AI analysis of market data and generating trading signals.

**How to obtain**:
1. Visit the DeepSeek API website
2. Create an account
3. Navigate to API keys section
4. Generate a new API key
5. Copy the key and add to your `.env` file

**Required permission**: Must have access to the `deepseek-chat` model

**Security considerations**:
- Never share your API key publicly
- Do not commit the `.env` file to version control
- Monitor API usage to control costs
- Regenerate the key if compromised

### Binance API Configuration

**Purpose**: Used for trading on Binance exchange (in `deepseek.py` version).

#### BINANCE_API_KEY
- **Purpose**: Your Binance API key identifier
- **How to obtain**:
  1. Log into your Binance account
  2. Go to Settings > API Management
  3. Create a new API key
  4. Enable "Enable Spot & Margin Trading"
  5. Copy the API key string

#### BINANCE_SECRET
- **Purpose**: Your Binance API secret key for authentication
- **How to obtain**: Generated alongside the API key
- **Security**: Keep this secret and secure

**Required permissions**:
- Enable Spot & Margin Trading
- Enable Futures Trading (if using futures)
- IP restrictions (optional but recommended)

### OKX API Configuration

**Purpose**: Used for trading on OKX exchange (in all OKX versions).

#### OKX_API_KEY
- **Purpose**: Your OKX API key identifier
- **How to obtain**:
  1. Log into your OKX account
  2. Go to Assets > API
  3. Create a new API key
  4. Select appropriate permissions
  5. Copy the API key string

#### OKX_SECRET
- **Purpose**: Your OKX API secret key for authentication
- **How to obtain**: Generated alongside the API key
- **Security**: Keep this secret and secure

#### OKX_PASSWORD
- **Purpose**: Your OKX API passphrase (not your account password)
- **How to obtain**: Set during API key creation process
- **Note**: This is a separate password created specifically for API access

**Required permissions**:
- Enable Trading (Spot, Futures, or both)
- Enable Transfer (if needed)
- IP restrictions (optional but recommended)

## Trading Configuration Parameters

In addition to the `.env` file, each script contains a `TRADE_CONFIG` dictionary that can be modified directly in the Python file:

### Basic Trading Parameters

```python
TRADE_CONFIG = {
    'symbol': 'BTC/USDT:USDT',  # Trading pair to trade
    'leverage': 10,             # Leverage amount (1-100 depending on exchange)
    'timeframe': '15m',         # Candlestick timeframe (15m, 1h, etc.)
    'test_mode': False,         # Set to True to simulate trades without executing
    'amount': 0.01,             # Fixed amount to trade (in BTC, varies by script)
}
```

#### Symbol Configuration
- **Format**: Different for each exchange
  - Binance: `'BTC/USDT'` (spot) or `'BTC/USDT'` with futures options
  - OKX: `'BTC/USDT:USDT'` (perpetual swap)
- **Note**: Verify the correct symbol format for your exchange

#### Leverage Configuration
- **Range**: Varies by exchange (typically 1x to 125x)
- **Risk**: Higher leverage increases both potential profits and losses
- **Recommendation**: Start with lower leverage (5x-10x) for testing

#### Timeframe Configuration
- **Options**: 
  - `'1m'`, `'5m'`, `'15m'`, `'30m'` (short-term)
  - `'1h'`, `'2h'`, `'4h'` (medium-term)
  - `'1d'` (long-term)
- **Recommendation**: `'15m'` for most strategies

#### Test Mode
- **True**: Simulates trades without executing real orders
- **False**: Executes real trades on the exchange
- **Recommendation**: Always test with `True` first

### Advanced Trading Parameters (Enhanced/Advanced versions)

```python
TRADE_CONFIG = {
    # Basic parameters as above plus:
    'data_points': 96,  # Number of historical data points to fetch
    'analysis_periods': {  # Periods for different MA calculations
        'short_term': 20,
        'medium_term': 50,
        'long_term': 96
    },
    'position_management': {  # Intelligent position sizing
        'enable_intelligent_position': True,
        'base_usdt_amount': 100,  # Base USDT amount for position calculation
        'high_confidence_multiplier': 1.5,
        'medium_confidence_multiplier': 1.0,
        'low_confidence_multiplier': 0.5,
        'max_position_ratio': 10,  # Max percentage of balance to use
        'trend_strength_multiplier': 1.2
    }
}
```

## Configuration Best Practices

### Security Best Practices
1. **Never commit .env files**: Add `.env` to your `.gitignore` file
2. **Use strong API keys**: Generate unique, strong API keys
3. **Limit API permissions**: Only enable necessary trading permissions
4. **IP restrictions**: Restrict API access to specific IP addresses when possible
5. **Regular rotation**: Periodically regenerate API keys

### Trading Configuration Best Practices
1. **Start small**: Begin with small position sizes and low leverage
2. **Test thoroughly**: Use `test_mode: True` extensively before live trading
3. **Monitor usage**: Keep track of API rate limits and usage costs
4. **Backup configuration**: Keep a backup of working configurations
5. **Document changes**: Keep track of configuration changes and their results

### Exchange-Specific Notes

#### Binance Configuration
- Ensure futures wallet has sufficient balance
- Check if futures trading is enabled on your account
- Be aware of Binance's API rate limits

#### OKX Configuration
- Verify account has cross-margin mode enabled
- Check if perpetual swaps are enabled
- Note that OKX requires a passphrase in addition to API key/secret

## Troubleshooting Configuration Issues

### Common API Key Issues
1. **"Invalid API key"**: Verify the key is copied correctly without extra spaces
2. **"Signature not valid"**: Check that the secret key matches the API key
3. **"Permission denied"**: Verify API key permissions are correctly set
4. **"IP not allowed"**: Check if IP restrictions are enabled

### Common Trading Configuration Issues
1. **"Insufficient balance"**: Verify account has sufficient funds
2. **"Invalid symbol"**: Check symbol format for your exchange
3. **"Leverage not allowed"**: Verify leverage settings are within exchange limits
4. **"Rate limit exceeded"**: Check API usage and implement delays if needed

### Testing Configuration
1. Start with `test_mode: True`
2. Verify all API keys work by making simple API calls
3. Test with small position sizes initially
4. Monitor logs for any configuration-related errors