# Large Language Models' Detection of Political Orientation in Newspapers

## Description
This project provides a set of tools to scrape, clean, and analyze news articles from various newspaper websites. The tools include extracting URLs, fetching article content, cleaning data, and evaluating the economic and political  stances expressed in the articles using different LLMs.

## Features
- Scrape article URLs from newspaper homepages
- Fetch and clean article content from extracted URLs
- Evaluate articles based on economic and political scales using different language models

## Data
The directory 'output/evaluations' already contains the dataset extracted and analyzed in the paper "Large Language Models’ Detection of Political Orientation in Newspapers" by Alessio Buscemi and Daniele Proverbio, 2024, https://arxiv.org/pdf/2406.00018

## Remarks
- To use OpenAI's GPTs and Google's Gemini models, you must update the relevant scripts with your own API keys.

## Installation
To set up the project locally, clone the repository and install the required dependencies:

```bash
git clone https://github.com/alessio0208/LLMs_for_political_orientation.git
cd LLMs_for_political_orientation
pip install -r requirements.txt
