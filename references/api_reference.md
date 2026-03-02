# Content Heat Manager - API Reference

## Core Class: HeatManager

### Initialization

```python
from content_heat_manager import HeatManager

# Default configuration
manager = HeatManager()

# Custom configuration
manager = HeatManager(
    cache_file="my_cache.json",  # Custom cache location
    decay_rate=0.95               # 5% hourly decay
)
```

### Methods

#### calculate_heat(article)
Calculate comprehensive heat score for an article.

**Parameters:**
- `article` (dict): Article data with required keys:
  - `title` (str): Article title
  - `url` (str): Unique URL identifier
  - `source` (str): Source platform name
  - `published` (str): ISO timestamp
  - `summary` (str, optional): Content summary
  - Platform-specific metrics (optional):
    - `stars` (int): For GitHub
    - `score` (int): For HackerNews
    - `upvotes` (int): For Reddit

**Returns:**
```python
{
    "total": 7.5,           # Overall heat score (0-10)
    "time": 8.0,            # Time freshness score
    "platform": 6.0,        # Platform authority score
    "relevance": 9.0,       # Topic relevance score
    "cross_platform": 5.0,  # Cross-platform buzz score
    "calculated_at": "...", # ISO timestamp
    "url": "..."
}
```

**Example:**
```python
article = {
    "title": "OpenAI Raises $11B",
    "url": "https://example.com/1",
    "source": "TechCrunch",
    "published": "2026-03-02T14:00:00Z",
    "summary": "Major funding round announced"
}

heat = manager.calculate_heat(article)
print(f"Heat score: {heat['total']}/10")
```

#### get_or_calculate(article)
Alias for `calculate_heat()`. Checks cache first, calculates if not cached.

#### get_top_articles(articles, n=10)
Get top N articles sorted by heat score.

**Parameters:**
- `articles` (list): List of article dicts
- `n` (int): Number of top articles to return

**Returns:**
List of articles with added `heat` key.

**Example:**
```python
top_10 = manager.get_top_articles(all_articles, n=10)
for article in top_10:
    print(f"{article['heat']['total']}: {article['title']}")
```

#### filter_by_relevance(articles, min_score=5.0)
Filter articles by minimum relevance score.

**Use case:** Remove off-topic content before ranking.

**Example:**
```python
# Keep only AI/tech relevant articles
filtered = manager.filter_by_relevance(articles, min_score=4.0)
```

#### filter_by_time(articles, hours=24)
Filter articles by time window.

**Use case:** Keep only recent content.

**Example:**
```python
# Keep only last 24 hours
recent = manager.filter_by_time(articles, hours=24)
```

#### update_time_decay()
Apply time decay to all cached articles.

**Use case:** Run hourly via cron to keep scores fresh.

**Returns:** Number of updated articles.

**Example:**
```python
updated = manager.update_time_decay()
print(f"Updated {updated} articles")
```

#### get_heat_distribution()
Get statistics about current heat distribution.

**Returns:**
```python
{
    "total_cached": 100,
    "avg_heat": 6.5,
    "max_heat": 9.8,
    "min_heat": 3.2,
    "viral_count": 5,    # >= 9
    "hot_count": 25,     # 7-9
    "warm_count": 50,    # 5-7
    "cold_count": 20     # < 5
}
```

#### clear_cache()
Clear all cached heat data.

#### export_to_json(filepath)
Export cache to JSON file.

### Helper Functions

#### get_heat_emoji(score)
Get emoji representation of heat level.

```python
from content_heat_manager import get_heat_emoji

emoji = get_heat_emoji(8.5)  # Returns "🔥🔥"
```

| Score | Emoji | Level |
|-------|-------|-------|
| >= 9 | 🔥🔥🔥 | Viral |
| 7-9 | 🔥🔥 | Hot |
| 5-7 | 🔥 | Warm |
| < 5 | 💤 | Cold |

#### get_heat_color(score)
Get hex color code for heat score.

```python
from content_heat_manager import get_heat_color

color = get_heat_color(8.5)  # Returns "#ffd93d" (yellow)
```

| Score | Color |
|-------|-------|
| >= 9 | #ff6b6b (red) |
| 7-9 | #ffd93d (yellow) |
| 5-7 | #6bcf7f (green) |
| < 5 | #8b949e (gray) |

## Configuration Files

### Platform Weights

Customize source scoring in `references/platform_weights.json`:

```json
{
  "MyCustomSource": {
    "type": "static",
    "weight": 6.0
  }
}
```

### Topic Keywords

Customize relevance keywords in `references/topic_keywords.json`:

```json
{
  "my_category": {
    "weight": 2.5,
    "keywords": ["keyword1", "keyword2"]
  }
}
```

## Complete Workflow Example

```python
from content_heat_manager import HeatManager

# 1. Initialize
manager = HeatManager()

# 2. Fetch articles (your own fetch logic)
articles = fetch_from_multiple_sources()

# 3. Filter by time (last 24h)
recent = manager.filter_by_time(articles, hours=24)

# 4. Filter by relevance
relevant = manager.filter_by_relevance(recent, min_score=4.0)

# 5. Calculate heat and sort
for article in relevant:
    article['heat'] = manager.calculate_heat(article)

sorted_articles = sorted(relevant, key=lambda x: x['heat']['total'], reverse=True)

# 6. Take top 10
top_10 = sorted_articles[:10]

# 7. Display
for article in top_10:
    print(f"[{article['heat']['total']}] {article['title']}")

# 8. Setup hourly decay update (in production)
# crontab: 0 * * * * python3 update_heat_decay.py
```

## Cron Setup

### Hourly Heat Decay Update

Add to crontab:
```bash
0 * * * * cd /path/to/project && python3 /path/to/content-heat-manager/scripts/update_heat_decay.py >> /var/log/heat_decay.log 2>&1
```

### Daily Report Generation

```bash
0 7 * * * cd /path/to/project && python3 /path/to/content-heat-manager/scripts/generate_daily_report.py >> /var/log/daily_report.log 2>&1
```

## Error Handling

All methods handle errors gracefully:
- Missing fields default to sensible values
- Invalid timestamps default to current time
- File I/O errors print warnings but don't crash

## Performance Notes

- First calculation for a URL takes ~1ms
- Cached results are instant (dictionary lookup)
- Cache file auto-saves on each calculation
- Suitable for thousands of articles

## Best Practices

1. **Always use URL as unique identifier** - ensures proper caching
2. **Set up hourly decay updates** - keeps scores fresh
3. **Filter before calculating** - reduces unnecessary computation
4. **Customize platform weights** - for your specific sources
5. **Adjust topic keywords** - for your domain
