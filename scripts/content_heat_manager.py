#!/usr/bin/env python3
"""
Content Heat Manager - Core Module
Multi-dimensional content popularity scoring system
"""

import json
import os
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path


class HeatManager:
    """
    Content heat scoring manager
    
    Calculates multi-dimensional heat scores for content items:
    - Time freshness (25%): Exponential decay based on age
    - Platform authority (25%): Source-specific scoring
    - Topic relevance (30%): Keyword matching
    - Cross-platform buzz (20%): Multi-source appearance
    """
    
    DEFAULT_CACHE_FILE = "heat_cache.json"
    DEFAULT_DECAY_RATE = 0.95  # 5% per hour
    
    # Platform weight configurations
    PLATFORM_WEIGHTS = {
        # Tech platforms
        "GitHub": lambda metrics: min(10, 5 + metrics.get("stars", 0) / 1000),
        "HackerNews": lambda metrics: min(10, 5 + metrics.get("score", 0) / 50),
        "Reddit": lambda metrics: min(10, 5 + metrics.get("upvotes", 0) / 100),
        "ProductHunt": lambda metrics: min(10, 5 + metrics.get("votes", 0) / 50),
        
        # Chinese tech media
        "36氪": 6.0,
        "量子位": 6.5,
        "钛媒体": 5.5,
        "InfoQ": 6.0,
        "机器之心": 7.0,
        "掘金": 5.5,
        "知乎": 5.0,
        "CSDN": 4.5,
        
        # General tech media
        "TechCrunch": 6.5,
        "The Verge": 6.0,
        "Ars Technica": 6.5,
        "Wired": 5.5,
        
        # Default
        "default": 5.0
    }
    
    # Topic relevance keywords with weights
    TOPIC_KEYWORDS = {
        # AI/ML keywords (high weight)
        "openai": 3.0, "anthropic": 3.0, "claude": 3.0, "gpt": 3.0, "llm": 3.0,
        "人工智能": 3.0, "大模型": 3.0, "机器学习": 2.5, "深度学习": 2.5,
        
        # Business/funding keywords
        "融资": 2.5, "投资": 2.0, "亿美元": 2.0, "收购": 2.0, "ipo": 2.0,
        "startup": 2.0, "独角兽": 2.0, "估值": 1.5,
        
        # Product/release keywords
        "发布": 1.5, "上线": 1.5, "推出": 1.5, "新产品": 1.5,
        "release": 1.5, "launch": 1.5, "update": 1.0,
        
        # Impact keywords
        "突破": 2.0, "里程碑": 2.0, "革命": 2.0, "颠覆": 1.5,
        "breakthrough": 2.0, "milestone": 2.0, "revolutionary": 1.5,
        
        # Tech company leaders
        "黄仁勋": 1.5, "马斯克": 1.5, "sam altman": 1.5, "李彦宏": 1.5,
        "nvidia": 1.5, "tesla": 1.5, "google": 1.0, "microsoft": 1.0,
        
        # Tech concepts
        "agent": 1.5, "智能体": 1.5, "rag": 1.5, "向量": 1.0,
        "generative": 1.5, "生成式": 1.5, "multimodal": 1.5, "多模态": 1.5,
        "具身智能": 2.0, "embodied": 2.0, "机器人": 1.5, "robot": 1.5,
        
        # Negative keywords (reduce score)
        "租房": -2.0, "补贴": -2.0, "医药": -2.0, "医疗": -1.5,
        "减持": -1.5, "分红": -1.5, "股息": -1.5,
    }
    
    # Dimension weights for total score calculation
    DIMENSION_WEIGHTS = {
        "time": 0.25,
        "platform": 0.25,
        "relevance": 0.30,
        "cross_platform": 0.20
    }
    
    def __init__(self, cache_file: Optional[str] = None, decay_rate: float = None):
        """
        Initialize HeatManager
        
        Args:
            cache_file: Path to cache file (default: heat_cache.json)
            decay_rate: Hourly decay rate (default: 0.95 = 5% loss per hour)
        """
        self.cache_file = cache_file or self.DEFAULT_CACHE_FILE
        self.decay_rate = decay_rate or self.DEFAULT_DECAY_RATE
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load heat cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load cache: {e}")
        
        return {
            "articles": {},
            "last_update": datetime.now(timezone.utc).isoformat(),
            "version": "1.0"
        }
    
    def _save_cache(self):
        """Save heat cache to file"""
        try:
            os.makedirs(os.path.dirname(self.cache_file) or '.', exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Warning: Could not save cache: {e}")
    
    def _parse_time(self, time_str: str) -> Optional[datetime]:
        """Parse various time formats"""
        if not time_str:
            return None
        
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S%z',
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S GMT',
            '%Y-%m-%d',
        ]
        
        time_str = str(time_str).strip()
        
        for fmt in formats:
            try:
                dt = datetime.strptime(time_str, fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except ValueError:
                continue
        
        # Try ISO format
        try:
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            return dt
        except:
            pass
        
        return None
    
    def _calculate_time_score(self, published_time: str) -> float:
        """Calculate time-based freshness score"""
        pub_time = self._parse_time(published_time)
        if not pub_time:
            return 5.0  # Default middle score
        
        now = datetime.now(timezone.utc)
        hours_ago = (now - pub_time).total_seconds() / 3600
        
        # Exponential decay
        score = 10.0 * (self.decay_rate ** hours_ago)
        return max(score, 0.0)
    
    def _calculate_platform_score(self, source: str, metrics: Dict[str, Any]) -> float:
        """Calculate platform authority score"""
        weight = self.PLATFORM_WEIGHTS.get(source, self.PLATFORM_WEIGHTS["default"])
        
        if callable(weight):
            return weight(metrics)
        
        return float(weight)
    
    def _calculate_relevance_score(self, title: str, summary: str = "") -> float:
        """Calculate topic relevance score based on keywords"""
        text = (title + " " + summary).lower()
        
        score = 5.0  # Base score
        
        for keyword, weight in self.TOPIC_KEYWORDS.items():
            if keyword.lower() in text:
                score += weight
        
        return max(0.0, min(score, 10.0))
    
    def _calculate_cross_platform_score(self, url: str) -> float:
        """Calculate cross-platform buzz score"""
        # Check if this URL appears in cache (simulating multi-platform detection)
        # In real implementation, this would check for similar content across sources
        
        url_variants = [
            url,
            url.replace('https://', 'http://'),
            url.replace('www.', ''),
            url.rstrip('/'),
        ]
        
        count = sum(1 for variant in url_variants if variant in self.cache["articles"])
        
        if count >= 3:
            return 9.0
        elif count == 2:
            return 7.5
        else:
            return 5.0
    
    def calculate_heat(self, article: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate comprehensive heat score for an article
        
        Args:
            article: Dict with keys: title, url, source, published, summary (optional)
        
        Returns:
            Dict with total score and dimension breakdown
        """
        url = article.get("url", "")
        
        # Check cache first
        if url and url in self.cache["articles"]:
            cached = self.cache["articles"][url]
            # Update time decay only
            cached["time"] = round(
                self._calculate_time_score(article.get("published", "")), 1
            )
            # Recalculate total
            cached["total"] = round(
                cached["time"] * self.DIMENSION_WEIGHTS["time"] +
                cached["platform"] * self.DIMENSION_WEIGHTS["platform"] +
                cached["relevance"] * self.DIMENSION_WEIGHTS["relevance"] +
                cached["cross_platform"] * self.DIMENSION_WEIGHTS["cross_platform"],
                1
            )
            return cached
        
        # Calculate all dimensions
        time_score = self._calculate_time_score(article.get("published", ""))
        platform_score = self._calculate_platform_score(
            article.get("source", "default"),
            article
        )
        relevance_score = self._calculate_relevance_score(
            article.get("title", ""),
            article.get("summary", "")
        )
        cross_platform_score = self._calculate_cross_platform_score(url)
        
        # Calculate weighted total
        total = (
            time_score * self.DIMENSION_WEIGHTS["time"] +
            platform_score * self.DIMENSION_WEIGHTS["platform"] +
            relevance_score * self.DIMENSION_WEIGHTS["relevance"] +
            cross_platform_score * self.DIMENSION_WEIGHTS["cross_platform"]
        )
        
        heat_data = {
            "total": round(min(total, 10.0), 1),
            "time": round(time_score, 1),
            "platform": round(platform_score, 1),
            "relevance": round(relevance_score, 1),
            "cross_platform": round(cross_platform_score, 1),
            "calculated_at": datetime.now(timezone.utc).isoformat(),
            "url": url
        }
        
        # Cache the result
        if url:
            self.cache["articles"][url] = heat_data
            self._save_cache()
        
        return heat_data
    
    def get_or_calculate(self, article: Dict[str, Any]) -> Dict[str, float]:
        """Alias for calculate_heat with caching"""
        return self.calculate_heat(article)
    
    def update_time_decay(self):
        """Update time decay for all cached articles"""
        updated_count = 0
        
        for url, heat_data in self.cache["articles"].items():
            # Get original article data
            # In practice, you'd store this or recalculate
            # Here we just update the time component
            
            # Calculate new time score based on original publish time
            # This is a simplified version - in production you'd store pub_time
            new_time_score = heat_data["time"] * self.decay_rate
            
            heat_data["time"] = round(new_time_score, 1)
            heat_data["total"] = round(
                heat_data["time"] * self.DIMENSION_WEIGHTS["time"] +
                heat_data["platform"] * self.DIMENSION_WEIGHTS["platform"] +
                heat_data["relevance"] * self.DIMENSION_WEIGHTS["relevance"] +
                heat_data["cross_platform"] * self.DIMENSION_WEIGHTS["cross_platform"],
                1
            )
            updated_count += 1
        
        self.cache["last_update"] = datetime.now(timezone.utc).isoformat()
        self._save_cache()
        
        return updated_count
    
    def get_top_articles(self, articles: List[Dict], n: int = 10) -> List[Dict]:
        """Get top N articles by heat score"""
        # Calculate heat for all
        for article in articles:
            article["heat"] = self.calculate_heat(article)
        
        # Sort by total heat
        sorted_articles = sorted(
            articles,
            key=lambda x: x["heat"]["total"],
            reverse=True
        )
        
        return sorted_articles[:n]
    
    def filter_by_relevance(self, articles: List[Dict], min_score: float = 5.0) -> List[Dict]:
        """Filter articles by minimum relevance score"""
        filtered = []
        for article in articles:
            heat = self.calculate_heat(article)
            if heat["relevance"] >= min_score:
                article["heat"] = heat
                filtered.append(article)
        return filtered
    
    def filter_by_time(self, articles: List[Dict], hours: int = 24) -> List[Dict]:
        """Filter articles by time window"""
        filtered = []
        now = datetime.now(timezone.utc)
        
        for article in articles:
            pub_time = self._parse_time(article.get("published", ""))
            if pub_time:
                age_hours = (now - pub_time).total_seconds() / 3600
                if age_hours <= hours:
                    article["heat"] = self.calculate_heat(article)
                    filtered.append(article)
        
        return filtered
    
    def get_heat_distribution(self) -> Dict[str, Any]:
        """Get statistics about current heat distribution"""
        heats = [h["total"] for h in self.cache["articles"].values()]
        
        if not heats:
            return {"total": 0}
        
        return {
            "total_cached": len(heats),
            "avg_heat": round(sum(heats) / len(heats), 2),
            "max_heat": max(heats),
            "min_heat": min(heats),
            "viral_count": len([h for h in heats if h >= 9]),      # 🔥🔥🔥
            "hot_count": len([h for h in heats if 7 <= h < 9]),    # 🔥🔥
            "warm_count": len([h for h in heats if 5 <= h < 7]),   # 🔥
            "cold_count": len([h for h in heats if h < 5])         # 💤
        }
    
    def clear_cache(self):
        """Clear all cached heat data"""
        self.cache = {
            "articles": {},
            "last_update": datetime.now(timezone.utc).isoformat(),
            "version": "1.0"
        }
        self._save_cache()
    
    def export_to_json(self, filepath: str):
        """Export all cached data to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)


# Helper function to get emoji for heat level
def get_heat_emoji(score: float) -> str:
    """Get appropriate emoji for heat score"""
    if score >= 9:
        return "🔥🔥🔥"
    elif score >= 7:
        return "🔥🔥"
    elif score >= 5:
        return "🔥"
    else:
        return "💤"


def get_heat_color(score: float) -> str:
    """Get color code for heat score"""
    if score >= 9:
        return "#ff6b6b"  # Red
    elif score >= 7:
        return "#ffd93d"  # Yellow
    elif score >= 5:
        return "#6bcf7f"  # Green
    else:
        return "#8b949e"  # Gray


if __name__ == "__main__":
    # Demo
    manager = HeatManager()
    
    articles = [
        {
            "title": "OpenAI最新融资1100亿美元！英伟达亚马逊软银都抢到船票了",
            "url": "https://example.com/1",
            "source": "量子位",
            "published": "2026-03-02 03:50:45",
            "summary": "OpenAI融资消息"
        },
        {
            "title": "成都六类人才可享租房补贴",
            "url": "https://example.com/2",
            "source": "36氪",
            "published": "2026-03-02 16:21:42",
            "summary": "人才补贴政策"
        }
    ]
    
    print("="*60)
    print("🔥 Content Heat Manager Demo")
    print("="*60)
    
    for article in articles:
        heat = manager.calculate_heat(article)
        emoji = get_heat_emoji(heat["total"])
        
        print(f"\n📰 {article['title'][:40]}...")
        print(f"   Source: {article['source']}")
        print(f"   {emoji} Heat: {heat['total']}/10")
        print(f"   ├─ Time: {heat['time']}")
        print(f"   ├─ Platform: {heat['platform']}")
        print(f"   ├─ Relevance: {heat['relevance']}")
        print(f"   └─ Cross-Platform: {heat['cross_platform']}")
    
    # Filter low relevance
    print("\n" + "="*60)
    print("📊 After filtering (min relevance 5.0):")
    print("="*60)
    
    filtered = manager.filter_by_relevance(articles, min_score=5.0)
    for article in filtered:
        print(f"✅ {article['title'][:50]}... (relevance: {article['heat']['relevance']})")
