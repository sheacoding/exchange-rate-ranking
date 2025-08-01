#!/usr/bin/env python3
"""
汇率兑换排行分析工具
Exchange Rate Ranking Analysis Tool

实时查询全球汇率，分析人民币通过中间货币兑换美元的最优路径
Real-time global exchange rate analysis for optimal CNY to USD conversion paths
"""

import click
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt
from currency_analyzer import CurrencyAnalyzer
from utils import display_conversion_analysis, display_loading, display_error, console
from config import DEFAULT_CURRENCIES, POPULAR_CURRENCIES
from offline_mode import OfflineExchangeAPI, get_offline_demo_message, is_network_available

@click.command()
@click.option('--amount', '-a', type=float, help='CNY amount to convert')
@click.option('--currencies', '-c', help='Comma-separated list of intermediate currencies')
@click.option('--all-currencies', is_flag=True, help='Use all available currencies from API')
@click.option('--popular', is_flag=True, help='Use popular currencies only')
@click.option('--offline', is_flag=True, help='Force offline demo mode')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def main(amount, currencies, all_currencies, popular, offline, debug):
    """
    汇率兑换排行分析工具
    
    分析人民币通过不同中间货币兑换美元的效率，帮助找到最具性价比的兑换路径。
    """
    console.print("[bold blue]🌍 汇率兑换排行分析工具[/bold blue]")
    console.print("[dim]Exchange Rate Ranking Analysis Tool[/dim]\n")
    
    try:
        # Get CNY amount
        if not amount:
            amount = FloatPrompt.ask("请输入人民币金额 (Enter CNY amount)", default=10000.0)
        
        if amount <= 0:
            display_error("金额必须大于0")
            return
        
        # Check network and initialize analyzer
        use_offline_mode = offline or not is_network_available()
        
        if use_offline_mode:
            console.print(get_offline_demo_message())
            if not click.confirm("是否继续使用离线演示模式?", default=True):
                return
            
            # Create offline analyzer
            analyzer = CurrencyAnalyzer()
            analyzer.api = OfflineExchangeAPI()  # Replace with offline API
        else:
            analyzer = CurrencyAnalyzer()
        
        # Get currencies list
        if currencies:
            currency_list = [c.strip().upper() for c in currencies.split(',')]
        elif all_currencies:
            console.print("[yellow]获取API支持的所有货币列表...[/yellow]")
            try:
                available_currencies = analyzer.api.get_available_currencies()
                # Remove CNY and USD from the list as they are source and target
                currency_list = [c for c in available_currencies if c not in ['CNY', 'USD']]
                
                if len(currency_list) > 0:
                    console.print(f"[green]找到 {len(currency_list)} 种可用货币[/green]")
                else:
                    console.print("[red]未找到可用货币，API可能有问题[/red]")
                    console.print("[yellow]建议运行: python test_api.py 来诊断问题[/yellow]")
                    return
            except Exception as e:
                console.print(f"[red]获取货币列表时发生错误: {e}[/red]")
                console.print("[yellow]建议运行: python test_api.py 来诊断问题[/yellow]")
                return
        elif popular:
            currency_list = POPULAR_CURRENCIES
        else:
            currency_choice = Prompt.ask(
                "选择货币列表 (Choose currency list)",
                choices=['1', '2', '3', '4'],
                default='1'
            )
            
            console.print("\n货币列表选项:")
            console.print("1. 全部货币 (All currencies) - 最全面的分析")
            console.print("2. 热门货币 (Popular currencies) - 常用货币快速分析") 
            console.print("3. 默认货币 (Default currencies) - 平衡的选择")
            console.print("4. 自定义货币 (Custom currencies) - 手动选择")
            
            if currency_choice == '1':
                console.print("[yellow]获取API支持的所有货币列表...[/yellow]")
                try:
                    available_currencies = analyzer.api.get_available_currencies()
                    currency_list = [c for c in available_currencies if c not in ['CNY', 'USD']]
                    
                    if len(currency_list) > 0:
                        console.print(f"[green]找到 {len(currency_list)} 种可用货币[/green]")
                    else:
                        console.print("[red]未找到可用货币，使用默认列表[/red]")
                        currency_list = DEFAULT_CURRENCIES
                except Exception as e:
                    console.print(f"[red]获取货币列表时发生错误: {e}[/red]")
                    console.print("[yellow]使用默认货币列表[/yellow]")
                    currency_list = DEFAULT_CURRENCIES
            elif currency_choice == '2':
                currency_list = POPULAR_CURRENCIES
            elif currency_choice == '3':
                currency_list = DEFAULT_CURRENCIES
            else:
                custom_currencies = Prompt.ask(
                    "请输入货币代码，用逗号分隔 (Enter currency codes, comma-separated)",
                    default='EUR,GBP,JPY,KRW,HKD'
                )
                currency_list = [c.strip().upper() for c in custom_currencies.split(',')]
        
        # Filter to only valid currencies available from API
        console.print("[yellow]验证货币有效性...[/yellow]")
        valid_currencies = analyzer.api.filter_valid_currencies(currency_list)
        
        if len(valid_currencies) < len(currency_list):
            invalid_currencies = set(currency_list) - set(valid_currencies)
            console.print(f"[yellow]以下货币不可用: {', '.join(invalid_currencies)}[/yellow]")
        
        if not valid_currencies:
            display_error("没有可用的货币进行分析")
            return
            
        console.print(f"[green]将分析 {len(valid_currencies)} 种货币[/green]: {', '.join(valid_currencies[:10])}{'...' if len(valid_currencies) > 10 else ''}\n")
        
        # Perform analysis
        display_loading()
        
        analysis = analyzer.get_best_conversion_recommendation(amount, valid_currencies)
        
        # Display results
        display_conversion_analysis(analysis)
        
        # Interactive mode
        while True:
            action = Prompt.ask(
                "\n选择操作 (Choose action)",
                choices=['r', 'n', 'q'],
                default='q'
            )
            
            if action == 'r':
                # Refresh analysis
                console.print("[yellow]🔄 刷新汇率数据...[/yellow]")
                try:
                    # Clear cache and create new analyzer
                    analyzer.api.clear_cache()
                    
                    if use_offline_mode:
                        analyzer = CurrencyAnalyzer()
                        analyzer.api = OfflineExchangeAPI()
                    else:
                        analyzer = CurrencyAnalyzer()
                    
                    display_loading()
                    analysis = analyzer.get_best_conversion_recommendation(amount, valid_currencies)
                    display_conversion_analysis(analysis)
                except Exception as e:
                    display_error(f"刷新时发生错误: {str(e)}")
                    if not use_offline_mode:
                        console.print("[yellow]提示: 网络连接可能不稳定，可尝试离线模式: --offline[/yellow]")
            elif action == 'n':
                # New analysis
                amount = FloatPrompt.ask("请输入新的人民币金额", default=amount)
                display_loading()
                analysis = analyzer.get_best_conversion_recommendation(amount, valid_currencies)
                display_conversion_analysis(analysis)
            else:
                break
        
        console.print("\n[bold blue]感谢使用汇率分析工具！[/bold blue]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]程序已退出[/yellow]")
    except Exception as e:
        if debug:
            console.print_exception()
        else:
            display_error(f"发生错误: {str(e)}")

if __name__ == '__main__':
    main()