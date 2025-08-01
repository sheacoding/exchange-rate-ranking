import time
import functools
from typing import Dict, Any
from rich.console import Console

console = Console()

class PerformanceMonitor:
    def __init__(self):
        self.timings = {}
        self.api_calls = 0
        self.cache_hits = 0
        self.cache_misses = 0
    
    def time_function(self, func_name: str):
        """Decorator to time function execution"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                
                execution_time = end_time - start_time
                if func_name not in self.timings:
                    self.timings[func_name] = []
                self.timings[func_name].append(execution_time)
                
                return result
            return wrapper
        return decorator
    
    def record_api_call(self):
        """Record an API call"""
        self.api_calls += 1
    
    def record_cache_hit(self):
        """Record a cache hit"""
        self.cache_hits += 1
    
    def record_cache_miss(self):
        """Record a cache miss"""
        self.cache_misses += 1
    
    def print_performance_report(self):
        """Print detailed performance report"""
        console.print("\n[bold blue]🔍 性能分析报告 (Performance Analysis Report)[/bold blue]")
        console.print("=" * 60)
        
        # API statistics
        total_cache_operations = self.cache_hits + self.cache_misses
        cache_hit_rate = (self.cache_hits / total_cache_operations * 100) if total_cache_operations > 0 else 0
        
        console.print(f"API调用次数: {self.api_calls}")
        console.print(f"缓存命中率: {cache_hit_rate:.1f}% ({self.cache_hits}/{total_cache_operations})")
        
        # Function timing statistics
        if self.timings:
            console.print("\n[bold]函数执行时间统计:[/bold]")
            for func_name, times in self.timings.items():
                avg_time = sum(times) / len(times)
                total_time = sum(times)
                console.print(f"  {func_name}:")
                console.print(f"    平均: {avg_time:.3f}秒")
                console.print(f"    总计: {total_time:.3f}秒")
                console.print(f"    调用: {len(times)}次")
        
        # Performance recommendations
        console.print(f"\n[bold]性能建议:[/bold]")
        if self.api_calls > 50:
            console.print("  ⚠️  API调用次数较多，建议使用批量模式")
        if cache_hit_rate < 50:
            console.print("  ⚠️  缓存命中率较低，考虑优化缓存策略")
        if cache_hit_rate > 80:
            console.print("  ✅ 缓存效率良好")
        
        console.print("=" * 60)

# Global performance monitor instance
perf_monitor = PerformanceMonitor()