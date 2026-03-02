#!/usr/bin/env python3
"""
Complete example: Multi-source content aggregation with heat scoring
Demonstrates the full workflow of the Content Heat Manager skill
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from content_heat_manager import HeatManager, get_heat_emoji
from datetime import datetime, timedelta, timezone


def generate_daily_report():
    """
    Example: Generate a daily report from multiple sources
    This demonstrates the complete workflow
    """
    
    # Initialize heat manager
    manager = HeatManager(cache_file="daily_report_cache.json")
    
    # Simulate fetched articles from multiple sources
    from datetime import timezone
    now = datetime.now(timezone.utc)
    
    raw_articles = [
        # HackerNews (high engagement)
        {
            "title": "Anthropic AI reportedly used for Iran airstrike intelligence analysis",
            "url": "https://news.ycombinator.com/item?id=43234567",
            "source": "HackerNews",
            "published": (now - timedelta(hours=8)).isoformat(),
            "summary": "US military reportedly used Claude AI for target identification",
            "score": 850,  # HN upvotes
        },
        
        # GitHub (developer interest)
        {
            "title": "OpenAI Python SDK v1.12.0 released with new features",
            "url": "https://github.com/openai/openai-python/releases/tag/v1.12.0",
            "source": "GitHub",
            "published": (now - timedelta(hours=2)).isoformat(),
            "summary": "New streaming support and improved error handling",
            "stars": 2500,
        },
        
        # Chinese tech media
        {
            "title": "OpenAI最新融资1100亿美元！英伟达亚马逊软银都抢到船票了",
            "url": "https://www.qbitai.com/2026/03/openai-funding",
            "source": "量子位",
            "published": (now - timedelta(hours=3)).isoformat(),
            "summary": "OpenAI完成新一轮融资，估值大幅提升",
        },
        
        {
            "title": "成都六类人才可享租房补贴",
            "url": "https://36kr.com/newsflashes/3705724711743617",
            "source": "36氪",
            "published": (now - timedelta(hours=4)).isoformat(),
            "summary": "成都发布人才租房补贴政策",
        },
        
        # Product launch
        {
            "title": "NVIDIA announces AI-native 6G network with global telcos",
            "url": "https://nvidianews.nvidia.com/news/6g-ai-network",
            "source": "TechCrunch",
            "published": (now - timedelta(hours=6)).isoformat(),
            "summary": "Partnership with SoftBank, T-Mobile for 6G infrastructure",
        },
    ]
    
    print("="*70)
    print("📰 Daily Report Generation with Content Heat Manager")
    print("="*70)
    
    # Step 1: Filter by time (last 24 hours)
    print("\n🕐 Step 1: Filtering articles by time window...")
    recent_articles = manager.filter_by_time(raw_articles, hours=24)
    print(f"   ✅ {len(recent_articles)} articles within 24 hours")
    
    # Step 2: Filter by relevance (remove off-topic)
    print("\n🔍 Step 2: Filtering by AI/tech relevance...")
    relevant_articles = manager.filter_by_relevance(recent_articles, min_score=4.0)
    print(f"   ✅ {len(relevant_articles)} articles pass relevance filter")
    
    # Step 3: Calculate heat scores
    print("\n🔥 Step 3: Calculating heat scores...")
    for article in relevant_articles:
        article["heat"] = manager.calculate_heat(article)
    
    # Step 4: Sort by heat
    print("\n📊 Step 4: Sorting by total heat score...")
    sorted_articles = sorted(
        relevant_articles,
        key=lambda x: x["heat"]["total"],
        reverse=True
    )
    
    # Step 5: Display results
    print("\n" + "="*70)
    print("📋 TOP ARTICLES (Ranked by Heat)")
    print("="*70)
    
    for i, article in enumerate(sorted_articles[:5], 1):
        heat = article["heat"]
        emoji = get_heat_emoji(heat["total"])
        
        print(f"\n{i}. {emoji} [{heat['total']}/10] {article['title'][:60]}...")
        print(f"   Source: {article['source']} | Published: {article['published'][:16]}")
        print(f"   Heat breakdown:")
        print(f"   • Time Freshness: {heat['time']}")
        print(f"   • Platform Authority: {heat['platform']}")
        print(f"   • Topic Relevance: {heat['relevance']}")
        print(f"   • Cross-Platform: {heat['cross_platform']}")
    
    # Step 6: Show statistics
    print("\n" + "="*70)
    print("📈 Heat Distribution")
    print("="*70)
    
    stats = manager.get_heat_distribution()
    print(f"Total cached: {stats.get('total_cached', 0)}")
    print(f"Average heat: {stats.get('avg_heat', 0)}")
    print(f"🔥🔥🔥 Viral (9-10): {stats.get('viral_count', 0)}")
    print(f"🔥🔥 Hot (7-9): {stats.get('hot_count', 0)}")
    print(f"🔥 Warm (5-7): {stats.get('warm_count', 0)}")
    print(f"💤 Cold (<5): {stats.get('cold_count', 0)}")
    
    # Step 7: Export for further use
    print("\n💾 Cache saved to: daily_report_cache.json")
    
    return sorted_articles


if __name__ == "__main__":
    articles = generate_daily_report()
    
    print("\n" + "="*70)
    print("✅ Daily report generation complete!")
    print("="*70)
