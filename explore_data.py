#!/usr/bin/env python3
"""
Script to explore the existing arXiv search data
"""

import pickle
import pandas as pd
import os

def load_sorted_data():
    """Load the processed arXiv data"""
    data_file = "meta-query-search/data/SortMetaTask/SortMetaTask__99914b932b-data.pkl"
    
    if os.path.exists(data_file):
        with open(data_file, 'rb') as f:
            data = pickle.load(f)
        return data
    else:
        print(f"Data file not found: {data_file}")
        return None

def explore_data():
    """Explore the structure and contents of the data"""
    data = load_sorted_data()
    
    if data is None:
        return
    
    print("Data type:", type(data))
    print("Data keys:", list(data.keys()) if isinstance(data, dict) else "Not a dictionary")
    
    if isinstance(data, pd.DataFrame):
        print("\nDataFrame Info:")
        print(f"Shape: {data.shape}")
        print(f"Columns: {list(data.columns)}")
        print("\nFirst few rows:")
        print(data.head())
        
        # Show some statistics
        if 'title_has_word' in data.columns:
            print(f"\nPapers with search terms in title: {data['title_has_word'].sum()}")
        
        if 'two_year_date' in data.columns:
            print(f"Papers from last 2 years: {data['two_year_date'].sum()}")
            
        if 'published' in data.columns:
            print(f"Date range: {data['published'].min()} to {data['published'].max()}")
    
    return data

if __name__ == "__main__":
    explore_data()
