import os
import sys
import pandas as pd
from src.UrlExtractor import UrlExtractor
from src.UrlsCleaner import UrlsCleaner
from src.NewsContentExtractor import NewsContentExtractor
from src.LLMManager import LLMManager
from src.ArticlesCleaner import ArticlesCleaner
from src.GPTModel import GPT35, GPT4
from src.GeminiModel import Gemini, Gemini15

# Define input directory and filename constants
INPUT_DIR = 'input'
NEWSPAPERS_FILENAME = 'selected_newspapers.csv'

def scrape_urls():
    """
    Scrapes article URLs from a list of newspaper homepages.
    """
    # Load the list of newspaper URLs from a CSV file
    news_df = pd.read_csv(os.path.join(INPUT_DIR, NEWSPAPERS_FILENAME))
    urls = news_df['homepage']
    
    # Initialize the URL scraper
    scraper = UrlExtractor()
    
    for url in urls:
        print(url)
        try:
            # Fetch and save article URLs for each newspaper homepage
            article_urls = scraper.fetch_article_urls(url)
            scraper.save_urls_to_json(url, article_urls)
        except Exception as e:
            # Log faulty URLs that cannot be processed
            print(f"Error processing {url}: {e}")
            scraper.log_faulty_url(url)
    
    # Clean the extracted URLs
    articles_cleaner = UrlsCleaner()
    articles_cleaner.top20_articles()

def scrape_articles():
    """
    Scrapes the content of articles from previously extracted URLs.
    """
    # Initialize and run the article content extractor
    article_extractor = NewsContentExtractor()
    article_extractor.extract_all_articles()

def clean_articles():
    """
    Cleans the scraped articles based on optional length constraints.
    """
    try:
        # Get minimum and maximum length from command line arguments
        min_length = int(sys.argv[2])
        max_length = int(sys.argv[3])
        articles_cleaner = ArticlesCleaner()
        articles_cleaner.clean(min_length=min_length, max_length=max_length)
    except IndexError:
        # Default cleaning without length constraints
        articles_cleaner = ArticlesCleaner()
        articles_cleaner.clean()

def evaluate_articles():
    """
    Evaluates articles using the specified language model.
    """
    # Get the model name from command line arguments
    model_name = sys.argv[2]
    
    # Select the appropriate model based on the provided name
    if model_name == 'gpt3':
        model = GPT35()
    elif model_name == 'gpt4':
        model = GPT4()
    elif model_name == 'gemini':
        model = Gemini()
    elif model_name == 'gemini1.5':
        model = Gemini15()
    else:
        raise Exception("No model selected")
    
    try:
        # Get input directory from command line arguments, if provided
        input_dir = sys.argv[3]
        llm_manager = LLMManager(model, input_dir=input_dir)
    except IndexError:
        # Initialize LLMManager without input directory
        llm_manager = LLMManager(model)
    
    # Query the selected model on the articles
    llm_manager.query_models_on_articles()

if __name__ == "__main__":
    # Get the action from the command line arguments
    try:
        action = sys.argv[1]
    except IndexError:
        raise Exception("No action selected")

    if action == 'scrape_urls':
        scrape_urls()
    elif action == 'scrape_articles':
        scrape_articles()
    elif action == 'clean_articles':
        clean_articles()
    elif action == 'evaluate':
        evaluate_articles()
    else:
        raise Exception("Invalid action selected")
