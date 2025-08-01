"""
离线模式和演示数据
Offline Mode and Demo Data

当网络连接有问题时，使用模拟数据进行演示
"""

from typing import Dict
import time
import random

class OfflineExchangeAPI:
    """离线模式的汇率API模拟"""
    
    def __init__(self):
        self.cache = {}
        self.cache_timestamps = {}
        
        # 模拟汇率数据 (基于真实汇率的近似值)
        self.demo_rates = {
            'USD': {
                'CNY': 7.2345, 'EUR': 0.8234, 'GBP': 0.7123, 'JPY': 149.56,
                'KRW': 1324.45, 'HKD': 7.8123, 'SGD': 1.3456, 'AUD': 1.5234,
                'CAD': 1.3567, 'CHF': 0.8945, 'TWD': 31.234, 'THB': 35.67,
                'MYR': 4.6789, 'INR': 83.234, 'AED': 3.6725, 'SAR': 3.7501,
                'NOK': 10.567, 'SEK': 10.234, 'DKK': 6.8901, 'RUB': 91.234,
                'ZAR': 18.567, 'MXN': 17.234, 'BRL': 4.9876, 'ARS': 865.23,
                'TRY': 27.345, 'PLN': 4.0567, 'CZK': 22.345, 'HUF': 356.78,
                'ILS': 3.6789, 'NZD': 1.6234
            }
        }
        
        # 计算反向汇率
        for base in list(self.demo_rates.keys()):
            for target, rate in self.demo_rates[base].items():
                if target not in self.demo_rates:
                    self.demo_rates[target] = {}
                self.demo_rates[target][base] = 1.0 / rate
        
        # 添加CNY基准汇率
        self.demo_rates['CNY'] = {}
        for currency, rate in self.demo_rates['USD'].items():
            if currency != 'CNY':
                cny_rate = rate / self.demo_rates['USD']['CNY']
                self.demo_rates['CNY'][currency] = cny_rate
        
        self.demo_rates['CNY']['USD'] = 1.0 / self.demo_rates['USD']['CNY']
    
    def get_rates(self, base_currency: str = 'USD') -> Dict[str, float]:
        """获取模拟汇率数据"""
        if base_currency in self.demo_rates:
            # 添加少量随机波动来模拟实时数据
            rates = {}
            for currency, rate in self.demo_rates[base_currency].items():
                # 添加±0.5%的随机波动
                variation = random.uniform(-0.005, 0.005)
                rates[currency] = rate * (1 + variation)
            
            print(f"📱 使用离线模式数据 ({base_currency} 基准)")
            return rates
        else:
            print(f"⚠️  离线模式不支持 {base_currency} 基准货币")
            return {}
    
    def get_conversion_rate(self, from_currency: str, to_currency: str) -> float:
        """获取特定货币转换率"""
        if from_currency == to_currency:
            return 1.0
        
        # 尝试直接转换
        from_rates = self.get_rates(from_currency)
        if to_currency in from_rates:
            return from_rates[to_currency]
        
        # 通过USD中转
        usd_rates = self.get_rates('USD')
        if from_currency in usd_rates and to_currency in usd_rates:
            from_to_usd = 1.0 / usd_rates[from_currency]
            usd_to_target = usd_rates[to_currency]
            return from_to_usd * usd_to_target
        
        return None
    
    def get_available_currencies(self):
        """获取可用货币列表"""
        all_currencies = set()
        for base_rates in self.demo_rates.values():
            all_currencies.update(base_rates.keys())
        all_currencies.update(self.demo_rates.keys())
        
        print(f"📱 离线模式支持 {len(all_currencies)} 种货币")
        return list(all_currencies)
    
    def clear_cache(self):
        """清空缓存（离线模式无需实际清空）"""
        print("📱 离线模式 - 缓存已清空")

def is_network_available() -> bool:
    """检测网络是否可用"""
    import requests
    try:
        response = requests.get("https://httpbin.org/get", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_offline_demo_message():
    """获取离线模式说明"""
    return """
🔌 离线演示模式

由于网络连接问题，程序已切换到离线演示模式。

特点:
• 使用模拟汇率数据（基于真实汇率）
• 支持30+种主要货币
• 每次查询会有小幅波动模拟实时性
• 所有功能正常工作，仅数据为演示数据

注意: 这些数据仅用于演示程序功能，不能用于实际交易！
"""

if __name__ == '__main__':
    # 测试离线模式
    offline_api = OfflineExchangeAPI()
    print("测试离线模式...")
    
    usd_rates = offline_api.get_rates('USD')
    print(f"USD汇率数量: {len(usd_rates)}")
    print(f"USD->CNY: {usd_rates.get('CNY', 'N/A')}")
    
    cny_to_usd = offline_api.get_conversion_rate('CNY', 'USD')
    print(f"CNY->USD: {cny_to_usd}")
    
    currencies = offline_api.get_available_currencies()
    print(f"支持货币: {len(currencies)}")