---
name: content-heat-manager
description: Content popularity and relevance scoring system for information aggregation projects. Use when building news aggregators, content curators, daily reports, or any system that needs to rank/sort articles by importance, freshness, and relevance. Supports multi-dimensional scoring (time decay, platform authority, topic relevance, cross-platform buzz), automatic heat decay, and persistent caching. Ideal for AI news aggregation, tech monitoring, investment research, and content recommendation systems.
---

# Content Heat Manager

A comprehensive content popularity and relevance scoring system for information aggregation projects.

## When to Use

Use this skill when you need to:
- Build a news aggregator with intelligent ranking
- Create daily/weekly reports from multiple sources
- Filter and sort content by importance
- Implement time-decay based freshness scoring
- Calculate cross-platform content buzz

## Features

### 1. Multi-Dimensional Heat Scoring

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Time Freshness** | 25% | Exponential decay (5% per hour) |
| **Platform Authority** | 25% | Source-specific scoring |
| **Topic Relevance** | 30% | Keyword matching with weights |
| **Cross-Platform Buzz** | 20% | Multi-source appearance bonus |

### 2. Automatic Time Decay

Content loses heat over time:
- Formula: `heat = initial × 0.95^hours`
- Updated automatically via cron
- Ensures fresh content ranks higher

### 3. Content Filtering

- **AI/Topic Relevance Filter**: Remove off-topic content
- **Time Window Filter**: Keep only recent content (configurable)
- **Heat Threshold**: Filter low-engagement content

### 4. Persistent Caching

- Heat scores cached in JSON
- Survives restarts
- Incremental updates

## Quick Start

```python
from content_heat_manager import HeatManager

# Initialize
manager = HeatManager(cache_file="my_heat_cache.json")

# Define your articles
articles = [
    {
        "title": "OpenAI Raises $11B",
        "url": "https://example.com/1",
        "source": "TechCrunch",
        "published": "2026-03-02 14:00:00",
        "summary": "OpenAI funding news"
    }
]

# Calculate heat and sort
for article in articles:
    article['heat'] = manager.calculate_heat(article)

articles.sort(key=lambda x: x['heat']['total'], reverse=True)
```

## Article Format

```python
{
    "title": "Article title (required)",
    "url": "Unique identifier (required)",
    "source": "Source name (required)",
    "published": "ISO timestamp (required)",
    "summary": "Content summary (optional)",
    # Platform-specific metrics (optional)
    "upvotes": 100,
    "comments": 50,
    "shares": 25
}
```

## Heat Levels

| Score | Level | Emoji | Description |
|-------|-------|-------|-------------|
| 9-10 | Viral | 🔥🔥🔥 | Hot across platforms |
| 7-9 | Hot | 🔥🔥 | High relevance + recent |
| 5-7 | Warm | 🔥 | Moderate interest |
| <5 | Cold | 💤 | Low engagement |

## Automation

### Hourly Heat Decay Update

Add to crontab:
```bash
0 * * * * cd /your/project && python3 update_heat_decay.py
```

### Daily Report Generation

See `scripts/generate_heat_report.py` for complete example.

## Customization

### Custom Platform Scoring

Edit `references/platform_weights.json` to customize source weights.

### Custom Topic Keywords

Edit `references/topic_keywords.json` to adjust relevance scoring.

## API Reference

See `references/api_reference.md` for detailed API documentation.

## Examples

- `examples/news_aggregator.py` - Basic news aggregation
- `examples/daily_report.py` - Generate ranked daily reports
- `examples/multi_source.py` - Aggregate from multiple platforms
