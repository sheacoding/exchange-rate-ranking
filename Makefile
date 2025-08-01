# Exchange Rate Ranking - Makefile
# 简化常用操作的快捷命令

.PHONY: help install dev test lint format clean run run-offline run-popular benchmark api-test

# Default target
help:
	@echo "Exchange Rate Ranking - 可用命令:"
	@echo ""
	@echo "  install     - 安装项目依赖"
	@echo "  dev         - 安装开发依赖"
	@echo "  test        - 运行测试"
	@echo "  lint        - 代码检查"
	@echo "  format      - 代码格式化"
	@echo "  clean       - 清理缓存文件"
	@echo ""
	@echo "  run         - 运行主程序"
	@echo "  run-offline - 离线模式运行"
	@echo "  run-popular - 热门货币分析"
	@echo "  benchmark   - 性能测试"
	@echo "  api-test    - API连接测试"
	@echo ""
	@echo "使用示例: make install && make run"

# Installation
install:
	@echo "📦 安装项目依赖..."
	uv sync

dev:
	@echo "🛠️ 安装开发依赖..."
	uv sync --group dev

# Testing
test:
	@echo "🧪 运行测试..."
	uv run pytest

test-cov:
	@echo "📊 运行测试并生成覆盖率报告..."
	uv run pytest --cov=. --cov-report=html

# Code quality
lint:
	@echo "🔍 代码检查..."
	uv run flake8 .
	uv run mypy .

format:
	@echo "✨ 代码格式化..."
	uv run black .

format-check:
	@echo "📝 检查代码格式..."
	uv run black --check .

# Cleanup
clean:
	@echo "🧹 清理缓存文件..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete

# Application commands
run:
	@echo "🚀 运行汇率分析工具..."
	uv run era

run-offline:
	@echo "📱 离线模式运行..."
	uv run era --offline

run-popular:
	@echo "⭐ 热门货币分析..."
	uv run era --popular

run-all:
	@echo "🌍 全货币分析..."
	uv run era --all-currencies

# Testing and benchmarking
benchmark:
	@echo "⚡ 性能基准测试..."
	uv run era-benchmark

benchmark-full:
	@echo "🔥 全规模性能测试..."
	uv run era-benchmark --full-test

api-test:
	@echo "🔌 API连接测试..."
	uv run era-test

network-test:
	@echo "🌐 网络连接测试..."
	uv run network_fix.py

# Development workflow
dev-setup: install dev
	@echo "✅ 开发环境设置完成!"

check: format-check lint test
	@echo "✅ 代码检查完成!"

# Quick fixes
quick-fix:
	@echo "🔧 运行快速修复..."
	uv run quick_fix.py

# Documentation
docs-deps:
	@echo "📚 安装文档依赖..."
	uv add --dev mkdocs mkdocs-material

docs-serve:
	@echo "📖 启动文档服务器..."
	uv run mkdocs serve

# Build and distribution
build:
	@echo "📦 构建项目..."
	uv build

publish-test:
	@echo "🚀 发布到测试PyPI..."
	uv publish --repository testpypi

publish:
	@echo "🎉 发布到PyPI..."
	uv publish

# Environment management
env-info:
	@echo "ℹ️ 环境信息:"
	uv show
	@echo ""
	uv tree

env-update:
	@echo "🔄 更新依赖..."
	uv sync --upgrade

env-lock:
	@echo "🔒 锁定依赖版本..."
	uv lock

# Convenience targets for common workflows
demo: run-offline
	@echo "💡 提示: 您刚刚运行了离线演示模式"

start: run-popular
	@echo "💡 提示: 使用 'make run' 来运行完整交互模式"

ci: check
	@echo "✅ CI检查通过!"