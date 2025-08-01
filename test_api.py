#!/usr/bin/env python3
"""
简单API测试脚本
Simple API Test Script
"""

import sys
from exchange_rate_api import ExchangeRateAPI
from rich.console import Console

console = Console()

def test_api_connection():
    """Test API connection with simple calls"""
    console.print("[bold blue]🔍 API连接测试[/bold blue]\n")
    
    api = ExchangeRateAPI()
    
    # Test 1: Get USD rates
    console.print("测试1: 获取USD汇率...")
    usd_rates = api.get_rates('USD')
    
    if usd_rates:
        console.print(f"[green]✅ 成功获取USD汇率[/green]")
        console.print(f"货币数量: {len(usd_rates)}")
        console.print(f"包含CNY: {'CNY' in usd_rates}")
        console.print(f"USD->CNY汇率: {usd_rates.get('CNY', 'N/A')}")
    else:
        console.print("[red]❌ 无法获取USD汇率[/red]")
        return False
    
    # Test 2: Get CNY rates
    console.print("\n测试2: 获取CNY汇率...")
    cny_rates = api.get_rates('CNY')
    
    if cny_rates:
        console.print(f"[green]✅ 成功获取CNY汇率[/green]")
        console.print(f"货币数量: {len(cny_rates)}")
        console.print(f"包含USD: {'USD' in cny_rates}")
        console.print(f"CNY->USD汇率: {cny_rates.get('USD', 'N/A')}")
    else:
        console.print("[red]❌ 无法获取CNY汇率[/red]")
        return False
    
    # Test 3: Direct conversion
    console.print("\n测试3: 直接汇率转换...")
    cny_to_usd = api.get_conversion_rate('CNY', 'USD')
    
    if cny_to_usd:
        console.print(f"[green]✅ CNY->USD转换成功[/green]")
        console.print(f"1 CNY = {cny_to_usd:.6f} USD")
    else:
        console.print("[red]❌ CNY->USD转换失败[/red]")
        return False
    
    # Test 4: Available currencies
    console.print("\n测试4: 获取可用货币列表...")
    available = api.get_available_currencies()
    
    if available:
        console.print(f"[green]✅ 成功获取货币列表[/green]")
        console.print(f"可用货币数量: {len(available)}")
        console.print(f"前10种货币: {available[:10]}")
    else:
        console.print("[red]❌ 无法获取货币列表[/red]")
        return False
    
    console.print(f"\n[bold green]🎉 所有测试通过！API连接正常[/bold green]")
    return True

if __name__ == '__main__':
    success = test_api_connection()
    sys.exit(0 if success else 1)