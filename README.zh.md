# Content Heat Manager 内容热度管理器

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)]()

[English](README.md) | 中文文档

> 为信息聚合项目提供的综合内容热度和相关性评分系统

## 🎯 项目概述

Content Heat Manager 是一个智能评分系统，基于多维度对内容进行排名，包括时间新鲜度、平台影响力、主题相关度和跨平台传播度。它专为新闻聚合器、内容策展人、日报系统以及任何需要智能内容排名的系统设计。

## ✨ 核心特性

### 多维度热度评分

| 维度 | 权重 | 说明 |
|-----------|--------|-------------|
| **时间新鲜度** | 25% | 指数衰减（每小时5%） |
| **平台影响力** | 25% | 来源特定评分 |
| **主题相关度** | 30% | 带权重的关键词匹配 |
| **跨平台传播** | 20% | 多平台出现加分 |

### 主要功能

- 🔥 **自动时间衰减**：内容热度随时间自然降低
- 🎯 **智能过滤**：自动过滤无关内容
- 💾 **持久化缓存**：基于JSON的存储，支持增量更新
- 🌍 **多平台支持**：GitHub、HackerNews、Reddit、中文科技媒体
- 📊 **热度分布分析**：追踪内容表现
- ⏰ **定时任务就绪**：内置脚本支持定时更新

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/content-heat-manager.git
cd content-heat-manager

# 安装依赖（无需外部依赖！）
# 仅使用 Python 标准库
```

### 基本用法

```python
from content_heat_manager import HeatManager, get_heat_emoji

# 初始化
manager = HeatManager()

# 你的内容文章
articles = [
    {
        "title": "OpenAI完成110亿美元新一轮融资",
        "url": "https://techcrunch.com/openai-funding",
        "source": "TechCrunch",
        "published": "2026-03-02T14:00:00Z",
        "summary": "来自顶级投资人的大规模融资轮"
    }
]

# 计算热度分数
for article in articles:
    article['heat'] = manager.calculate_heat(article)

# 按热度排序
articles.sort(key=lambda x: x['heat']['total'], reverse=True)

# 显示结果
for article in articles:
    emoji = get_heat_emoji(article['heat']['total'])
    print(f"{emoji} [{article['heat']['total']}/10] {article['title']}")
```

### 输出示例

```
🔥🔥 [8.2/10] OpenAI完成110亿美元新一轮融资
🔥🔥 [7.8/10] Anthropic发布新AI模型
🔥 [6.5/10] NVIDIA宣布6G网络计划
```

## 📖 文档

### API 参考

详见 [references/api_reference.md](references/api_reference.md) 获取完整 API 文档。

### 配置

- **平台权重**：在 `references/platform_weights.json` 中自定义来源评分
- **主题关键词**：在 `references/topic_keywords.json` 中调整相关性关键词

### 自动化

通过 cron 设置每小时热度衰减更新：

```bash
# 添加到 crontab
0 * * * * cd /path/to/project && python3 scripts/update_heat_decay.py
```

## 📂 项目结构

```
content-heat-manager/
├── README.md                       # 英文文档
├── README.zh.md                    # 中文文档（本文件）
├── SKILL.md                        # OpenClaw skill 定义
├── scripts/
│   ├── content_heat_manager.py     # 核心 HeatManager 类
│   ├── generate_daily_report.py    # 日报生成示例
│   └── update_heat_decay.py        # 定时更新脚本
├── references/
│   ├── api_reference.md            # 完整 API 文档
│   ├── platform_weights.json       # 平台评分配置
│   └── topic_keywords.json         # 主题相关性配置
└── assets/                         # 资源目录（可选）
```

## 🎨 热度等级

| 分数 | 等级 | 表情 | 说明 |
|-------|-------|-------|-------------|
| 9-10 | 爆款 | 🔥🔥🔥 | 多平台热门 |
| 7-9 | 热门 | 🔥🔥 | 高相关度 + 近期发布 |
| 5-7 | 一般 | 🔥 | 中等关注度 |
| <5 | 冷门 | 💤 | 低参与度或已过时 |

## 💡 应用场景

- **AI新闻聚合**：按重要性排名AI/科技新闻
- **产品经理日报**：聚合行业新闻
- **投资监控**：追踪融资和市场新闻
- **技术团队周刊**：策划开发者聚焦内容
- **研究监控**：追踪学术和行业出版物

## 🔧 高级用法

### 自定义平台权重

```python
# 在 references/platform_weights.json 中
{
  "我的自定义来源": {
    "type": "static",
    "weight": 7.0
  }
}
```

### 自定义主题关键词

```python
# 在 references/topic_keywords.json 中
{
  "我的分类": {
    "weight": 3.0,
    "keywords": ["关键词1", "关键词2"]
  }
}
```

### 批量处理

```python
# 高效处理数千篇文章
manager = HeatManager(cache_file="large_cache.json")

# 文章自动缓存
for article in articles:
    heat = manager.calculate_heat(article)

# 获取前100名
top_articles = manager.get_top_articles(articles, n=100)

# 获取分布统计
stats = manager.get_heat_distribution()
```

## 🧪 测试

```bash
# 运行演示
python3 scripts/content_heat_manager.py

# 运行日报示例
python3 scripts/generate_daily_report.py
```

## 📦 OpenClaw Skill

本项目也打包为 OpenClaw skill：

```bash
# 作为 OpenClaw skill 安装
cp content-heat-manager.skill ~/.openclaw/skills/
```

然后在任何 OpenClaw 会话中使用：
```python
from content_heat_manager import HeatManager
manager = HeatManager()
```

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 仓库
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 灵感来自 [Horizon](https://github.com/thysrael/Horizon) 项目
- 为AI驱动的内容聚合工作流构建

## 📞 联系方式

- GitHub Issues: [https://github.com/yourusername/content-heat-manager/issues](https://github.com/yourusername/content-heat-manager/issues)
- 邮箱: your.email@example.com

---

用 ❤️ 打造，为更好的内容策展
