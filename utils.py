from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from currency_analyzer import ConversionPath

console = Console()

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount with proper symbols"""
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'CNY': '¥',
        'KRW': '₩',
        'HKD': 'HK$',
        'SGD': 'S$',
        'AUD': 'A$',
        'CAD': 'C$',
        'CHF': 'CHF '
    }
    
    symbol = symbols.get(currency, currency + ' ')
    
    if currency == 'JPY' or currency == 'KRW':
        return f"{symbol}{amount:,.0f}"
    else:
        return f"{symbol}{amount:,.4f}"

def format_rate(rate: float) -> str:
    """Format exchange rate"""
    return f"{rate:.6f}"

def format_percentage(percentage: float) -> str:
    """Format percentage with color coding"""
    if percentage > 0:
        return f"[green]+{percentage:.4f}%[/green]"
    elif percentage < 0:
        return f"[red]{percentage:.4f}%[/red]"
    else:
        return f"{percentage:.4f}%"

def display_conversion_analysis(analysis: dict):
    """Display the conversion analysis in a formatted table"""
    if analysis['status'] != 'success':
        console.print(f"[red]Error: {analysis['message']}[/red]")
        return
    
    cny_amount = analysis['cny_amount']
    direct_usd = analysis['direct_usd_amount']
    best_path = analysis['best_path']
    all_paths = analysis['all_paths']
    
    # Header
    console.print("\n" + "="*80)
    console.print(f"[bold blue]汇率兑换分析报告 (Exchange Rate Analysis)[/bold blue]")
    console.print(f"原始金额 (Original Amount): [bold]{format_currency(cny_amount, 'CNY')}[/bold]")
    console.print("="*80)
    
    # Direct conversion info
    console.print(f"\n[bold]直接兑换 (Direct Conversion):[/bold]")
    console.print(f"CNY → USD: {format_currency(direct_usd, 'USD')}")
    
    # Best path recommendation
    console.print(f"\n[bold green]最佳兑换路径 (Best Conversion Path):[/bold green]")
    console.print(f"路径: CNY → {best_path.intermediate_currency} → USD")
    console.print(f"最终金额: {format_currency(best_path.total_usd_amount, 'USD')}")
    console.print(f"节省金额: {format_currency(analysis['savings'], 'USD')}")
    console.print(f"收益率: {format_percentage(best_path.efficiency_score)}")
    
    # Statistics
    total_currencies = len(all_paths)
    positive_paths = len([p for p in all_paths if p.efficiency_score > 0])
    
    console.print(f"\n[bold]分析统计 (Analysis Statistics):[/bold]")
    console.print(f"总分析货币: {total_currencies} 种")
    console.print(f"有正收益的路径: {positive_paths} 条")
    console.print(f"收益率范围: {min(p.efficiency_score for p in all_paths):+.4f}% ~ {max(p.efficiency_score for p in all_paths):+.4f}%")
    
    # Determine how many rows to show
    max_display = 50  # Maximum rows to display in table
    display_paths = all_paths[:max_display]
    
    # Detailed paths table
    table_title = f"\n汇率排行榜 - 前{len(display_paths)}名"
    if total_currencies > max_display:
        table_title += f" (共{total_currencies}种货币)"
    
    table = Table(title=table_title)
    table.add_column("排名", style="cyan", no_wrap=True, width=4)
    table.add_column("中间货币", style="magenta", width=8)
    table.add_column("CNY汇率", style="cyan", width=10)
    table.add_column("USD汇率", style="cyan", width=10) 
    table.add_column("最终USD", style="green", width=12)
    table.add_column("收益率", style="yellow", width=10)
    
    for i, path in enumerate(display_paths, 1):
        efficiency_color = "green" if path.efficiency_score > 0 else "red" if path.efficiency_score < 0 else "white"
        
        table.add_row(
            str(i),
            path.intermediate_currency,
            format_rate(path.cny_to_intermediate_rate),
            format_rate(path.intermediate_to_usd_rate),
            format_currency(path.total_usd_amount, 'USD'),
            f"[{efficiency_color}]{path.efficiency_score:+.4f}%[/{efficiency_color}]"
        )
    
    console.print(table)
    
    if total_currencies > max_display:
        console.print(f"\n[dim]注: 仅显示前{max_display}条结果，完整列表包含{total_currencies}种货币[/dim]")
    
    # Summary
    if best_path.efficiency_score > 0:
        console.print(f"\n[bold green]推荐使用 {best_path.intermediate_currency} 作为中间货币，可获得额外收益！[/bold green]")
    else:
        console.print(f"\n[bold yellow]直接兑换可能是更好的选择。[/bold yellow]")

def display_loading():
    """Display loading message"""
    console.print("[bold blue]正在获取实时汇率数据...[/bold blue]")

def create_progress_bar():
    """Create a progress bar for currency processing"""
    return Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        console=console
    )

def display_error(message: str):
    """Display error message"""
    console.print(f"[bold red]错误: {message}[/bold red]")