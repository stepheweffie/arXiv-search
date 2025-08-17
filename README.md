# 🚀 arXiv Visual Search & Analytics

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Jupyter Book](https://img.shields.io/badge/Jupyter-Book-orange.svg)](https://jupyterbook.org/)
[![arXiv](https://img.shields.io/badge/arXiv-papers-red.svg)](https://arxiv.org/)

**A comprehensive research discovery platform** combining arXiv paper search, AI-powered semantic analysis, and stunning interactive visualizations. Transform how you explore and analyze academic research with transformer-based embeddings, clustering analysis, and beautiful data visualizations.

## ✨ What Makes This Special

🧠 **AI-Powered Semantic Search** - Find papers using natural language queries with transformer embeddings  
📊 **Interactive Visual Analytics** - Beautiful charts, word clouds, and 2D embedding visualizations  
📚 **Complete Jupyter Book** - Professional documentation with executable notebooks  
🎯 **1,500+ Pre-analyzed Papers** - Ready-to-use dataset spanning 30+ years  
🔬 **Advanced ML Clustering** - Discover research paper relationships and groups  
📈 **Publication Trend Analysis** - Track research evolution over time

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

## 📚 Jupyter Book: Visual Analytics

Explore the complete **interactive Jupyter Book** with stunning visualizations and comprehensive analysis:

### 🎯 Book Chapters:

1. **📊 Data Processing with d6tflow** - Automated workflow management
2. **🤖 Transformer Setup & Models** - AI-powered semantic embeddings  
3. **🔍 Simple Semantic Search** - Natural language paper discovery
4. **🎨 Visual Analytics & Interactive Charts** - Stunning data visualizations

### 🚀 Getting Started with Notebooks:

```bash
# Navigate to the Jupyter Book directory
cd meta-query-search/

# Install additional visualization dependencies
pip install matplotlib seaborn plotly wordcloud umap-learn

# Run individual notebooks
jupyter notebook working_integrated.ipynb    # Simple semantic search
jupyter notebook visual_integrated.ipynb     # Full visual analytics

# Build the complete Jupyter Book
jupyter-book build .
```

### 📊 Visual Features:

**🎨 Interactive Visualizations:**
- 📈 Publication trends over 30+ years
- ☁️ Dynamic word clouds for research topics
- 🎯 2D embedding space with UMAP clustering
- 📊 Advanced analytics dashboard with Plotly
- 🔍 Search result similarity visualization

**🧠 AI-Powered Analysis:**
- 🤖 SentenceTransformer embeddings (768-dimensional)
- 🎯 K-means clustering (8 distinct research groups)
- 📐 Cosine similarity search scoring
- 🧮 UMAP dimensionality reduction for visualization

**📈 Analytics Dashboard:**
- 📅 Publication timeline analysis
- 🏷️ Keyword frequency charts
- 📏 Title/abstract length distributions  
- 🔄 Recent vs. historical paper comparisons

### 💻 Semantic Search Examples:

```python
# Load the visual analytics system
from working_integrated import semantic_search, display_results

# Natural language searches
results = semantic_search("attention mechanisms in neural networks", top_k=10)
display_results(results)

# Topic-based discovery
results = semantic_search("computer vision deep learning", top_k=5)
results = semantic_search("reinforcement learning algorithms", top_k=7)
```

## 🎮 Interactive Features

### 🔍 **Semantic Search**
Query papers using natural language instead of exact keywords:
- "deep learning for natural language processing"
- "computer vision and image recognition" 
- "reinforcement learning in robotics"

### 📊 **Visual Exploration**
- **Clustering Visualization**: See how papers group by research topics
- **Similarity Heatmaps**: Discover paper relationships
- **Publication Trends**: Track research evolution over time
- **Word Clouds**: Identify trending research keywords

### 🎯 **Smart Filtering**
- Cluster-based filtering (8 ML research groups)
- Publication date ranges (1992-2025)
- Similarity threshold filtering
- Keyword presence analysis

## 📊 Dataset Statistics

**Current Analysis Results:**
- 📚 **Total Papers**: 1,500+ research papers
- 📅 **Date Range**: 1992-2025 (33 years of research)
- 🆕 **Recent Papers**: 229 papers (last 2 years)
- 🏷️ **Keyword Matches**: 616 papers with ML terms in titles
- 🎯 **Research Clusters**: 8 distinct ML research groups
- 🧮 **Embedding Dimensions**: 768-dimensional transformer embeddings

**Top Research Topics:**
- Machine Learning: 656 papers
- Learning: 472 papers  
- Machines: 203 papers
- Quantum: 64 papers
- Deep Learning: 59 papers

## 🛠️ Advanced Usage

### 📈 **Visual Analytics Workflow**

```python
# 1. Load enhanced visual notebook
jupyter notebook meta-query-search/visual_integrated.ipynb

# 2. Run semantic search with visualizations
results = semantic_search_with_viz("transformer attention", top_k=10)

# 3. Explore cluster visualizations
# - 2D UMAP embedding space
# - Interactive Plotly charts
# - Word cloud generation

# 4. Export enhanced results
df_enhanced.to_csv('arxiv_visual_analysis.csv')
```

### 🎨 **Customization Options**

```python
# Adjust clustering parameters
kmeans = KMeans(n_clusters=12, random_state=42)  # More clusters

# Modify embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Smaller model

# Customize visualization colors
px.scatter(color_discrete_sequence=px.colors.qualitative.Set3)
```

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

## 🚀 What's Next?

**Planned Enhancements:**
- 🔄 Real-time arXiv monitoring
- 📧 Research alert notifications  
- 🌐 Web-based dashboard interface
- 📱 Mobile-responsive visualizations
- 🤖 GPT integration for paper summaries
- 🔗 Citation network analysis
- 📊 Impact factor predictions

## 🤝 Contributing

We welcome contributions! Areas for improvement:
- 🎨 Additional visualization types
- 🔍 Enhanced search algorithms
- 📊 More statistical analyses
- 🚀 Performance optimizations
- 📚 Documentation improvements

## 📄 License

MIT License - feel free to use and modify for your research needs!

## 🙏 Acknowledgments

- **arXiv** for providing free access to scientific papers
- **Hugging Face** for transformer models and sentence-transformers
- **Plotly** for interactive visualizations
- **Jupyter Book** for beautiful documentation
- **UMAP** for dimensionality reduction

---

**⭐ Star this repository if you find it useful for your research!**
