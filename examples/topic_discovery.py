#!/usr/bin/env python3
"""
Topic Discovery and Analysis Example

This example shows how to discover research topics, analyze their relationships,
and identify emerging areas in machine learning research.
"""

import sys
sys.path.append('..')

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import re
from arxiv_search import ArxivSearcher

def discover_topics():
    """Discover and analyze research topics from the paper collection"""
    
    searcher = ArxivSearcher()
    searcher.data_dir = "../meta-query-search/data"  # Fix path for examples
    
    if not searcher.load_existing_data():
        print("No data found! Please run: ../arxiv search machine learning --save")
        return
    
    df = searcher.current_data
    
    print("=== Topic Discovery Analysis ===")
    print(f"Analyzing {len(df)} papers for topic patterns")
    
    # 1. Extract key terms from titles and abstracts
    print("\n🔍 Extracting Key Terms...")
    key_terms = extract_key_terms(df)
    
    # 2. Identify topic clusters
    print("\n🎯 Identifying Topic Clusters...")
    topic_clusters = identify_topic_clusters(df, key_terms)
    
    # 3. Analyze topic evolution over time
    print("\n📈 Topic Evolution Over Time...")
    df['year'] = df['published'].dt.year
    topic_evolution = analyze_topic_evolution(df, topic_clusters)
    
    # 4. Find emerging topics (hot in recent years)
    print("\n🚀 Emerging Topics (High Growth 2020+)...")
    emerging_topics = find_emerging_topics(df, topic_clusters)
    
    # 5. Topic co-occurrence analysis
    print("\n🔗 Topic Co-occurrence Analysis...")
    topic_cooccurrence = analyze_topic_cooccurrence(df, topic_clusters)
    
    # 6. Generate research recommendations
    print("\n💡 Research Recommendations...")
    recommendations = generate_recommendations(topic_clusters, emerging_topics, topic_cooccurrence)
    
    return {
        'key_terms': key_terms,
        'topic_clusters': topic_clusters,
        'topic_evolution': topic_evolution,
        'emerging_topics': emerging_topics,
        'cooccurrence': topic_cooccurrence,
        'recommendations': recommendations
    }

def extract_key_terms(df, top_n=100):
    """Extract key terms from titles and abstracts"""
    # Combine titles and abstracts
    text_data = (df['title'] + ' ' + df['abstract']).fillna('')
    
    # Clean and tokenize
    all_text = ' '.join(text_data).lower()
    
    # Extract meaningful terms (2-4 words)
    patterns = [
        r'\b[a-z]+\s+(?:learning|network|model|algorithm|method|system|analysis|detection|classification|recognition|optimization|prediction|generation)\b',
        r'\b(?:deep|machine|reinforcement|supervised|unsupervised|neural|convolutional|recurrent|transformer|attention)\s+[a-z]+\b',
        r'\b[a-z]+\s+(?:vision|processing|intelligence|computing|science|technology)\b'
    ]
    
    key_terms = []
    for pattern in patterns:
        matches = re.findall(pattern, all_text)
        key_terms.extend(matches)
    
    # Count and filter
    term_counts = Counter(key_terms)
    
    # Filter out too common or too rare terms
    filtered_terms = {term: count for term, count in term_counts.items() 
                     if count >= 5 and count <= len(df) * 0.1}
    
    return dict(sorted(filtered_terms.items(), key=lambda x: x[1], reverse=True)[:top_n])

def identify_topic_clusters(df, key_terms):
    """Identify topic clusters based on key terms"""
    
    # Define topic clusters based on common research areas
    topic_clusters = {
        'Deep Learning': ['deep learning', 'neural network', 'deep neural', 'convolutional neural', 
                         'recurrent neural', 'deep model', 'neural architecture'],
        
        'Computer Vision': ['computer vision', 'image processing', 'object detection', 'image recognition',
                           'visual', 'image classification', 'face recognition', 'image analysis'],
        
        'Natural Language Processing': ['natural language', 'text processing', 'language model', 
                                      'text classification', 'sentiment analysis', 'text mining',
                                      'text generation', 'machine translation'],
        
        'Reinforcement Learning': ['reinforcement learning', 'reward', 'policy', 'agent', 
                                  'markov decision', 'q learning', 'policy gradient'],
        
        'Optimization': ['optimization', 'genetic algorithm', 'evolutionary', 'gradient descent',
                        'parameter optimization', 'hyperparameter', 'loss function'],
        
        'Probabilistic Models': ['bayesian', 'probability', 'probabilistic', 'stochastic',
                               'gaussian', 'monte carlo', 'markov', 'random'],
        
        'Clustering & Classification': ['clustering', 'classification', 'supervised learning',
                                      'unsupervised learning', 'semi supervised', 'support vector'],
        
        'Time Series & Forecasting': ['time series', 'forecasting', 'prediction', 'temporal',
                                     'sequential', 'lstm', 'recurrent'],
        
        'Generative Models': ['generative', 'autoencoder', 'variational', 'gan', 'generative adversarial',
                             'diffusion', 'generation'],
        
        'Ethics & Explainability': ['ethical', 'fairness', 'bias', 'explainable', 'interpretable',
                                  'transparency', 'accountability', 'responsible ai']
    }
    
    # Count papers for each topic cluster
    topic_counts = {}
    for topic, keywords in topic_clusters.items():
        count = 0
        for keyword in keywords:
            count += df['combined'].str.contains(keyword, case=False, na=False).sum()
        topic_counts[topic] = count
    
    return dict(sorted(topic_counts.items(), key=lambda x: x[1], reverse=True))

def analyze_topic_evolution(df, topic_clusters):
    """Analyze how topics have evolved over time"""
    evolution = {}
    
    for topic in topic_clusters.keys():
        yearly_counts = defaultdict(int)
        
        # Get papers for this topic
        topic_keywords = get_topic_keywords(topic)
        topic_mask = df['combined'].str.contains('|'.join(topic_keywords), case=False, na=False)
        topic_papers = df[topic_mask]
        
        # Count by year
        if len(topic_papers) > 0:
            yearly = topic_papers['year'].value_counts().sort_index()
            evolution[topic] = {
                'total_papers': len(topic_papers),
                'first_year': yearly.index.min() if len(yearly) > 0 else None,
                'peak_year': yearly.idxmax() if len(yearly) > 0 else None,
                'recent_trend': calculate_trend(yearly.tail(5)) if len(yearly) >= 5 else 'insufficient_data'
            }
    
    # Sort by recent activity
    sorted_evolution = dict(sorted(evolution.items(), key=lambda x: x[1]['total_papers'], reverse=True))
    
    for topic, data in list(sorted_evolution.items())[:10]:
        print(f"  {topic}: {data['total_papers']} papers, peak in {data['peak_year']}, trend: {data['recent_trend']}")
    
    return sorted_evolution

def find_emerging_topics(df, topic_clusters):
    """Find topics that are emerging (growing rapidly in recent years)"""
    recent_years = df[df['year'] >= 2020]
    older_years = df[df['year'] < 2020]
    
    emerging = {}
    
    for topic in topic_clusters.keys():
        keywords = get_topic_keywords(topic)
        
        # Count in recent vs older periods
        recent_count = recent_years['combined'].str.contains('|'.join(keywords), case=False, na=False).sum()
        older_count = older_years['combined'].str.contains('|'.join(keywords), case=False, na=False).sum()
        
        if older_count > 0:
            growth_rate = (recent_count - older_count) / older_count
            if growth_rate > 0.5 and recent_count >= 5:  # At least 50% growth and 5+ recent papers
                emerging[topic] = {
                    'growth_rate': growth_rate,
                    'recent_papers': recent_count,
                    'older_papers': older_count
                }
    
    # Sort by growth rate
    sorted_emerging = dict(sorted(emerging.items(), key=lambda x: x[1]['growth_rate'], reverse=True))
    
    for topic, data in list(sorted_emerging.items())[:5]:
        print(f"  {topic}: {data['growth_rate']:.1%} growth ({data['older_papers']} → {data['recent_papers']} papers)")
    
    return sorted_emerging

def analyze_topic_cooccurrence(df, topic_clusters):
    """Analyze which topics frequently appear together"""
    cooccurrence = defaultdict(lambda: defaultdict(int))
    
    # For each paper, check which topics it belongs to
    for _, paper in df.iterrows():
        paper_topics = []
        for topic in topic_clusters.keys():
            keywords = get_topic_keywords(topic)
            if any(keyword in paper['combined'].lower() for keyword in keywords):
                paper_topics.append(topic)
        
        # Record co-occurrences
        for i, topic1 in enumerate(paper_topics):
            for topic2 in paper_topics[i+1:]:
                cooccurrence[topic1][topic2] += 1
                cooccurrence[topic2][topic1] += 1
    
    # Find strongest connections
    strong_connections = []
    for topic1, connections in cooccurrence.items():
        for topic2, count in connections.items():
            if count >= 5:  # At least 5 co-occurrences
                strong_connections.append((topic1, topic2, count))
    
    strong_connections.sort(key=lambda x: x[2], reverse=True)
    
    print("  Top Topic Combinations:")
    for topic1, topic2, count in strong_connections[:8]:
        print(f"    {topic1} + {topic2}: {count} papers")
    
    return dict(cooccurrence)

def generate_recommendations(topic_clusters, emerging_topics, cooccurrence):
    """Generate research recommendations based on the analysis"""
    recommendations = []
    
    # 1. Emerging areas to explore
    if emerging_topics:
        top_emerging = list(emerging_topics.keys())[:3]
        recommendations.append(f"🔥 Hot emerging areas: {', '.join(top_emerging)}")
    
    # 2. Interdisciplinary opportunities
    top_combinations = []
    for topic1, connections in cooccurrence.items():
        for topic2, count in connections.items():
            if count >= 10:
                top_combinations.append((topic1, topic2, count))
    
    top_combinations.sort(key=lambda x: x[2], reverse=True)
    if top_combinations:
        combo = top_combinations[0]
        recommendations.append(f"🔗 Strong interdisciplinary area: {combo[0]} + {combo[1]} ({combo[2]} papers)")
    
    # 3. Underexplored combinations
    underexplored = []
    for topic1 in list(topic_clusters.keys())[:5]:
        for topic2 in list(topic_clusters.keys())[:5]:
            if topic1 != topic2:
                combo_count = cooccurrence.get(topic1, {}).get(topic2, 0)
                if combo_count < 3:  # Very few papers combining these
                    underexplored.append((topic1, topic2))
    
    if underexplored:
        combo = underexplored[0]
        recommendations.append(f"💡 Potential research gap: {combo[0]} + {combo[1]} (underexplored combination)")
    
    print("  Research Suggestions:")
    for rec in recommendations:
        print(f"    {rec}")
    
    return recommendations

def get_topic_keywords(topic):
    """Get keywords for a specific topic"""
    topic_keywords = {
        'Deep Learning': ['deep learning', 'neural network', 'deep neural'],
        'Computer Vision': ['computer vision', 'image', 'visual', 'object detection'],
        'Natural Language Processing': ['natural language', 'text', 'nlp'],
        'Reinforcement Learning': ['reinforcement learning', 'reward', 'agent'],
        'Optimization': ['optimization', 'genetic algorithm'],
        'Probabilistic Models': ['bayesian', 'probability', 'probabilistic'],
        'Clustering & Classification': ['clustering', 'classification'],
        'Time Series & Forecasting': ['time series', 'forecasting', 'temporal'],
        'Generative Models': ['generative', 'autoencoder', 'gan'],
        'Ethics & Explainability': ['ethical', 'fairness', 'explainable']
    }
    return topic_keywords.get(topic, [topic.lower()])

def calculate_trend(yearly_series):
    """Calculate trend (increasing, decreasing, stable)"""
    if len(yearly_series) < 2:
        return 'insufficient_data'
    
    first_half = yearly_series.iloc[:len(yearly_series)//2].mean()
    second_half = yearly_series.iloc[len(yearly_series)//2:].mean()
    
    change = (second_half - first_half) / first_half if first_half > 0 else 0
    
    if change > 0.2:
        return 'increasing'
    elif change < -0.2:
        return 'decreasing'
    else:
        return 'stable'

if __name__ == "__main__":
    results = discover_topics()
