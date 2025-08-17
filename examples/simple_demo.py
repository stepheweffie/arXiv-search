#!/usr/bin/env python3
"""
Simple Demo of arXiv Search Analysis

A quick demonstration of what you can do with your arXiv dataset.
"""

import sys
sys.path.append('..')

import pandas as pd
from arxiv_search import ArxivSearcher

def main():
    print("🔬 arXiv Search Tool - Quick Demo")
    print("="*50)
    
    # Load the searcher and data
    searcher = ArxivSearcher()
    searcher.data_dir = "../meta-query-search/data"
    
    if not searcher.load_existing_data():
        print("❌ No data found! Please ensure you have run the main search.")
        return
    
    df = searcher.current_data
    
    print(f"✅ Loaded {len(df)} research papers!")
    print(f"📅 Date range: {df['published'].min().year} - {df['published'].max().year}")
    
    # Basic analysis
    print(f"\n📊 BASIC STATISTICS:")
    df['year'] = df['published'].dt.year
    recent_papers = df[df['year'] >= 2020]
    print(f"   Recent papers (2020+): {len(recent_papers)}")
    
    # Hot topics
    print(f"\n🔥 HOT TOPICS:")
    hot_terms = ['deep learning', 'transformer', 'neural network', 'reinforcement learning']
    for term in hot_terms:
        count = df['combined'].str.contains(term, case=False, na=False).sum()
        print(f"   {term.title()}: {count} papers")
    
    # Recent developments
    print(f"\n🚀 RECENT DEVELOPMENTS (2024-2025):")
    very_recent = df[df['year'] >= 2024]
    if len(very_recent) > 0:
        print(f"   Papers from 2024-2025: {len(very_recent)}")
        print("   Latest papers:")
        for _, paper in very_recent.sort_values('published', ascending=False).head(3).iterrows():
            print(f"   • {paper['title'][:60]}... ({paper['year']})")
    
    # Topic search examples
    print(f"\n🔍 SEARCH EXAMPLES:")
    
    # Example 1: Find transformer papers
    transformer_papers = df[df['combined'].str.contains('transformer', case=False, na=False)]
    print(f"   'Transformer' papers: {len(transformer_papers)}")
    if len(transformer_papers) > 0:
        latest = transformer_papers.sort_values('published', ascending=False).iloc[0]
        print(f"   Latest: {latest['title'][:50]}... ({latest['year']})")
    
    # Example 2: Find ethical AI papers
    ethics_papers = df[df['combined'].str.contains('ethical|fairness|bias', case=False, na=False)]
    print(f"   AI Ethics papers: {len(ethics_papers)}")
    
    # Example 3: Find quantum ML papers
    quantum_papers = df[df['combined'].str.contains('quantum.*machine learning|quantum.*neural', case=False, na=False)]
    print(f"   Quantum ML papers: {len(quantum_papers)}")
    
    print(f"\n✨ That's just a taste! Check out the other examples for advanced analysis.")
    print(f"💡 Try running: python research_workflows.py")

if __name__ == "__main__":
    main()
