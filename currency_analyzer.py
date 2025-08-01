from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from exchange_rate_api import ExchangeRateAPI

@dataclass
class ConversionPath:
    intermediate_currency: str
    cny_to_intermediate_rate: float
    intermediate_to_usd_rate: float
    total_usd_amount: float
    efficiency_score: float

class CurrencyAnalyzer:
    def __init__(self):
        self.api = ExchangeRateAPI()
        self.bulk_rates = None
        self.direct_cny_to_usd = None
    
    def analyze_conversion_paths(self, cny_amount: float, currencies: List[str], use_bulk_processing: bool = True) -> List[ConversionPath]:
        """Analyze all possible conversion paths from CNY to USD through intermediate currencies"""
        if use_bulk_processing and len(currencies) > 20:
            return self._analyze_conversion_paths_bulk(cny_amount, currencies)
        else:
            return self._analyze_conversion_paths_sequential(cny_amount, currencies)
    
    def _analyze_conversion_paths_sequential(self, cny_amount: float, currencies: List[str]) -> List[ConversionPath]:
        """Sequential processing for small currency lists"""
        paths = []
        
        for currency in currencies:
            if currency in ['CNY', 'USD']:
                continue
            
            path = self._calculate_conversion_path(cny_amount, currency)
            if path:
                paths.append(path)
        
        # Sort by efficiency score (higher is better)
        paths.sort(key=lambda x: x.efficiency_score, reverse=True)
        return paths
    
    def _analyze_conversion_paths_bulk(self, cny_amount: float, currencies: List[str]) -> List[ConversionPath]:
        """Optimized bulk processing for large currency lists"""
        # Pre-fetch bulk rates to minimize API calls
        print("正在预加载汇率数据...")
        start_time = time.time()
        
        self.bulk_rates = self.api.get_all_rates_bulk()
        self.direct_cny_to_usd = self.api.get_conversion_rate_bulk('CNY', 'USD', self.bulk_rates)
        
        print(f"预加载完成，耗时 {time.time() - start_time:.2f} 秒")
        
        # Filter currencies and process in batches
        valid_currencies = [c for c in currencies if c not in ['CNY', 'USD']]
        
        paths = []
        batch_size = 50  # Process in batches to show progress
        
        for i in range(0, len(valid_currencies), batch_size):
            batch = valid_currencies[i:i + batch_size]
            print(f"正在处理第 {i//batch_size + 1} 批货币 ({i+1}-{min(i+batch_size, len(valid_currencies))}/{len(valid_currencies)})")
            
            batch_paths = self._process_currency_batch(cny_amount, batch)
            paths.extend(batch_paths)
        
        # Sort by efficiency score (higher is better)
        paths.sort(key=lambda x: x.efficiency_score, reverse=True)
        return paths
    
    def _process_currency_batch(self, cny_amount: float, currencies: List[str]) -> List[ConversionPath]:
        """Process a batch of currencies with threading"""
        paths = []
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit all currency calculations
            future_to_currency = {
                executor.submit(self._calculate_conversion_path_bulk, cny_amount, currency): currency
                for currency in currencies
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_currency):
                path = future.result()
                if path:
                    paths.append(path)
        
        return paths
    
    def _calculate_conversion_path_bulk(self, cny_amount: float, intermediate_currency: str) -> Optional[ConversionPath]:
        """Fast conversion path calculation using bulk rates"""
        if not self.bulk_rates or not self.direct_cny_to_usd:
            return self._calculate_conversion_path(cny_amount, intermediate_currency)
        
        # Get CNY to intermediate rate using bulk rates
        cny_to_intermediate = self.api.get_conversion_rate_bulk('CNY', intermediate_currency, self.bulk_rates)
        if not cny_to_intermediate:
            return None
        
        # Get intermediate to USD rate using bulk rates
        intermediate_to_usd = self.api.get_conversion_rate_bulk(intermediate_currency, 'USD', self.bulk_rates)
        if not intermediate_to_usd:
            return None
        
        # Calculate total USD amount after conversion
        intermediate_amount = cny_amount * cny_to_intermediate
        usd_amount = intermediate_amount * intermediate_to_usd
        
        # Use cached direct CNY to USD rate
        direct_usd_amount = cny_amount * self.direct_cny_to_usd
        
        # Calculate efficiency score
        efficiency_score = (usd_amount / direct_usd_amount - 1) * 100 if direct_usd_amount > 0 else 0
        
        return ConversionPath(
            intermediate_currency=intermediate_currency,
            cny_to_intermediate_rate=cny_to_intermediate,
            intermediate_to_usd_rate=intermediate_to_usd,
            total_usd_amount=usd_amount,
            efficiency_score=efficiency_score
        )
    
    def _calculate_conversion_path(self, cny_amount: float, intermediate_currency: str) -> Optional[ConversionPath]:
        """Calculate conversion path: CNY -> Intermediate -> USD"""
        # Get CNY to intermediate rate
        cny_to_intermediate = self.api.get_conversion_rate('CNY', intermediate_currency)
        if not cny_to_intermediate:
            return None
        
        # Get intermediate to USD rate
        intermediate_to_usd = self.api.get_conversion_rate(intermediate_currency, 'USD')
        if not intermediate_to_usd:
            return None
        
        # Calculate total USD amount after conversion
        intermediate_amount = cny_amount * cny_to_intermediate
        usd_amount = intermediate_amount * intermediate_to_usd
        
        # Calculate direct CNY to USD for comparison
        direct_cny_to_usd = self.api.get_conversion_rate('CNY', 'USD')
        if not direct_cny_to_usd:
            return None
        
        direct_usd_amount = cny_amount * direct_cny_to_usd
        
        # Calculate efficiency score (how much better this path is compared to direct conversion)
        efficiency_score = (usd_amount / direct_usd_amount - 1) * 100 if direct_usd_amount > 0 else 0
        
        return ConversionPath(
            intermediate_currency=intermediate_currency,
            cny_to_intermediate_rate=cny_to_intermediate,
            intermediate_to_usd_rate=intermediate_to_usd,
            total_usd_amount=usd_amount,
            efficiency_score=efficiency_score
        )
    
    def get_direct_conversion(self, cny_amount: float) -> Optional[float]:
        """Get direct CNY to USD conversion for comparison"""
        rate = self.api.get_conversion_rate('CNY', 'USD')
        return cny_amount * rate if rate else None
    
    def get_best_conversion_recommendation(self, cny_amount: float, currencies: List[str]) -> Dict:
        """Get the best conversion recommendation with analysis"""
        paths = self.analyze_conversion_paths(cny_amount, currencies)
        direct_usd = self.get_direct_conversion(cny_amount)
        
        if not paths:
            return {
                'status': 'error',
                'message': 'No conversion paths available'
            }
        
        best_path = paths[0]
        
        return {
            'status': 'success',
            'cny_amount': cny_amount,
            'direct_usd_amount': direct_usd,
            'best_path': best_path,
            'all_paths': paths,  # All paths for comprehensive analysis
            'savings': best_path.total_usd_amount - direct_usd if direct_usd else 0,
            'savings_percentage': best_path.efficiency_score
        }