#!/usr/bin/env python3
"""
快速修复脚本
Quick Fix Script

解决常见的网络和SSL问题
"""

import sys
import subprocess
from rich.console import Console

console = Console()

def install_dependencies():
    """安装或升级必要的依赖"""
    console.print("[bold blue]🔧 安装/升级依赖包...[/bold blue]")
    
    packages = [
        "requests>=2.31.0",
        "certifi>=2023.7.22", 
        "urllib3>=2.0.0",
        "rich>=13.7.0"
    ]
    
    for package in packages:
        try:
            console.print(f"安装 {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", package], 
                         check=True, capture_output=True)
            console.print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            console.print(f"❌ {package} 安装失败: {e}")

def test_program():
    """测试程序是否能正常运行"""
    console.print("\n[bold blue]🧪 测试程序...[/bold blue]")
    
    try:
        # 测试离线模式
        console.print("测试离线模式:")
        result = subprocess.run([
            sys.executable, "main.py", "--offline", "--amount", "1000", 
            "--currencies", "EUR,GBP,JPY"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            console.print("✅ 离线模式测试成功")
        else:
            console.print(f"❌ 离线模式测试失败: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        console.print("⚠️  程序测试超时")
    except Exception as e:
        console.print(f"❌ 测试过程出错: {e}")

def show_usage_tips():
    """显示使用建议"""
    console.print("\n[bold green]💡 使用建议:[/bold green]")
    
    tips = [
        "如果网络有问题，使用: python main.py --offline",
        "快速分析少量货币: python main.py --currencies 'EUR,GBP,JPY'", 
        "热门货币分析: python main.py --popular",
        "API连接测试: python test_api.py",
        "网络诊断: python network_fix.py"
    ]
    
    for i, tip in enumerate(tips, 1):
        console.print(f"{i}. {tip}")

def main():
    """主函数"""
    console.print("[bold blue]🚀 汇率分析工具快速修复[/bold blue]\n")
    
    # 安装依赖
    install_dependencies()
    
    # 测试程序
    test_program()
    
    # 显示使用建议
    show_usage_tips()
    
    console.print(f"\n[bold green]🎉 修复完成！现在可以尝试运行程序了[/bold green]")
    console.print("[yellow]推荐首先尝试: python main.py --offline[/yellow]")

if __name__ == '__main__':
    main()