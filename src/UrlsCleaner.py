import json
import pandas as pd
import os
from .FileManager import FileManager

# Define root and directory paths
ROOT = 'output'
INPUT_DIR = os.path.join(ROOT, 'urls')
OUTPUT_DIR = os.path.join(ROOT, 'cleaned_urls')

class UrlsCleaner:
    """
    A class to clean and filter URLs of articles, and save the top 20 longest articles per newspaper.
    """

    def clean_dataframe(self, urls):
        """
        Cleans the DataFrame by eliminating newspapers with fewer than 30 articles.
        
        Parameters:
        urls (dict): Dictionary with newspaper names as keys and lists of URLs as values.
        
        Returns:
        pd.DataFrame: A cleaned DataFrame with sufficient articles.
        """
        data = [(key, value) for key, values in urls.items() for value in values]
        df = pd.DataFrame(data, columns=['newspaper', 'articles'])
        df_count = df.groupby('newspaper').count().sort_values(by='articles').reset_index()
        
        # Identify newspapers with fewer than 30 articles
        to_eliminate = df_count[df_count['articles'] < 30]
        eliminate_names = to_eliminate['newspaper'].tolist()
        
        # Filter out newspapers with insufficient articles
        df_filtered = df[~df['newspaper'].isin(eliminate_names)]
        return df_filtered

    @staticmethod
    def top_articles(group):
        """
        Selects the top 20 longest articles from each newspaper.
        
        Parameters:
        group (pd.DataFrame): DataFrame group of articles for a specific newspaper.
        
        Returns:
        pd.DataFrame: DataFrame containing the top 20 longest articles.
        """
        return group.sort_values('length', ascending=False).head(20)

    @staticmethod
    def save(articles, filepath):
        """
        Saves the filtered articles to a CSV file.
        
        Parameters:
        articles (pd.DataFrame): DataFrame containing filtered articles.
        filepath (str): The original file path for constructing the output filename.
        """
        filename = os.path.basename(filepath)
        FileManager.save_file(filename, 'cleanedUrls', 'csv', OUTPUT_DIR, articles)

    def top20_articles(self):
        """
        Processes all JSON files in the input directory to filter and save the top 20 articles per newspaper.
        """
        json_files = FileManager.select_missing_files(INPUT_DIR, OUTPUT_DIR)
        
        for file in json_files:
            filepath = os.path.join(INPUT_DIR, file)
            
            with open(filepath, 'r') as f:
                urls = json.load(f)
            
            df = self.clean_dataframe(urls)
            df['length'] = df['articles'].apply(len)
            
            # Apply the top_articles function to each newspaper group
            top_articles_per_newspaper = df.groupby('newspaper').apply(self.top_articles)
            top_articles_per_newspaper.reset_index(drop=True, inplace=True)
            top_articles_per_newspaper.drop('length', axis=1, inplace=True)
            
            self.save(top_articles_per_newspaper, filepath)
