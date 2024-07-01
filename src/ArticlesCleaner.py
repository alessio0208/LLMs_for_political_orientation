import pandas as pd
import os
from .FileManager import FileManager

# Define the root directory and subdirectories for input and output files
ROOT = 'output'
INPUT_DIR = os.path.join(ROOT, 'articles')
OUTPUT_DIR = os.path.join(ROOT, 'cleaned_articles')

class ArticlesCleaner:
    
    @staticmethod
    def clean(min_length=1000, max_length=5000):
        """
        Cleans articles by filtering out those that do not meet the length requirements
        and saves the cleaned articles to the output directory.
        
        Parameters:
        min_length (int): Minimum length of article content to be included.
        max_length (int): Maximum length of article content to be included.
        """
        
        # Select files that need to be processed
        files_to_process = FileManager.select_missing_files(INPUT_DIR, OUTPUT_DIR)
        
        for f in files_to_process:
            # Construct the full file path for reading
            filepath = os.path.join(INPUT_DIR, f)
            
            # Read the CSV file into a DataFrame
            df = pd.read_csv(filepath)
            
            # Ensure 'article_content' is of string type
            df = df[df['article_content'].apply(lambda x: isinstance(x, str))]
            df['content_length'] = df['article_content'].apply(len)

            # Filter the DataFrame to include only rows where content_length is within the desired range
            filtered_df = df[(df['content_length'] >= min_length) & (df['content_length'] <= max_length)]
            
            # Filter groups to ensure each newspaper has at least 5 articles
            result_df = filtered_df.groupby('newspaper').filter(lambda x: len(x) >= 5)
                          
            final_df = result_df[['newspaper', 'article_url', 'article_content']]
            
            # Save the cleaned DataFrame to the output directory
            FileManager.save_file(f, 'cleanedArticles', 'csv', OUTPUT_DIR, final_df)
