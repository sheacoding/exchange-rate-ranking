import requests
import time
import ssl
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from typing import Dict, Optional, List
from config import EXCHANGE_API_KEY, API_URLS, CACHE_DURATION_MINUTES

class ExchangeRateAPI:
    def __init__(self):
        self.cache = {}
        self.cache_timestamps = {}
        self.session = self._create_session()
    
    def _create_session(self):
        """Create a requests session with retry logic and SSL configuration"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        # Configure adapter with retry
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set headers
        session.headers.update({
            'User-Agent': 'ExchangeRateRanking/1.0',
            'Accept': 'application/json',
            'Connection': 'close'  # Prevent connection pooling issues
        })
        
        return session
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        self.cache_timestamps.clear()
        print("🔄 缓存已清空")
    
    def _is_cache_valid(self, currency: str) -> bool:
        """Check if cached data is still valid"""
        if currency not in self.cache_timestamps:
            return False
        
        cache_age = time.time() - self.cache_timestamps[currency]
        return cache_age < (CACHE_DURATION_MINUTES * 60)
    
    def get_rates(self, base_currency: str = 'USD') -> Optional[Dict[str, float]]:
        """Fetch exchange rates with caching"""
        if self._is_cache_valid(base_currency):
            return self.cache[base_currency]
        
        rates = self._fetch_rates(base_currency)
        if rates:
            self.cache[base_currency] = rates
            self.cache_timestamps[base_currency] = time.time()
        
        return rates
    
    def _fetch_rates(self, base_currency: str) -> Optional[Dict[str, float]]:
        """Fetch rates from API with fallback - following official examples"""
        # API endpoints to try in order
        apis = [
            # Try paid API first if key is available
            {
                'name': 'Paid API',
                'url': f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base_currency}",
                'enabled': bool(EXCHANGE_API_KEY),
                'data_key': 'conversion_rates',
                'success_check': lambda data: data.get('result') == 'success'
            },
            # Alternative free API (often more stable)
            {
                'name': 'Alternative API',
                'url': f"https://api.exchangerate.host/latest?base={base_currency}",
                'enabled': True,
                'data_key': 'rates',
                'success_check': lambda data: data.get('success', True)
            },
            # Original free API
            {
                'name': 'Free API',
                'url': f"https://api.exchangerate-api.com/v4/latest/{base_currency}",
                'enabled': True,
                'data_key': 'rates',
                'success_check': lambda data: True
            }
        ]
        
        for api in apis:
            if not api['enabled']:
                continue
                
            try:
                print(f"尝试 {api['name']}...")
                response = self.session.get(
                    api['url'], 
                    timeout=20,
                    verify=True  # Enable SSL verification
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if api['success_check'](data):
                        rates = data.get(api['data_key'], {})
                        if rates and len(rates) > 10:  # Validate response
                            print(f"✅ {api['name']} 成功")
                            return rates
                        else:
                            print(f"⚠️  {api['name']} 返回数据不完整")
                    else:
                        print(f"❌ {api['name']} 返回错误: {data.get('error-type', 'Unknown')}")
                else:
                    print(f"❌ {api['name']} HTTP错误: {response.status_code}")
                    
            except requests.exceptions.SSLError as e:
                print(f"❌ {api['name']} SSL错误: {str(e)[:100]}...")
                continue
            except requests.exceptions.ConnectionError as e:
                print(f"❌ {api['name']} 连接错误: {str(e)[:100]}...")
                continue
            except requests.exceptions.Timeout as e:
                print(f"❌ {api['name']} 超时错误")
                continue
            except requests.RequestException as e:
                print(f"❌ {api['name']} 请求异常: {str(e)[:100]}...")
                continue
            except Exception as e:
                print(f"❌ {api['name']} 未知错误: {str(e)[:100]}...")
                continue
        
        print("❌ 所有API都无法访问")
        return None
    
    def get_conversion_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Get specific conversion rate between two currencies"""
        if from_currency == to_currency:
            return 1.0
        
        # Try direct conversion
        rates = self.get_rates(from_currency)
        if rates and to_currency in rates:
            return rates[to_currency]
        
        # Try reverse conversion
        rates = self.get_rates(to_currency)
        if rates and from_currency in rates:
            return 1.0 / rates[from_currency]
        
        # Try USD as intermediate
        usd_rates = self.get_rates('USD')
        if usd_rates and from_currency in usd_rates and to_currency in usd_rates:
            from_to_usd = 1.0 / usd_rates[from_currency]
            usd_to_target = usd_rates[to_currency]
            return from_to_usd * usd_to_target
        
        return None
    
    def get_all_rates_bulk(self) -> Dict[str, Dict[str, float]]:
        """Pre-fetch all major currency rates for bulk processing"""
        bulk_rates = {}
        
        # Key currencies to fetch rates for bulk processing
        key_currencies = ['USD', 'CNY', 'EUR', 'GBP', 'JPY']
        
        for currency in key_currencies:
            rates = self.get_rates(currency)
            if rates:
                bulk_rates[currency] = rates
        
        return bulk_rates
    
    def get_conversion_rate_bulk(self, from_currency: str, to_currency: str, bulk_rates: Dict[str, Dict[str, float]]) -> Optional[float]:
        """Fast conversion rate lookup using pre-fetched bulk rates"""
        if from_currency == to_currency:
            return 1.0
        
        # Try direct conversion from bulk rates
        if from_currency in bulk_rates and to_currency in bulk_rates[from_currency]:
            return bulk_rates[from_currency][to_currency]
        
        # Try reverse conversion from bulk rates
        if to_currency in bulk_rates and from_currency in bulk_rates[to_currency]:
            return 1.0 / bulk_rates[to_currency][from_currency]
        
        # Try USD as intermediate using bulk rates
        if 'USD' in bulk_rates:
            usd_rates = bulk_rates['USD']
            if from_currency in usd_rates and to_currency in usd_rates:
                from_to_usd = 1.0 / usd_rates[from_currency]
                usd_to_target = usd_rates[to_currency]
                return from_to_usd * usd_to_target
        
        # Fallback to regular API call
        return self.get_conversion_rate(from_currency, to_currency)
    
    def get_available_currencies(self) -> List[str]:
        """Get list of available currencies from the API with fallback"""
        # Try USD first (most common base)
        rates = self.get_rates('USD')
        if rates and len(rates) > 10:  # Valid response should have many currencies
            return list(rates.keys())
        
        # Try EUR as fallback
        rates = self.get_rates('EUR')
        if rates and len(rates) > 10:
            return list(rates.keys())
        
        # If API fails, return our comprehensive default list as fallback
        from config import DEFAULT_CURRENCIES
        print("⚠️  无法从API获取货币列表，使用内置货币列表")
        return DEFAULT_CURRENCIES
    
    def filter_valid_currencies(self, currency_list: List[str]) -> List[str]:
        """Filter currency list to only include currencies available from the API"""
        available = self.get_available_currencies()
        if not available:
            return currency_list  # Return original list if we can't get available currencies
        
        # Filter currencies that are available in the API
        valid_currencies = [currency for currency in currency_list if currency in available]
        return valid_currencies