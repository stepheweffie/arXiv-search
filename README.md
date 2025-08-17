# arXiv Search Tool

A comprehensive command-line tool for searching and managing arXiv papers using the arXiv API. This tool allows you to search for papers, filter results, and analyze the data with ease.

## Features

- **Search arXiv API**: Query arXiv for papers using keywords
- **Local Search**: Search within previously downloaded data
- **Date Filtering**: Filter papers by publication date
- **Export Results**: Export search results to CSV, JSON, or pickle formats
- **Statistics**: View statistics about your paper collection
- **Recent Papers**: List and filter recent publications

## Quick Start

### Using the existing data (3,000+ papers on machine learning, meta data)

```bash
# View statistics about existing data
./arxiv stats

# Search for papers about "neural networks" in titles
./arxiv find "neural networks" --field title

# List recent papers (most recent first)
./arxiv list --recent --limit 10

# Filter papers from last 2 years
./arxiv filter --recent-years 2

# Search abstracts for "deep learning"
./arxiv find "deep learning" --field abstract
```

### Searching for new papers

```bash
# Search arXiv for new papers about quantum computing
./arxiv search quantum computing --save

# Search with more specific keywords
./arxiv search natural language processing transformers --max-results 1000
```

## Installation & Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd arXiv-search
   ```

2. **Set up the virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Make the wrapper script executable**:
   ```bash
   chmod +x arxiv
   ```

## Usage

### Commands

#### `search` - Search arXiv API for new papers
```bash
./arxiv search <keywords...> [options]

# Options:
# --max-results, -m    Maximum number of results (default: 3000)
# --save, -s           Save results to pickle file

# Examples:
./arxiv search machine learning ethics --save
./arxiv search computer vision --max-results 500
```

#### `find` - Search within existing data
```bash
./arxiv find <query> [options]

# Options:
# --field, -f          Field to search in: title, abstract, combined (default: combined)
# --case-sensitive, -c Case sensitive search
# --export, -e         Export results to file
# --format             Export format: csv, json, pkl (default: csv)

# Examples:
./arxiv find "reinforcement learning" --field title
./arxiv find "transformer" --export results.csv
./arxiv find "GAN" --case-sensitive --field title
```

#### `filter` - Filter data by publication date
```bash
./arxiv filter [options]

# Options:
# --recent-years, -r   Papers from last N years
# --start-date, -s     Start date (YYYY-MM-DD)
# --end-date, -e       End date (YYYY-MM-DD)
# --export             Export filtered results to file
# --format             Export format: csv, json, pkl (default: csv)

# Examples:
./arxiv filter --recent-years 1
./arxiv filter --start-date 2020-01-01 --end-date 2022-12-31
./arxiv filter --recent-years 2 --export recent_papers.json --format json
```

#### `stats` - Show statistics about the data
```bash
./arxiv stats

# Shows:
# - Total number of papers
# - Date range of publications
# - Papers with search terms in title
# - Papers from recent years
# - Top 10 most frequent words in titles
```

#### `list` - List papers
```bash
./arxiv list [options]

# Options:
# --limit, -l    Number of papers to show (default: 10)
# --recent, -r   Show most recent papers first

# Examples:
./arxiv list --limit 20
./arxiv list --recent --limit 5
```

## Data Structure

The tool processes papers into a pandas DataFrame with the following columns:
- `title`: Paper title
- `abstract`: Paper abstract
- `published`: Publication date
- `updated`: Last update date
- `url`: arXiv URL
- `two_year_date`: 1 if published in last 2 years, 0 otherwise
- `title_has_word`: Boolean indicating if search terms are in title
- `combined`: Title + abstract combined for full-text search

## Examples

### Research Workflow Example
```bash
# 1. Check what data you have
./arxiv stats

# 2. Find papers about a specific topic
./arxiv find "attention mechanism" --field title --export attention_papers.csv

# 3. Get recent papers on your topic
./arxiv filter --recent-years 1 --export recent_ml_papers.json --format json

# 4. Search for new papers on a different topic
./arxiv search robotics automation --save

# 5. List the most recent papers to see what's new
./arxiv list --recent --limit 15
```

### Export and Analysis
```bash
# Export all neural network papers to CSV for analysis
./arxiv find "neural network" --export neural_networks.csv

# Get papers from 2023 and export as JSON
./arxiv filter --start-date 2023-01-01 --end-date 2023-12-31 --export papers_2023.json --format json

# Export recent transformer papers as pickle for Python analysis
./arxiv find "transformer" --field combined --export transformer_papers.pkl --format pkl
```

## Data Location

Processed data is stored in:
- `meta-query-search/data/SortMetaTask/` - Main processed dataset
- `meta-query-search/data/MetaDataTask/` - Raw arXiv API responses

## Current Dataset

The repository contains a pre-processed dataset of 3,000 papers related to:
- Machine learning
- Meta learning
- Data science
- Related computational topics

Date range: 1992 to 2025 (regularly updated)
Last updated: July 2025

## Python API

You can also use the `ArxivSearcher` class directly in Python:

```python
from arxiv_search import ArxivSearcher

searcher = ArxivSearcher()
searcher.load_existing_data()

# Search within data
results = searcher.search_local("deep learning", field="title")

# Filter by date
recent_papers = searcher.filter_by_date(recent_years=1)

# Get statistics
searcher.show_stats()
```
