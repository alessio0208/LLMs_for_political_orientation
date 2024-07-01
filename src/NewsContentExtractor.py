import pandas as pd
import os
from .FileManager import FileManager
from newspaper import Article

# Define root and directory paths
ROOT = 'output'
INPUT_DIR = os.path.join(ROOT, 'cleaned_urls')
OUTPUT_DIR = os.path.join(ROOT, 'articles')

class NewsContentExtractor:
    """
    A class to extract news articles from URLs and save them to CSV files.
    """
    
    @staticmethod
    def extract_article_from_url(url):
        """
        Extracts the content of a news article from a given URL.
        
        Parameters:
        url (str): The URL of the news article.
        
        Returns:
        str: The extracted article text.
        """
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    
    def extract_all_articles(self):
        """
        Extracts articles from URLs in the input directory and saves them to the output directory.
        """
        cleaned_articles_files = FileManager.select_missing_files(INPUT_DIR, OUTPUT_DIR)
        articles = []
        
        for f in cleaned_articles_files:
            filepath = os.path.join(INPUT_DIR, f)
            df = pd.read_csv(filepath)
            
            for _, row in df.iterrows():
                print(row['articles'])
                try:
                    article_content = self.extract_article_from_url(row['articles'])
                    articles.append([row['newspaper'], row['articles'], article_content])
                except Exception as e:
                    print(f"Error extracting article from {row['articles']}: {e}")
                
            # Convert the list of articles to a DataFrame and save it
            articles_df = pd.DataFrame(articles, columns=['newspaper', 'article_url', 'article_content'])
            FileManager.save_file(f, 'articles', 'csv', OUTPUT_DIR, articles_df)