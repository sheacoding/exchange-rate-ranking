# UV 包管理使用指南

本项目使用 [uv](https://docs.astral.sh/uv/) 作为 Python 包管理器和虚拟环境管理工具。

## 🚀 快速开始

### 1. 安装 uv
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip 安装
pip install uv
```

### 2. 初始化项目
```bash
# 克隆项目后，在项目目录中运行
cd ExchangeRateRanking_py

# 同步依赖（自动创建虚拟环境）
uv sync
```

### 3. 运行程序
```bash
# 主程序
uv run main.py

# 带参数运行
uv run main.py --offline
uv run main.py --popular --amount 5000
uv run main.py --all-currencies

# 使用定义的脚本别名
uv run era              # 等同于 uv run main.py
uv run era-test         # 等同于 uv run test_api.py
uv run era-benchmark    # 等同于 uv run benchmark.py
```

## 📦 依赖管理

### 添加新依赖
```bash
# 添加运行时依赖
uv add requests
uv add "rich>=13.7.0"

# 添加开发依赖
uv add --dev pytest
uv add --dev "black>=23.0.0"

# 添加可选依赖组
uv add --optional test pytest-mock
```

### 更新依赖
```bash
# 更新所有依赖
uv sync --upgrade

# 更新特定依赖
uv add "requests>=2.32.0"
```

### 移除依赖
```bash
# 移除依赖
uv remove requests

# 移除开发依赖
uv remove --dev pytest
```

## 🔧 开发工具

### 代码格式化
```bash
# 安装开发依赖
uv sync --group dev

# 格式化代码
uv run black .

# 检查代码风格
uv run flake8 .

# 类型检查
uv run mypy .
```

### 运行测试
```bash
# 安装测试依赖
uv sync --group test

# 运行测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=.
```

## 🌟 常用命令

### 项目管理
```bash
# 查看项目信息
uv show

# 查看依赖树
uv tree

# 检查过时的依赖
uv sync --dry-run

# 锁定依赖版本
uv lock
```

### 虚拟环境管理
```bash
# 激活虚拟环境 (可选)
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows

# 退出虚拟环境
deactivate

# 查看虚拟环境信息
uv venv --show
```

### 安装项目（可编辑模式）
```bash
# 以可编辑模式安装项目
uv sync --editable

# 安装到系统环境
uv build
pip install dist/*.whl
```

## 🛠️ 实用脚本

项目中定义了以下便捷脚本：

| 脚本名称 | 等效命令 | 描述 |
|---------|---------|------|
| `era` | `uv run main.py` | 运行主程序 |
| `era-test` | `uv run test_api.py` | API连接测试 |
| `era-benchmark` | `uv run benchmark.py` | 性能基准测试 |

使用示例：
```bash
# 运行程序
uv run era --offline

# 测试API连接
uv run era-test

# 性能测试
uv run era-benchmark
```

## 📋 项目结构

```
ExchangeRateRanking_py/
├── pyproject.toml          # 项目配置和依赖
├── uv.lock                 # 锁定文件（版本控制）
├── .venv/                  # 虚拟环境目录
├── main.py                 # 主程序入口
├── config.py               # 配置文件
├── exchange_rate_api.py    # API接口
├── currency_analyzer.py    # 货币分析逻辑
├── utils.py                # 工具函数
├── offline_mode.py         # 离线模式
├── test_api.py            # API测试
├── benchmark.py           # 性能测试
├── network_fix.py         # 网络修复
├── quick_fix.py           # 快速修复
└── README.md              # 项目说明
```

## 💡 最佳实践

### 1. 依赖版本管理
- 使用 `uv.lock` 确保团队环境一致
- 定期运行 `uv sync --upgrade` 更新依赖
- 生产环境使用 `uv sync --frozen` 安装锁定版本

### 2. 开发工作流
```bash
# 每日开发开始
uv sync                     # 同步依赖

# 开发过程中
uv run era --offline        # 测试功能
uv run black .              # 格式化代码
uv run pytest              # 运行测试

# 提交前
uv sync --upgrade           # 更新依赖
uv run pytest              # 确保测试通过
```

### 3. 部署建议
```bash
# 生产环境部署
uv sync --frozen            # 使用锁定版本
uv run era --popular        # 运行程序
```

## 🔍 故障排除

### 常见问题
1. **uv sync 失败**
   ```bash
   # 清理缓存重试
   uv cache clean
   uv sync
   ```

2. **虚拟环境问题**
   ```bash
   # 重建虚拟环境
   rm -rf .venv
   uv venv
   uv sync
   ```

3. **依赖冲突**
   ```bash
   # 查看依赖树找出冲突
   uv tree
   
   # 解决冲突后重新同步
   uv sync --resolution=highest
   ```

## 📚 参考资料

- [uv 官方文档](https://docs.astral.sh/uv/)
- [Python 项目配置指南](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [uv vs pip 对比](https://docs.astral.sh/uv/pip/)

---

有了 uv，依赖管理变得更快、更可靠！🚀