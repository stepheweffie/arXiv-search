#!/usr/bin/env python3
"""
arXiv Search Tool - Command-line interface for searching and managing arXiv papers
"""

import argparse
import pickle
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import sys
from io import StringIO
import re

class ArxivSearcher:
    def __init__(self):
        self.data_dir = "meta-query-search/data"
        self.current_data = None
        
    def load_existing_data(self):
        """Load existing processed data"""
        data_file = f"{self.data_dir}/SortMetaTask/SortMetaTask__99914b932b-data.pkl"
        
        if os.path.exists(data_file):
            with open(data_file, 'rb') as f:
                self.current_data = pickle.load(f)
            return True
        return False
    
    def search_arxiv_api(self, query_words, max_results=3000):
        """Search arXiv using the API"""
        queries = [word + '&' for word in query_words]
        query = ''.join(queries)
        url = f'https://export.arxiv.org/api/query?search_query=all:{query}start=0&max_results={max_results}'
        
        print(f"Searching arXiv with URL: {url}")
        print(f"Query words: {', '.join(query_words)}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text, url
        except requests.RequestException as e:
            print(f"Error fetching data from arXiv: {e}")
            return None, None
    
    def process_arxiv_xml(self, xml_data, search_term=None):
        """Process XML data from arXiv API"""
        try:
            df = pd.read_xml(StringIO(xml_data))
            
            # Calculate two years ago timestamp
            two_years_ago = pd.Timestamp.now(tz='UTC') - pd.DateOffset(years=2)
            
            # Create processed dataframe
            xml_df = pd.DataFrame()
            xml_df['title'] = df['title'][7:]  # Skip the first 7 metadata rows
            xml_df['abstract'] = df['summary'][7:]
            xml_df['published'] = pd.to_datetime(df['published'][7:])
            xml_df['updated'] = df['updated'][7:]
            xml_df['url'] = df['id'][7:]
            
            # Add computed columns
            xml_df['two_year_date'] = xml_df['published'].apply(lambda x: 1 if x > two_years_ago else 0)
            
            if search_term:
                xml_df['title_has_word'] = xml_df['title'].str.contains(f'{search_term}', case=False)
            else:
                xml_df['title_has_word'] = False
                
            xml_df['combined'] = xml_df['title'] + ' ' + xml_df['abstract']
            
            return xml_df
            
        except Exception as e:
            print(f"Error processing XML data: {e}")
            return None
    
    def search_local(self, query, field='combined', case_sensitive=False):
        """Search within loaded data"""
        if self.current_data is None:
            if not self.load_existing_data():
                print("No existing data found. Run a new search first.")
                return None
        
        if field not in self.current_data.columns:
            print(f"Field '{field}' not found in data. Available fields: {list(self.current_data.columns)}")
            return None
        
        # Perform search
        mask = self.current_data[field].str.contains(query, case=case_sensitive, na=False)
        results = self.current_data[mask]
        
        return results
    
    def filter_by_date(self, start_date=None, end_date=None, recent_years=None):
        """Filter data by publication date"""
        if self.current_data is None:
            if not self.load_existing_data():
                print("No existing data found. Run a new search first.")
                return None
        
        df = self.current_data.copy()
        
        if recent_years:
            cutoff_date = pd.Timestamp.now(tz='UTC') - pd.DateOffset(years=recent_years)
            df = df[df['published'] > cutoff_date]
        
        if start_date:
            start_date = pd.to_datetime(start_date)
            df = df[df['published'] >= start_date]
        
        if end_date:
            end_date = pd.to_datetime(end_date)
            df = df[df['published'] <= end_date]
        
        return df
    
    def show_stats(self):
        """Display statistics about the current data"""
        if self.current_data is None:
            if not self.load_existing_data():
                print("No existing data found. Run a new search first.")
                return
        
        df = self.current_data
        print("=== arXiv Data Statistics ===")
        print(f"Total papers: {len(df)}")
        print(f"Date range: {df['published'].min()} to {df['published'].max()}")
        
        if 'title_has_word' in df.columns:
            print(f"Papers with search terms in title: {df['title_has_word'].sum()}")
        
        if 'two_year_date' in df.columns:
            print(f"Papers from last 2 years: {df['two_year_date'].sum()}")
        
        # Top words in titles
        all_titles = ' '.join(df['title'].astype(str)).lower()
        words = re.findall(r'\b\w+\b', all_titles)
        word_freq = pd.Series(words).value_counts()
        print("\nTop 10 most frequent words in titles:")
        print(word_freq.head(10))
    
    def export_results(self, data, filename, format='csv'):
        """Export results to file"""
        if format.lower() == 'csv':
            data.to_csv(filename, index=False)
        elif format.lower() == 'json':
            data.to_json(filename, orient='records', indent=2)
        elif format.lower() == 'pkl':
            data.to_pickle(filename)
        else:
            print(f"Unsupported format: {format}")
            return False
        
        print(f"Results exported to {filename}")
        return True

def main():
    parser = argparse.ArgumentParser(description='arXiv Search Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # New search command
    search_parser = subparsers.add_parser('search', help='Search arXiv API for new papers')
    search_parser.add_argument('keywords', nargs='+', help='Keywords to search for')
    search_parser.add_argument('--max-results', '-m', type=int, default=3000, help='Maximum number of results')
    search_parser.add_argument('--save', '-s', action='store_true', help='Save results to pickle file')
    
    # Local search command
    local_parser = subparsers.add_parser('find', help='Search within existing data')
    local_parser.add_argument('query', help='Search query')
    local_parser.add_argument('--field', '-f', default='combined', 
                             choices=['title', 'abstract', 'combined'], help='Field to search in')
    local_parser.add_argument('--case-sensitive', '-c', action='store_true', help='Case sensitive search')
    local_parser.add_argument('--export', '-e', help='Export results to file')
    local_parser.add_argument('--format', choices=['csv', 'json', 'pkl'], default='csv', help='Export format')
    
    # Filter command
    filter_parser = subparsers.add_parser('filter', help='Filter data by date')
    filter_parser.add_argument('--recent-years', '-r', type=int, help='Papers from last N years')
    filter_parser.add_argument('--start-date', '-s', help='Start date (YYYY-MM-DD)')
    filter_parser.add_argument('--end-date', '-e', help='End date (YYYY-MM-DD)')
    filter_parser.add_argument('--export', help='Export filtered results to file')
    filter_parser.add_argument('--format', choices=['csv', 'json', 'pkl'], default='csv', help='Export format')
    
    # Stats command
    subparsers.add_parser('stats', help='Show statistics about the data')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List papers')
    list_parser.add_argument('--limit', '-l', type=int, default=10, help='Number of papers to show')
    list_parser.add_argument('--recent', '-r', action='store_true', help='Show most recent papers first')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    searcher = ArxivSearcher()
    
    if args.command == 'search':
        xml_data, url = searcher.search_arxiv_api(args.keywords, args.max_results)
        if xml_data:
            processed_data = searcher.process_arxiv_xml(xml_data, ' '.join(args.keywords[:2]))
            if processed_data is not None:
                print(f"Successfully processed {len(processed_data)} papers")
                searcher.current_data = processed_data
                
                if args.save:
                    filename = f"arxiv_search_{'_'.join(args.keywords)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
                    processed_data.to_pickle(filename)
                    print(f"Results saved to {filename}")
    
    elif args.command == 'find':
        results = searcher.search_local(args.query, args.field, args.case_sensitive)
        if results is not None:
            print(f"Found {len(results)} matching papers:")
            for idx, row in results.head(10).iterrows():
                print(f"\n{idx}. {row['title']}")
                print(f"   Published: {row['published']}")
                print(f"   URL: {row['url']}")
            
            if len(results) > 10:
                print(f"\n... and {len(results) - 10} more results")
            
            if args.export:
                searcher.export_results(results, args.export, args.format)
    
    elif args.command == 'filter':
        results = searcher.filter_by_date(args.start_date, args.end_date, args.recent_years)
        if results is not None:
            print(f"Found {len(results)} papers matching date criteria")
            
            if args.export:
                searcher.export_results(results, args.export, args.format)
    
    elif args.command == 'stats':
        searcher.show_stats()
    
    elif args.command == 'list':
        if searcher.current_data is None:
            searcher.load_existing_data()
        
        if searcher.current_data is not None:
            df = searcher.current_data
            if args.recent:
                df = df.sort_values('published', ascending=False)
            
            print(f"Listing {min(args.limit, len(df))} papers:")
            for idx, row in df.head(args.limit).iterrows():
                print(f"\n{idx}. {row['title']}")
                print(f"   Published: {row['published']}")
                print(f"   URL: {row['url']}")

if __name__ == "__main__":
    main()
