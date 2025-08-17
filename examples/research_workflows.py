#!/usr/bin/env python3
"""
Quick Research Workflows

This example provides ready-to-use workflows for common research tasks:
- Literature review preparation
- Competitive analysis
- Technology landscape mapping
- Research gap identification
"""

import sys
sys.path.append('..')

import pandas as pd
from datetime import datetime, timedelta
from arxiv_search import ArxivSearcher

def literature_review_workflow(topic, years_back=5):
    """Comprehensive workflow for literature review preparation"""
    
    print(f"=== Literature Review Workflow: {topic} ===")
    
    searcher = ArxivSearcher()
    searcher.data_dir = "../meta-query-search/data"  # Fix path for examples
    
    if not searcher.load_existing_data():
        print("No data found! Please run: ../arxiv search machine learning --save")
        return
    
    df = searcher.current_data
    
    # 1. Find relevant papers
    relevant_papers = df[df['combined'].str.contains(topic, case=False, na=False)]
    
    if len(relevant_papers) == 0:
        print(f"No papers found for '{topic}'. Try a broader search term.")
        return
    
    print(f"Found {len(relevant_papers)} papers related to '{topic}'")
    
    # 2. Filter by recency
    cutoff_date = pd.Timestamp.now() - pd.DateOffset(years=years_back)
    recent_papers = relevant_papers[relevant_papers['published'] > cutoff_date]
    
    print(f"Recent papers (last {years_back} years): {len(recent_papers)}")
    
    # 3. Identify key paper types
    survey_papers = recent_papers[
        recent_papers['title'].str.contains('survey|review|overview|comprehensive', case=False, na=False)
    ]
    
    method_papers = recent_papers[
        recent_papers['title'].str.contains('method|algorithm|approach|framework', case=False, na=False)
    ]
    
    empirical_papers = recent_papers[
        recent_papers['title'].str.contains('empirical|experimental|evaluation|comparison', case=False, na=False)
    ]
    
    print(f"\n📊 Paper Categories:")
    print(f"  Survey/Review papers: {len(survey_papers)}")
    print(f"  Methodological papers: {len(method_papers)}")
    print(f"  Empirical papers: {len(empirical_papers)}")
    
    # 4. Create reading list prioritized by type and date
    reading_list = []
    
    # Start with recent surveys
    for _, paper in survey_papers.sort_values('published', ascending=False).head(3).iterrows():
        reading_list.append({
            'priority': 'HIGH',
            'type': 'Survey',
            'title': paper['title'],
            'year': paper['published'].year,
            'url': paper['url']
        })
    
    # Add recent influential-looking papers
    influential = recent_papers[
        recent_papers['title'].str.contains('novel|breakthrough|significant|important', case=False, na=False)
    ].sort_values('published', ascending=False).head(5)
    
    for _, paper in influential.iterrows():
        reading_list.append({
            'priority': 'HIGH',
            'type': 'Novel Method',
            'title': paper['title'],
            'year': paper['published'].year,
            'url': paper['url']
        })
    
    # Add recent methodological papers
    for _, paper in method_papers.sort_values('published', ascending=False).head(8).iterrows():
        reading_list.append({
            'priority': 'MEDIUM',
            'type': 'Method',
            'title': paper['title'],
            'year': paper['published'].year,
            'url': paper['url']
        })
    
    print(f"\n📚 Prioritized Reading List:")
    for i, paper in enumerate(reading_list[:15], 1):
        print(f"  {i}. [{paper['priority']}] {paper['type']}: {paper['title'][:60]}...")
        print(f"     {paper['year']} | {paper['url']}")
        print()
    
    return {
        'total_papers': len(relevant_papers),
        'recent_papers': len(recent_papers),
        'reading_list': reading_list,
        'surveys': survey_papers,
        'methods': method_papers,
        'empirical': empirical_papers
    }

def competitive_analysis_workflow(your_approach, competitor_approaches):
    """Analyze how your approach compares to competitors"""
    
    print(f"=== Competitive Analysis: {your_approach} ===")
    
    searcher = ArxivSearcher()
    searcher.data_dir = "../meta-query-search/data"  # Fix path for examples
    
    if not searcher.load_existing_data():
        print("No data found! Please run: ../arxiv search machine learning --save")
        return
    
    df = searcher.current_data
    
    # Analyze each approach
    approaches = [your_approach] + competitor_approaches
    analysis = {}
    
    for approach in approaches:
        papers = df[df['combined'].str.contains(approach, case=False, na=False)]
        
        if len(papers) > 0:
            recent_papers = papers[papers['published'] > pd.Timestamp.now() - pd.DateOffset(years=2)]
            
            analysis[approach] = {
                'total_papers': len(papers),
                'recent_papers': len(recent_papers),
                'first_paper_year': papers['published'].dt.year.min(),
                'latest_paper_year': papers['published'].dt.year.max(),
                'trend': 'growing' if len(recent_papers) > len(papers) * 0.3 else 'stable'
            }
    
    print(f"\n🏁 Competitive Landscape:")
    for approach, data in analysis.items():
        status = "🚀 YOUR APPROACH" if approach == your_approach else "🔍 Competitor"
        print(f"  {status}: {approach}")
        print(f"     Total papers: {data['total_papers']}")
        print(f"     Recent activity: {data['recent_papers']} papers (last 2 years)")
        print(f"     Timeline: {data['first_paper_year']} - {data['latest_paper_year']}")
        print(f"     Trend: {data['trend']}")
        print()
    
    # Find combination opportunities
    print(f"🔗 Combination Opportunities:")
    for competitor in competitor_approaches:
        combo_papers = df[
            df['combined'].str.contains(your_approach, case=False, na=False) &
            df['combined'].str.contains(competitor, case=False, na=False)
        ]
        print(f"  {your_approach} + {competitor}: {len(combo_papers)} existing papers")
    
    return analysis

def technology_landscape_workflow(domain):
    """Map the technology landscape for a domain"""
    
    print(f"=== Technology Landscape: {domain} ===")
    
    searcher = ArxivSearcher()
    
    if not searcher.load_existing_data():
        print("No data found! Please run: ../arxiv search machine learning --save")
        return
    
    df = searcher.current_data
    
    # Find papers in the domain
    domain_papers = df[df['combined'].str.contains(domain, case=False, na=False)]
    
    if len(domain_papers) == 0:
        print(f"No papers found for domain '{domain}'")
        return
    
    print(f"Analyzing {len(domain_papers)} papers in {domain}")
    
    # Extract technologies and techniques
    technologies = extract_technologies(domain_papers)
    
    # Time-based analysis
    df['year'] = df['published'].dt.year
    recent_years = domain_papers[domain_papers['year'] >= 2020]
    older_years = domain_papers[domain_papers['year'] < 2020]
    
    print(f"\n🛠️ Technology Adoption in {domain}:")
    
    tech_evolution = {}
    for tech, count in technologies.items():
        recent_count = recent_years['combined'].str.contains(tech, case=False, na=False).sum()
        older_count = older_years['combined'].str.contains(tech, case=False, na=False).sum()
        
        if older_count > 0:
            growth = (recent_count - older_count) / older_count
            status = "🔥 Hot" if growth > 0.5 else "📈 Growing" if growth > 0 else "📉 Declining"
        else:
            status = "🆕 New" if recent_count > 0 else "❓ Rare"
        
        tech_evolution[tech] = {
            'status': status,
            'total': count,
            'recent': recent_count,
            'older': older_count
        }
    
    # Sort by recent activity
    sorted_tech = sorted(tech_evolution.items(), key=lambda x: x[1]['recent'], reverse=True)
    
    for tech, data in sorted_tech[:12]:
        print(f"  {data['status']} {tech}: {data['total']} papers ({data['recent']} recent)")
    
    return {
        'domain': domain,
        'total_papers': len(domain_papers),
        'technologies': tech_evolution
    }

def research_gap_workflow(established_area, emerging_area):
    """Identify research gaps between established and emerging areas"""
    
    print(f"=== Research Gap Analysis ===")
    print(f"Established: {established_area}")
    print(f"Emerging: {emerging_area}")
    
    searcher = ArxivSearcher()
    
    if not searcher.load_existing_data():
        print("No data found! Please run: ../arxiv search machine learning --save")
        return
    
    df = searcher.current_data
    
    # Find papers in each area
    established_papers = df[df['combined'].str.contains(established_area, case=False, na=False)]
    emerging_papers = df[df['combined'].str.contains(emerging_area, case=False, na=False)]
    
    # Find intersection
    intersection = df[
        df['combined'].str.contains(established_area, case=False, na=False) &
        df['combined'].str.contains(emerging_area, case=False, na=False)
    ]
    
    print(f"\n📊 Gap Analysis:")
    print(f"  {established_area} papers: {len(established_papers)}")
    print(f"  {emerging_area} papers: {len(emerging_papers)}")
    print(f"  Combined papers: {len(intersection)}")
    
    # Calculate gap score
    expected_intersection = (len(established_papers) * len(emerging_papers)) / len(df)
    gap_score = max(0, expected_intersection - len(intersection)) / expected_intersection
    
    print(f"  Gap Score: {gap_score:.2f} (0=no gap, 1=major gap)")
    
    if gap_score > 0.5:
        print(f"  🎯 RESEARCH OPPORTUNITY: High potential for combining {established_area} with {emerging_area}")
    elif gap_score > 0.2:
        print(f"  💡 MODERATE OPPORTUNITY: Some potential for integration")
    else:
        print(f"  ✅ WELL EXPLORED: Good coverage of the intersection")
    
    # Show what exists in the intersection
    if len(intersection) > 0:
        print(f"\n🔗 Existing Work at Intersection:")
        for _, paper in intersection.head(5).iterrows():
            print(f"  • {paper['title'][:70]}... ({paper['published'].year})")
    
    # Suggest unexplored combinations
    print(f"\n💭 Potential Research Directions:")
    
    # Extract key terms from each area
    established_terms = extract_key_terms_simple(established_papers)
    emerging_terms = extract_key_terms_simple(emerging_papers)
    
    suggestions = []
    for est_term in established_terms[:5]:
        for emg_term in emerging_terms[:5]:
            combo_papers = df[
                df['combined'].str.contains(est_term, case=False, na=False) &
                df['combined'].str.contains(emg_term, case=False, na=False)
            ]
            if len(combo_papers) <= 2:  # Very few papers
                suggestions.append(f"{est_term} + {emg_term}")
    
    for suggestion in suggestions[:5]:
        print(f"  🎯 {suggestion}")
    
    return {
        'established_count': len(established_papers),
        'emerging_count': len(emerging_papers),
        'intersection_count': len(intersection),
        'gap_score': gap_score,
        'suggestions': suggestions
    }

def extract_technologies(papers):
    """Extract technology mentions from papers"""
    
    common_techs = [
        'neural network', 'deep learning', 'convolutional', 'recurrent', 'transformer',
        'attention', 'lstm', 'gru', 'bert', 'gpt', 'gan', 'autoencoder', 'vae',
        'reinforcement learning', 'q learning', 'policy gradient', 'actor critic',
        'support vector', 'random forest', 'gradient boosting', 'naive bayes',
        'clustering', 'k means', 'hierarchical', 'dbscan', 'pca', 'tsne'
    ]
    
    tech_counts = {}
    for tech in common_techs:
        count = papers['combined'].str.contains(tech, case=False, na=False).sum()
        if count > 0:
            tech_counts[tech] = count
    
    return dict(sorted(tech_counts.items(), key=lambda x: x[1], reverse=True))

def extract_key_terms_simple(papers):
    """Extract key terms from papers for gap analysis"""
    
    import re
    from collections import Counter
    
    # Extract terms from titles (more focused than abstracts)
    text = ' '.join(papers['title'].astype(str)).lower()
    
    # Find multi-word terms
    terms = re.findall(r'\b[a-z]+(?:\s+[a-z]+){1,2}\b', text)
    
    # Filter and count
    term_counts = Counter(terms)
    filtered = {term: count for term, count in term_counts.items() 
               if count >= 3 and len(term.split()) >= 2}
    
    return [term for term, _ in sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:20]]

# Example usage functions
def run_example_workflows():
    """Run example workflows to demonstrate capabilities"""
    
    print("🚀 Running Example Research Workflows...\n")
    
    # Example 1: Literature review for deep learning
    print("=" * 60)
    literature_review_workflow("deep learning", years_back=3)
    
    # Example 2: Competitive analysis
    print("=" * 60)
    competitive_analysis_workflow(
        "transformer", 
        ["lstm", "gru", "attention mechanism"]
    )
    
    # Example 3: Technology landscape
    print("=" * 60)
    technology_landscape_workflow("computer vision")
    
    # Example 4: Research gap analysis
    print("=" * 60)
    research_gap_workflow("reinforcement learning", "meta learning")

if __name__ == "__main__":
    # You can run specific workflows or all examples
    
    # Single workflow examples:
    # literature_review_workflow("neural networks")
    # competitive_analysis_workflow("gpt", ["bert", "transformer"])
    # technology_landscape_workflow("nlp")
    # research_gap_workflow("computer vision", "quantum computing")
    
    # Or run all examples:
    run_example_workflows()
