# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python terminal application that queries real-time global exchange rates and provides intelligent currency conversion analysis. The application helps users find the most cost-effective currency conversion paths by:

1. Fetching real-time exchange rates from multiple sources
2. Calculating CNY (Chinese Yuan) to intermediate currency conversions
3. Ranking intermediate currencies to USD conversions
4. Presenting optimized currency exchange recommendations

## Architecture

- `main.py` - Entry point and terminal interface
- `exchange_rate_api.py` - Real-time exchange rate data fetching with bulk processing
- `currency_analyzer.py` - Core logic for conversion path analysis with performance optimizations
- `config.py` - Configuration and API settings
- `utils.py` - Utility functions for formatting and calculations
- `performance_monitor.py` - Performance monitoring and analysis tools
- `benchmark.py` - Performance benchmarking script

## Common Commands

### Project Setup with UV (Recommended)
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# or: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Initialize project and install dependencies
uv sync

# Run the application (interactive mode with currency selection)
uv run main.py
# or use the short alias: uv run era

# Run with all available currencies from API
uv run main.py --all-currencies

# Run with popular currencies only
uv run main.py --popular
# or: uv run era --popular

# Run with specific currency targets
uv run main.py --currencies EUR,GBP,JPY,KRW

# Run with specific amount
uv run main.py --amount 50000

# Run in debug mode
uv run main.py --debug

# Force offline demo mode
uv run main.py --offline

# Performance benchmarking
uv run benchmark.py
# or: uv run era-benchmark

# API connection testing
uv run test_api.py
# or: uv run era-test
```

### Legacy pip Setup (Alternative)
```bash
# Install dependencies with pip
pip install -r requirements.txt

# Run with python directly
python main.py
python benchmark.py
python test_api.py
```

### Troubleshooting

If you encounter "找到 0 种可用货币" error:

1. **Test API connection**:
   ```bash
   python test_api.py
   ```

2. **Check network connectivity** - The app needs internet access to fetch rates

3. **Try with API key** - Set `EXCHANGE_API_KEY` in `.env` file for paid API access

4. **Use fallback modes**:
   ```bash
   # Use popular currencies (doesn't require API currency list)
   python main.py --popular
   
   # Use specific currencies
   python main.py --currencies "EUR,GBP,JPY,KRW"
   
   # Force offline demo mode (no network required)
   python main.py --offline
   ```

### Network Issues & SSL Errors

If you encounter SSL/network connection errors:

1. **Try offline demo mode**:
   ```bash
   python main.py --offline
   ```

2. **Test network connectivity**:
   ```bash
   python network_fix.py
   ```

3. **Use alternative network settings**:
   ```bash
   # Install additional certificates
   pip install --upgrade certifi urllib3
   
   # Test with network fixes
   python -c "from network_fix import apply_network_fixes; apply_network_fixes()"
   ```

### Dependencies
- `requests` - API calls to exchange rate services
- `rich` - Terminal UI formatting and tables
- `click` - Command line interface
- `python-dotenv` - Environment variable management

## Key Features

- **Comprehensive Currency Coverage**: Analyzes 100+ global currencies automatically fetched from API
- **Real-time Exchange Rate Fetching**: Multiple API sources with automatic fallback
- **Intelligent Currency Filtering**: Validates and filters currencies based on API availability
- **Multi-tier Currency Lists**: All currencies, popular currencies, default set, or custom selection
- **Advanced Analysis Statistics**: Shows positive yield paths, efficiency ranges, and comprehensive rankings
- **Optimized Display**: Smart table pagination for large result sets (50+ currencies)
- **Interactive Terminal UI**: Rich formatting with color-coded efficiency scores
- **High-Performance Processing**: Bulk rate fetching, threading, and intelligent caching
- **Performance Monitoring**: Built-in benchmarking and performance analysis tools
- **Scalable Architecture**: Automatically switches between sequential and bulk processing based on currency count
- **Offline Demo Mode**: Works without internet connection using simulated exchange rate data
- **Robust Network Handling**: Multiple API fallbacks, SSL error recovery, and connection retry logic

## Configuration

Environment variables can be set in `.env` file:
- `EXCHANGE_API_KEY` - API key for premium rate services
- `DEFAULT_CURRENCIES` - Comma-separated list of currencies to analyze
- `CACHE_DURATION` - Rate cache duration in minutes