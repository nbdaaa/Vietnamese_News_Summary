# News Summary System

AI Multi-agent system for crawling and summarizing articles from Vietnamese news websites such as VnExpress, Dân Trí, and others.

## Overview

This system uses LangChain and LangGraph to build a multi-agent system capable of:

1. Crawling content from Vietnamese news websites
2. Summarizing content using LLM (In our project we use Gemini 2.0 Flash)
3. Saving results as a CSV file with 2 columns: Origin crawl text and summarized text

The system includes 4 main agents:
- Coordinator Agent: Manages workflow
- Crawler Agent: Collects content from news sites and preprocessing data
- Summarizer Agent: Summarizes content using LLM
- Storage Agent: Stores results into data/output

## Requirements

- Python 3.8+
- Conda (for environment management)
- LLM key (Here is Gemini)

## Installation

### Setting up the environment:

```bash
# Create a new Conda environment
conda create -n news-summary python=3.10

# Activate the environment
conda activate news-summary

# Install required libraries
conda install -c conda-forge pip
pip install langchain langchain-community langchain-openai beautifulsoup4 requests pandas langchain-experimental langchain_text_splitters langgraph aiohttp tenacity
```

Or you can use the environment.yml file:

```bash
conda env create -f environment.yml
conda activate news-summary
```

### Configuration:

Before running, edit the `config/settings.py` file to set:
- OpenAI API key
- Default URL list
- Other system parameters

## Directory Structure

```
news_summary_system/
├── config/              # System configuration
│   └── settings.py
├── agents/              # System agents
│   ├── __init__.py
│   ├── coordinator.py   # Coordination agent
│   ├── crawler.py       # Content collection agent
│   ├── summarizer.py    # Summarization agent
│   └── storage.py       # Storage agent
├── utils/               # Utilities
│   ├── __init__.py
│   └── helpers.py
├── data/                # Data directory
│   └── output/          # Output results
├── main.py              # Main execution file
├── environment.yml      # Conda environment configuration
├── requirements.txt     # Requirement for the project
└── README.md            # Documentation
```

## Usage

To run the system with default URLs:

```bash
python main.py
```

Or specify particular URLs:

```bash
python main.py https://vnexpress.net/thoi-su https://dantri.com.vn/su-kien.htm
```

Results will be saved in `data/output/news_summaries.csv`.

## Customization

### Adjusting summarization logic:

You can modify the prompts and parameters for the OpenAI model in `agents/summarizer.py`.

## Technologies Used

- **LangChain**: Framework for LLM-based applications
- **LangGraph**: Library for building multi-agent systems
- **Gemini**: Large language model for summarization
- **Trafilatura**: State-of-the-art open-source extractor (ACL 2021 paper).
- ~~**BeautifulSoup**: HTML parsing library~~ (Not needed anymore)

## Contributing

Contributions are welcome! Please create an issue or pull request if you want to improve this project.

## License

This project is distributed under the MIT license.
