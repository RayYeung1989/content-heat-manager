# Content Heat Manager

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)]()

[中文文档](README.zh.md) | English

> A comprehensive content popularity and relevance scoring system for information aggregation projects.

## 🎯 Overview

Content Heat Manager is an intelligent scoring system that ranks content based on multiple dimensions including time freshness, platform authority, topic relevance, and cross-platform buzz. It's designed for news aggregators, content curators, daily reports, and any system that needs intelligent content ranking.

## ✨ Features

### Multi-Dimensional Heat Scoring

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Time Freshness** | 25% | Exponential decay (5% per hour) |
| **Platform Authority** | 25% | Source-specific scoring |
| **Topic Relevance** | 30% | Keyword matching with weights |
| **Cross-Platform Buzz** | 20% | Multi-source appearance bonus |

### Key Capabilities

- 🔥 **Automatic Time Decay**: Content loses heat naturally over time
- 🎯 **Smart Filtering**: Remove off-topic content automatically
- 💾 **Persistent Caching**: JSON-based storage with incremental updates
- 🌍 **Multi-Platform Support**: GitHub, HackerNews, Reddit, Chinese tech media
- 📊 **Heat Distribution Analytics**: Track content performance
- ⏰ **Cron-Ready**: Built-in scripts for scheduled updates

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/content-heat-manager.git
cd content-heat-manager

# Install dependencies (no external dependencies required!)
# Uses only Python standard library
```

### Basic Usage

```python
from content_heat_manager import HeatManager, get_heat_emoji

# Initialize
manager = HeatManager()

# Your content articles
articles = [
    {
        "title": "OpenAI Raises $11B in New Funding",
        "url": "https://techcrunch.com/openai-funding",
        "source": "TechCrunch",
        "published": "2026-03-02T14:00:00Z",
        "summary": "Major funding round from top investors"
    }
]

# Calculate heat scores
for article in articles:
    article['heat'] = manager.calculate_heat(article)

# Sort by heat
articles.sort(key=lambda x: x['heat']['total'], reverse=True)

# Display results
for article in articles:
    emoji = get_heat_emoji(article['heat']['total'])
    print(f"{emoji} [{article['heat']['total']}/10] {article['title']}")
```

### Output Example

```
🔥🔥 [8.2/10] OpenAI Raises $11B in New Funding
🔥🔥 [7.8/10] Anthropic Releases New AI Model
🔥 [6.5/10] NVIDIA Announces 6G Network
```

## 📖 Documentation

### API Reference

See [references/api_reference.md](references/api_reference.md) for detailed API documentation.

### Configuration

- **Platform Weights**: Customize source scoring in `references/platform_weights.json`
- **Topic Keywords**: Adjust relevance keywords in `references/topic_keywords.json`

### Automation

Set up hourly heat decay updates via cron:

```bash
# Add to crontab
0 * * * * cd /path/to/project && python3 scripts/update_heat_decay.py
```

## 📂 Project Structure

```
content-heat-manager/
├── README.md                       # This file
├── README.zh.md                    # Chinese documentation
├── SKILL.md                        # OpenClaw skill definition
├── scripts/
│   ├── content_heat_manager.py     # Core HeatManager class
│   ├── generate_daily_report.py    # Daily report example
│   └── update_heat_decay.py        # Cron script for updates
├── references/
│   ├── api_reference.md            # Complete API documentation
│   ├── platform_weights.json       # Platform scoring config
│   └── topic_keywords.json         # Topic relevance config
└── assets/                         # Assets directory (optional)
```

## 🎨 Heat Levels

| Score | Level | Emoji | Description |
|-------|-------|-------|-------------|
| 9-10 | Viral | 🔥🔥🔥 | Hot across multiple platforms |
| 7-9 | Hot | 🔥🔥 | High relevance + recent publish |
| 5-7 | Warm | 🔥 | Moderate interest |
| <5 | Cold | 💤 | Low engagement or outdated |

## 💡 Use Cases

- **AI News Aggregation**: Rank AI/tech news by importance
- **Product Manager Daily Reports**: Aggregate industry news
- **Investment Monitoring**: Track funding and market news
- **Tech Team Newsletters**: Curate developer-focused content
- **Research Monitoring**: Track academic and industry publications

## 🔧 Advanced Usage

### Custom Platform Weights

```python
# In references/platform_weights.json
{
  "MyCustomSource": {
    "type": "static",
    "weight": 7.0
  }
}
```

### Custom Topic Keywords

```python
# In references/topic_keywords.json
{
  "my_category": {
    "weight": 3.0,
    "keywords": ["keyword1", "keyword2"]
  }
}
```

### Batch Processing

```python
# Process thousands of articles efficiently
manager = HeatManager(cache_file="large_cache.json")

# Articles are automatically cached
for article in articles:
    heat = manager.calculate_heat(article)

# Get top 100
top_articles = manager.get_top_articles(articles, n=100)

# Get distribution stats
stats = manager.get_heat_distribution()
```

## 🧪 Testing

```bash
# Run the demo
python3 scripts/content_heat_manager.py

# Run the daily report example
python3 scripts/generate_daily_report.py
```

## 📦 OpenClaw Skill

This project is also packaged as an OpenClaw skill. To install it for the **main OpenClaw agent** (not the dev workspace):

```bash
# Install to the main OpenClaw agent's skills directory
cp content-heat-manager.skill ~/.openclaw/skills/
```

Then the main agent can use it in any session:
```python
from content_heat_manager import HeatManager
manager = HeatManager()
```

**Note**: This installs the skill to your main OpenClaw workspace (`~/.openclaw/skills/`), making it available to the primary agent for all tasks.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the [Horizon](https://github.com/thysrael/Horizon) project
- Built for AI-powered content aggregation workflows

## 📞 Contact

- GitHub Issues: [https://github.com/yourusername/content-heat-manager/issues](https://github.com/yourusername/content-heat-manager/issues)
- Email: your.email@example.com

---

Made with ❤️ for better content curation
