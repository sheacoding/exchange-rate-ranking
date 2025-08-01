#!/usr/bin/env python3
"""
性能基准测试脚本
Performance Benchmark Script

测试不同模式下的性能差异
"""

import time
import click
from rich.console import Console
from rich.table import Table
from currency_analyzer import CurrencyAnalyzer
from config import DEFAULT_CURRENCIES, POPULAR_CURRENCIES
from performance_monitor import perf_monitor

console = Console()

def benchmark_currency_analysis():
    """Benchmark different currency analysis modes"""
    console.print("[bold blue]🚀 汇率分析性能基准测试[/bold blue]\n")
    
    analyzer = CurrencyAnalyzer()
    test_amount = 10000.0
    
    # Test scenarios
    scenarios = [
        ("小规模测试 (10货币)", DEFAULT_CURRENCIES[:10]),
        ("中等规模测试 (30货币)", POPULAR_CURRENCIES),
        ("大规模测试 (50货币)", DEFAULT_CURRENCIES[:50]),
    ]
    
    results_table = Table(title="性能测试结果")
    results_table.add_column("测试场景", style="cyan")
    results_table.add_column("货币数量", style="magenta")
    results_table.add_column("顺序处理时间", style="yellow")
    results_table.add_column("批量处理时间", style="green")
    results_table.add_column("性能提升", style="bold green")
    
    for scenario_name, currencies in scenarios:
        console.print(f"\n正在测试: {scenario_name}")
        
        # Test sequential processing
        console.print("  测试顺序处理...")
        start_time = time.time()
        sequential_paths = analyzer._analyze_conversion_paths_sequential(test_amount, currencies)
        sequential_time = time.time() - start_time
        
        # Reset analyzer for bulk test
        analyzer = CurrencyAnalyzer()
        
        # Test bulk processing
        console.print("  测试批量处理...")
        start_time = time.time()
        bulk_paths = analyzer._analyze_conversion_paths_bulk(test_amount, currencies)
        bulk_time = time.time() - start_time
        
        # Calculate improvement
        improvement = ((sequential_time - bulk_time) / sequential_time * 100) if sequential_time > 0 else 0
        
        results_table.add_row(
            scenario_name,
            str(len(currencies)),
            f"{sequential_time:.2f}秒",
            f"{bulk_time:.2f}秒",
            f"{improvement:+.1f}%"
        )
        
        console.print(f"  顺序处理: {sequential_time:.2f}秒")
        console.print(f"  批量处理: {bulk_time:.2f}秒")
        console.print(f"  性能提升: {improvement:+.1f}%")
    
    console.print("\n")
    console.print(results_table)
    
    # Print performance monitor report
    perf_monitor.print_performance_report()

@click.command()
@click.option('--full-test', is_flag=True, help='Run full scale test with all currencies')
def main(full_test):
    """Run performance benchmark tests"""
    if full_test:
        console.print("[yellow]警告: 全规模测试将使用所有可用货币，可能需要较长时间[/yellow]")
        if click.confirm("是否继续?"):
            analyzer = CurrencyAnalyzer()
            all_currencies = analyzer.api.get_available_currencies()
            console.print(f"将测试 {len(all_currencies)} 种货币")
            
            start_time = time.time()
            analyzer._analyze_conversion_paths_bulk(10000.0, all_currencies)
            total_time = time.time() - start_time
            
            console.print(f"全规模测试完成，总耗时: {total_time:.2f}秒")
            perf_monitor.print_performance_report()
    else:
        benchmark_currency_analysis()

if __name__ == '__main__':
    main()