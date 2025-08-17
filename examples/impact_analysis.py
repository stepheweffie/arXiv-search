#!/usr/bin/env python3
"""
Research Impact Analysis Example

This example demonstrates how to analyze research impact, identify influential papers,
track citation patterns, and discover breakthrough moments in machine learning research.
"""

import sys
sys.path.append('..')

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import re
from datetime import datetime, timedelta
from arxiv_search import ArxivSearcher

def analyze_research_impact():
    """Analyze research impact patterns and identify influential work"""
    
    searcher = ArxivSearcher()
    searcher.data_dir = "../meta-query-search/data"  # Fix path for examples
    
    if not searcher.load_existing_data():
        print("No data found! Please run: ../arxiv search machine learning --save")
        return
    
    df = searcher.current_data
    
    print("=== Research Impact Analysis ===")
    print(f"Analyzing impact patterns from {len(df)} papers")
    
    # Add derived features for analysis
    df = add_impact_features(df)
    
    # 1. Identify potentially high-impact papers
    print("\n🏆 Potentially High-Impact Papers...")
    high_impact = identify_high_impact_papers(df)
    
    # 2. Analyze breakthrough periods
    print("\n💥 Research Breakthrough Periods...")
    breakthroughs = identify_breakthrough_periods(df)
    
    # 3. Track technique adoption patterns
    print("\n📈 Technique Adoption Patterns...")
    adoption_patterns = analyze_adoption_patterns(df)
    
    # 4. Identify influential venues/authors
    print("\n🌟 Influential Research Patterns...")
    influence_patterns = analyze_influence_patterns(df)
    
    # 5. Find papers that introduced new concepts
    print("\n🚀 Concept Introduction Timeline...")
    concept_timeline = track_concept_introduction(df)
    
    return {
        'high_impact': high_impact,
        'breakthroughs': breakthroughs,
        'adoption_patterns': adoption_patterns,
        'influence_patterns': influence_patterns,
        'concept_timeline': concept_timeline
    }

def add_impact_features(df):
    """Add features that might indicate research impact"""
    df = df.copy()
    
    # Time features
    df['year'] = df['published'].dt.year
    df['age_years'] = datetime.now().year - df['year']
    
    # Title features that might indicate impact
    df['title_length'] = df['title'].str.len()
    df['has_novel'] = df['title'].str.contains('novel|new|first', case=False, na=False)
    df['has_breakthrough_words'] = df['title'].str.contains('breakthrough|revolutionar|groundbreaking', case=False, na=False)
    df['has_comparison'] = df['title'].str.contains('comparison|comparative|vs|versus', case=False, na=False)
    df['has_survey'] = df['title'].str.contains('survey|review|comprehensive', case=False, na=False)
    
    # Abstract features
    df['abstract_length'] = df['abstract'].fillna('').str.len()
    df['mentions_state_of_art'] = df['abstract'].str.contains('state.of.the.art|SOTA|state-of-the-art', case=False, na=False)
    df['mentions_performance'] = df['abstract'].str.contains('performance|accuracy|improvement|better', case=False, na=False)
    
    return df

def identify_high_impact_papers(df):
    """Identify papers likely to have high impact based on various signals"""
    
    # Create an impact score based on multiple factors
    impact_scores = pd.Series(0, index=df.index)
    
    # Factor 1: Early papers in a now-popular area (pioneering work)
    popular_terms_now = ['deep learning', 'neural network', 'transformer', 'attention', 'gan']
    for term in popular_terms_now:
        early_papers = df[
            (df['combined'].str.contains(term, case=False, na=False)) & 
            (df['year'] < 2015)  # Early adoption
        ]
        impact_scores.loc[early_papers.index] += 3
    
    # Factor 2: Papers introducing new concepts
    impact_scores += df['has_novel'].astype(int) * 2
    
    # Factor 3: Comprehensive surveys/reviews
    impact_scores += df['has_survey'].astype(int) * 2
    
    # Factor 4: Papers with performance claims
    impact_scores += df['mentions_performance'].astype(int)
    
    # Factor 5: Older papers still relevant (longevity)
    impact_scores += (df['age_years'] > 10).astype(int)
    
    # Get top scoring papers
    high_impact_papers = df.loc[impact_scores.nlargest(15).index]
    
    print("  Top Potentially High-Impact Papers:")
    for _, paper in high_impact_papers.iterrows():
        score = impact_scores.loc[paper.name]
        print(f"    📄 {paper['title'][:80]}...")
        print(f"       {paper['year']} | Impact Score: {score} | {paper['url']}")
        print()
    
    return high_impact_papers

def identify_breakthrough_periods(df):
    """Identify periods with significant research breakthroughs"""
    
    # Look for periods with sudden increases in certain types of papers
    df['year'] = df['published'].dt.year
    yearly_counts = df.groupby('year').size()
    
    # Key breakthrough indicators
    breakthrough_terms = [
        ('deep learning', 'Deep Learning Revolution'),
        ('convolutional neural', 'CNN Era'), 
        ('transformer', 'Transformer Era'),
        ('generative adversarial', 'GAN Era'),
        ('attention', 'Attention Mechanism Era'),
        ('bert|gpt', 'Large Language Model Era')
    ]
    
    breakthroughs = {}
    
    for term, era_name in breakthrough_terms:
        term_papers = df[df['combined'].str.contains(term, case=False, na=False)]
        if len(term_papers) > 0:
            yearly_term = term_papers.groupby('year').size()
            
            # Find the year with the biggest jump
            if len(yearly_term) >= 2:
                growth = yearly_term.pct_change().fillna(0)
                peak_growth_year = growth.idxmax() if growth.max() > 0 else None
                
                if peak_growth_year and growth.max() > 1:  # More than 100% growth
                    breakthroughs[era_name] = {
                        'breakthrough_year': int(peak_growth_year),
                        'growth_rate': growth.max(),
                        'total_papers': len(term_papers),
                        'peak_year_papers': int(yearly_term.loc[peak_growth_year])
                    }
    
    # Sort by breakthrough year
    sorted_breakthroughs = dict(sorted(breakthroughs.items(), key=lambda x: x[1]['breakthrough_year']))
    
    print("  Research Breakthrough Timeline:")
    for era, data in sorted_breakthroughs.items():
        print(f"    {data['breakthrough_year']}: {era}")
        print(f"       Growth: {data['growth_rate']:.1%} | Papers that year: {data['peak_year_papers']} | Total: {data['total_papers']}")
        print()
    
    return sorted_breakthroughs

def analyze_adoption_patterns(df):
    """Analyze how quickly new techniques are adopted"""
    
    key_techniques = {
        'CNNs': ['convolutional neural', 'cnn'],
        'RNNs/LSTMs': ['recurrent neural', 'lstm', 'rnn'],
        'Transformers': ['transformer', 'attention mechanism'],
        'GANs': ['generative adversarial', 'gan'],
        'Autoencoders': ['autoencoder', 'encoder decoder'],
        'Reinforcement Learning': ['reinforcement learning', 'policy gradient']
    }
    
    adoption_patterns = {}
    
    for technique, keywords in key_techniques.items():
        # Find papers mentioning this technique
        mask = df['combined'].str.contains('|'.join(keywords), case=False, na=False)
        technique_papers = df[mask]
        
        if len(technique_papers) >= 5:  # Need at least 5 papers
            yearly_counts = technique_papers.groupby('year').size()
            
            # Find adoption characteristics
            first_year = yearly_counts.index.min()
            peak_year = yearly_counts.idxmax()
            total_papers = len(technique_papers)
            
            # Calculate adoption speed (years to reach 50% of peak)
            cumulative = yearly_counts.cumsum()
            half_peak = yearly_counts.max() // 2
            years_to_half_peak = None
            
            for year, cum_count in cumulative.items():
                if cum_count >= half_peak:
                    years_to_half_peak = year - first_year
                    break
            
            adoption_patterns[technique] = {
                'first_appeared': int(first_year),
                'peak_year': int(peak_year),
                'total_papers': total_papers,
                'years_to_half_peak': years_to_half_peak,
                'adoption_speed': 'fast' if years_to_half_peak and years_to_half_peak <= 3 else 'gradual'
            }
    
    print("  Technology Adoption Analysis:")
    for technique, data in adoption_patterns.items():
        print(f"    {technique}: First {data['first_appeared']}, Peak {data['peak_year']}")
        print(f"       {data['total_papers']} papers, {data['adoption_speed']} adoption ({data['years_to_half_peak']} years to half-peak)")
        print()
    
    return adoption_patterns

def analyze_influence_patterns(df):
    """Analyze patterns that suggest influential research"""
    
    influence_patterns = {}
    
    # 1. Papers that seem to introduce terminology
    terminology_papers = df[
        df['title'].str.contains('introducing|novel|new approach to', case=False, na=False) |
        df['abstract'].str.contains('we introduce|we propose|we present', case=False, na=False)
    ]
    
    # 2. Methodological papers
    method_papers = df[
        df['title'].str.contains('method|algorithm|approach|framework|architecture', case=False, na=False)
    ]
    
    # 3. Empirical studies with broad implications
    empirical_papers = df[
        df['title'].str.contains('empirical|experimental|analysis|study of', case=False, na=False)
    ]
    
    influence_patterns = {
        'terminology_introducing': len(terminology_papers),
        'methodological': len(method_papers),
        'empirical_studies': len(empirical_papers)
    }
    
    # Find papers that might have started trends
    trend_starters = []
    
    # Look for early papers in areas that later became popular
    potential_trends = ['adversarial', 'attention', 'autoencoder', 'batch normalization', 'dropout']
    
    for trend in potential_trends:
        trend_papers = df[df['combined'].str.contains(trend, case=False, na=False)]
        if len(trend_papers) >= 10:  # Popular enough
            earliest = trend_papers.nsmallest(3, 'published')
            for _, paper in earliest.iterrows():
                trend_starters.append({
                    'title': paper['title'],
                    'year': paper['year'],
                    'trend': trend,
                    'url': paper['url']
                })
    
    print("  Research Influence Indicators:")
    print(f"    Papers introducing terminology: {influence_patterns['terminology_introducing']}")
    print(f"    Methodological papers: {influence_patterns['methodological']}")  
    print(f"    Empirical studies: {influence_patterns['empirical_studies']}")
    
    if trend_starters:
        print("\n  Potential Trend-Starting Papers:")
        for paper in trend_starters[:8]:
            print(f"    {paper['year']}: {paper['title'][:60]}... (Early {paper['trend']})")
    
    return influence_patterns

def track_concept_introduction(df):
    """Track when key concepts were first introduced in the dataset"""
    
    key_concepts = {
        'Deep Learning': ['deep learning', 'deep neural network'],
        'Convolutional Networks': ['convolutional neural', 'convnet', 'cnn'],
        'Recurrent Networks': ['recurrent neural', 'rnn', 'lstm', 'gru'],
        'Attention Mechanism': ['attention mechanism', 'self attention'],
        'Transformer': ['transformer', 'transformer architecture'],
        'Generative Adversarial': ['generative adversarial', 'gan'],
        'Variational Autoencoder': ['variational autoencoder', 'vae'],
        'Batch Normalization': ['batch normalization', 'batchnorm'],
        'Dropout': ['dropout', 'dropout regularization'],
        'Residual Networks': ['residual network', 'resnet', 'skip connection'],
        'Transfer Learning': ['transfer learning', 'fine tuning', 'pretrained'],
        'Meta Learning': ['meta learning', 'learning to learn'],
        'Few-shot Learning': ['few shot learning', 'one shot learning', 'zero shot']
    }
    
    concept_timeline = {}
    
    for concept, keywords in key_concepts.items():
        # Find papers mentioning this concept
        mask = df['combined'].str.contains('|'.join(keywords), case=False, na=False)
        concept_papers = df[mask]
        
        if len(concept_papers) > 0:
            first_paper = concept_papers.nsmallest(1, 'published').iloc[0]
            total_papers = len(concept_papers)
            
            concept_timeline[concept] = {
                'first_appearance': first_paper['year'],
                'first_paper_title': first_paper['title'],
                'first_paper_url': first_paper['url'],
                'total_papers': total_papers
            }
    
    # Sort by first appearance
    sorted_timeline = dict(sorted(concept_timeline.items(), key=lambda x: x[1]['first_appearance']))
    
    print("  Key Concept Introduction Timeline:")
    for concept, data in list(sorted_timeline.items())[:12]:
        print(f"    {data['first_appearance']}: {concept}")
        print(f"       First paper: \"{data['first_paper_title'][:50]}...\"")
        print(f"       Total papers: {data['total_papers']}")
        print()
    
    return sorted_timeline

if __name__ == "__main__":
    results = analyze_research_impact()
