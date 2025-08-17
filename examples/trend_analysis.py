#!/usr/bin/env python3
"""
Research Trend Analysis Example

This example demonstrates how to analyze research trends over time using the arXiv search tool.
It shows publication patterns, identifies hot topics, and tracks the evolution of research areas.
"""

import sys
import os
sys.path.append('..')

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from arxiv_search import ArxivSearcher

def analyze_trends():
    """Analyze publication trends in machine learning over time"""
    
    searcher = ArxivSearcher()
    searcher.data_dir = "../meta-query-search/data"  # Fix path for examples
    
    # Load the existing data
    if not searcher.load_existing_data():
        print("No data found! Please run: ../arxiv search machine learning --save")
        return
    
    df = searcher.current_data
    
    print("=== Research Trend Analysis ===")
    print(f"Analyzing {len(df)} papers from {df['published'].min().year} to {df['published'].max().year}")
    
    # Extract year from publication date
    df['year'] = df['published'].dt.year
    
    # 1. Publications per year
    yearly_counts = df['year'].value_counts().sort_index()
    
    print("\n📊 Publications per Year:")
    for year, count in yearly_counts.tail(10).items():
        print(f"  {year}: {count} papers")
    
    # 2. Growth analysis
    recent_years = yearly_counts.last('10Y')  # Last 10 years
    growth_rate = ((recent_years.iloc[-1] - recent_years.iloc[0]) / recent_years.iloc[0]) * 100
    print(f"\n📈 Growth in last 10 years: {growth_rate:.1f}%")
    
    # 3. Hot topics by era
    print("\n🔥 Hot Topics by Era:")
    
    # Pre-2010: Classical ML
    classical = df[df['year'] < 2010]
    classical_words = extract_common_words(classical['title'])
    print("  Pre-2010 (Classical ML):", ', '.join(classical_words[:5]))
    
    # 2010-2020: Deep Learning Era
    deep_learning = df[(df['year'] >= 2010) & (df['year'] < 2020)]
    dl_words = extract_common_words(deep_learning['title'])
    print("  2010-2020 (Deep Learning Era):", ', '.join(dl_words[:5]))
    
    # 2020+: Modern AI Era
    modern = df[df['year'] >= 2020]
    modern_words = extract_common_words(modern['title'])
    print("  2020+ (Modern AI Era):", ', '.join(modern_words[:5]))
    
    # 4. Specific technique trends
    print("\n🤖 Technique Evolution:")
    techniques = ['neural', 'deep', 'transformer', 'attention', 'reinforcement', 'quantum']
    
    for technique in techniques:
        trend = analyze_technique_trend(df, technique)
        if trend['total'] > 0:
            print(f"  {technique.capitalize()}: {trend['total']} papers, peak in {trend['peak_year']}")
    
    # 5. Recent surge topics
    print("\n🚀 Recently Surging Topics (2022+):")
    recent_surge = df[df['year'] >= 2022]
    surge_topics = find_surge_topics(recent_surge)
    for topic, count in surge_topics.items():
        print(f"  {topic}: {count} papers")

def extract_common_words(titles):
    """Extract common meaningful words from titles"""
    import re
    from collections import Counter
    
    # Combine all titles and extract words
    text = ' '.join(titles.astype(str)).lower()
    words = re.findall(r'\b[a-z]{4,}\b', text)  # Words with 4+ letters
    
    # Filter out common stop words
    stop_words = {'with', 'using', 'based', 'from', 'this', 'that', 'they', 'were', 
                  'been', 'have', 'their', 'more', 'what', 'some', 'time', 'very', 
                  'when', 'much', 'should', 'these', 'other', 'into', 'after', 'first',
                  'machine', 'learning', 'data', 'model', 'models', 'approach', 'method'}
    
    meaningful_words = [word for word in words if word not in stop_words]
    
    return [word for word, count in Counter(meaningful_words).most_common(10)]

def analyze_technique_trend(df, technique):
    """Analyze the trend of a specific technique over time"""
    technique_papers = df[df['combined'].str.contains(technique, case=False, na=False)]
    
    if len(technique_papers) == 0:
        return {'total': 0, 'peak_year': 'N/A'}
    
    yearly = technique_papers['year'].value_counts().sort_index()
    peak_year = yearly.idxmax() if len(yearly) > 0 else 'N/A'
    
    return {
        'total': len(technique_papers),
        'peak_year': peak_year
    }

def find_surge_topics(recent_df):
    """Find topics that are surging in recent papers"""
    surge_keywords = ['gpt', 'llm', 'large language', 'diffusion', 'stable diffusion', 
                     'chatgpt', 'generative', 'multimodal', 'vision transformer']
    
    surge_counts = {}
    for keyword in surge_keywords:
        count = recent_df['combined'].str.contains(keyword, case=False, na=False).sum()
        if count > 0:
            surge_counts[keyword] = count
    
    return dict(sorted(surge_counts.items(), key=lambda x: x[1], reverse=True))

if __name__ == "__main__":
    analyze_trends()
