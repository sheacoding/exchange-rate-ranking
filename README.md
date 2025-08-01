# 汇率兑换排行分析工具 / Exchange Rate Ranking Analysis Tool

一个智能的终端应用程序，用于分析人民币通过不同中间货币兑换美元的最优路径，帮助找到最具性价比的货币兑换方案。

An intelligent terminal application that analyzes optimal conversion paths from Chinese Yuan (CNY) to US Dollar (USD) through various intermediate currencies, helping you find the most cost-effective currency exchange solutions.

## 功能特点 / Features

- 🌍 **实时汇率查询** - 从多个API源获取最新汇率数据
- 📊 **智能路径分析** - 自动分析CNY→中间货币→USD的所有可能路径
- 🏆 **排行榜显示** - 按收益率排序显示最优兑换方案
- 💰 **收益计算** - 精确计算相比直接兑换的额外收益
- 🎨 **美观界面** - 彩色终端界面，支持中英双语
- ⚡ **缓存优化** - 智能缓存减少API调用次数

## 安装和使用 / Installation & Usage

### 1. 克隆项目 / Clone Repository
```bash
git clone <repository-url>
cd ExchangeRateRanking_py
```

### 2. 安装依赖 / Install Dependencies

#### 使用 UV (推荐) / Using UV (Recommended)
```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 同步依赖（自动创建虚拟环境）
uv sync
```

#### 使用 pip (传统方式) / Using pip (Legacy)
```bash
pip install -r requirements.txt
```

### 3. 配置API密钥 (可选) / Configure API Key (Optional)
```bash
cp .env.example .env
# 编辑 .env 文件，添加你的API密钥
# Edit .env file and add your API key
```

### 4. 运行程序 / Run Application

#### 使用 UV / Using UV
```bash
# 基本使用
uv run main.py
# 或使用短别名: uv run era

# 指定金额
uv run main.py --amount 50000

# 热门货币分析
uv run main.py --popular

# 全部货币分析
uv run main.py --all-currencies

# 指定中间货币
uv run main.py --currencies "EUR,GBP,JPY,KRW"

# 离线演示模式
uv run main.py --offline

# 调试模式
uv run main.py --debug
```

#### 使用 Python / Using Python
```bash
# 基本使用
python main.py

# 指定金额
python main.py --amount 50000

# 指定中间货币
python main.py --currencies "EUR,GBP,JPY,KRW"

# 调试模式
python main.py --debug
```

## 使用示例 / Usage Examples

```bash
# 分析10万人民币的最佳兑换路径 (UV)
uv run main.py --amount 100000

# 只分析欧元、英镑、日元作为中间货币 (UV)
uv run main.py --currencies "EUR,GBP,JPY"

# 热门货币快速分析 (UV)
uv run era --popular

# 离线演示模式 (UV)
uv run era --offline

# 交互式使用（推荐）
uv run era

# 传统Python方式
python main.py --amount 100000
python main.py --currencies "EUR,GBP,JPY"
python main.py
```

## 工作原理 / How It Works

1. **获取实时汇率** - 从exchangerate-api.com获取最新汇率数据
2. **计算转换路径** - 分析CNY→中间货币→USD的每条路径
3. **效率评分** - 计算相比直接兑换CNY→USD的收益率
4. **排序推荐** - 按收益率从高到低排序，推荐最优方案

## 支持的货币 / Supported Currencies

默认分析的中间货币包括：
- USD (美元) - EUR (欧元) - GBP (英镑) - JPY (日元)
- KRW (韩元) - HKD (港币) - SGD (新币) - AUD (澳元)
- CAD (加元) - CHF (瑞士法郎)

## 技术栈 / Tech Stack

- **Python 3.7+**
- **Rich** - 终端界面美化
- **Click** - 命令行界面
- **Requests** - HTTP请求
- **python-dotenv** - 环境变量管理

## API说明 / API Information

- 免费版本：无需API密钥，每月1500次请求
- 付费版本：需要API密钥，更高请求限制和更多功能
- 获取API密钥：https://exchangerate-api.com/

## 贡献 / Contributing

欢迎提交Issue和Pull Request！

## 许可证 / License

MIT License