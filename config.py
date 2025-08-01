import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
EXCHANGE_API_KEY = os.getenv('EXCHANGE_API_KEY', '')

# API URLs (multiple sources for reliability)
API_URLS = {
    'paid': 'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}',
    'free_v4': 'https://api.exchangerate-api.com/v4/latest/{base}',
    'alternative': 'https://api.exchangerate.host/latest?base={base}'
}

# Comprehensive list of major currencies supported by most exchange rate APIs
DEFAULT_CURRENCIES = [
    # Major currencies
    'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD',
    # Asian currencies
    'KRW', 'HKD', 'SGD', 'TWD', 'THB', 'MYR', 'IDR', 'PHP', 'VND', 'INR', 'PKR', 'BDT', 'LKR',
    # Middle Eastern currencies
    'AED', 'SAR', 'QAR', 'KWD', 'BHD', 'OMR', 'JOD', 'ILS', 'TRY', 'IRR',
    # European currencies
    'NOK', 'SEK', 'DKK', 'ISK', 'PLN', 'CZK', 'HUF', 'RON', 'BGN', 'HRK', 'RSD', 'MKD', 'ALL',
    'BAM', 'MDL', 'UAH', 'BYN', 'RUB', 'GEL', 'AMD', 'AZN', 'KZT', 'KGS', 'TJS', 'TMT', 'UZS',
    # African currencies
    'ZAR', 'NGN', 'EGP', 'KES', 'UGX', 'TZS', 'GHS', 'ETB', 'XOF', 'XAF', 'MAD', 'TND', 'DZD',
    'LYD', 'SDG', 'SSP', 'ERN', 'DJF', 'SOS', 'RWF', 'BIF', 'KMF', 'MUR', 'SCR', 'MGA', 'MWK',
    'ZMW', 'BWP', 'SZL', 'LSL', 'NAD', 'AOA', 'MZN', 'ZWL',
    # American currencies
    'MXN', 'BRL', 'ARS', 'CLP', 'COP', 'PEN', 'UYU', 'PYG', 'BOB', 'VES', 'GYD', 'SRD', 'FKP',
    'GTQ', 'BZD', 'HNL', 'NIO', 'CRC', 'PAB', 'CUP', 'DOP', 'HTG', 'JMD', 'KYD', 'XCD', 'BBD',
    'TTD', 'AWG', 'ANG', 'SVC', 'BMD', 'BSD',
    # Pacific currencies
    'FJD', 'PGK', 'SBD', 'TOP', 'VUV', 'WST', 'XPF',
    # Others
    'AFN', 'BTN', 'BND', 'KHR', 'LAK', 'MMK', 'NPR', 'MNT', 'UZS'
]

# Popular/Common currencies for quick analysis
POPULAR_CURRENCIES = [
    'USD', 'EUR', 'GBP', 'JPY', 'KRW', 'HKD', 'SGD', 'AUD', 'CAD', 'CHF',
    'TWD', 'THB', 'MYR', 'INR', 'AED', 'SAR', 'NOK', 'SEK', 'DKK', 'RUB',
    'ZAR', 'MXN', 'BRL', 'ARS', 'TRY', 'PLN', 'CZK', 'HUF', 'ILS', 'NZD'
]

# Cache settings
CACHE_DURATION_MINUTES = int(os.getenv('CACHE_DURATION', '5'))

# Base currency
BASE_CURRENCY = 'CNY'
TARGET_CURRENCY = 'USD'