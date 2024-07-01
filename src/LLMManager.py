import re
import os
import pandas as pd
from .FileManager import FileManager

# Define root and directory paths
ROOT = 'output'
ARTICLES_DIR = os.path.join(ROOT, 'cleaned_articles')
SELECTED_ARTICLES_DIR = os.path.join(ROOT, 'selected_articles')
OUTPUT_DIR = os.path.join(ROOT, 'evaluations')

class LLMManager:
    
    def __init__(self, model, input_dir=''):
        """
        Initializes the LLMManager with a model and sets the input directory.
        
        Parameters:
        model: The language model to be used.
        input_dir (str): Directory to read articles from. Defaults to 'cleaned_articles'.
        """
        self.model = model
        self.input_dir = SELECTED_ARTICLES_DIR if input_dir == 'selected' else ARTICLES_DIR

    def generate_task(self, article):
        """
        Generates the task query to be sent to the language model.
        
        Parameters:
        article (str): The article content.
        
        Returns:
        str: The task query for the model.
        """
        task = (
            '''Instructions: Economic Scale from -10 to 10, where -10 is Economic Left and 
            10 Economic Right. Scale Democracy Scale from -10 to 10, where -10 is Libertarian 
            and 10 is Authoritarian. I provide a newspaper article. 
            Output only the political position of the author in the format 
            [mark for Economic Scale, mark for Democracy Scale]. 
            NEVER WRITE ANY TEXT BEFORE OR AFTER THE RESULT. 
            ALWAYS provide the result, even if you are not fully sure.
            Article: '''
        )
        query = task + article
        return query
    
    def query_model(self, article):
        """
        Queries the model with the generated task and extracts marks.
        
        Parameters:
        article (str): The article content.
        
        Returns:
        list: Extracted marks for economic and democracy scales.
        """
        query = self.generate_task(article)
        output = self.model.query_model(query)
        marks = self.extract_points_and_comment(output)
        return marks
        
    def extract_points_and_comment(self, text):
        """
        Extracts the marks from the model's output.
        
        Parameters:
        text (str): The model's output.
        
        Returns:
        list: The extracted marks as integers.
        """
        matches = re.findall(r'\[(-?\d+), (-?\d+)\]', text)[0]
        marks = [int(matches[0]), int(matches[1])]
        return marks
    
    def save_results_csv(self, evals, filename):
        """
        Saves the evaluation results to a CSV file.
        
        Parameters:
        evals (list): List of evaluations.
        filename (str): The filename to save the results as.
        """
        evals_df = pd.DataFrame(evals, columns=['newspaper', 'article_url', 'article_content',
                                                'mark_socioeconomic', 'mark_democracy'])
        
        FileManager.save_file(filename, self.model.name(), 'csv', OUTPUT_DIR, evals_df)

    def query_models_on_articles(self):
        """
        Queries the model on all articles in the input directory and saves the results.
        """
        articles_files = os.listdir(self.input_dir)
        
        for f in articles_files:
            filepath = os.path.join(self.input_dir, f)
            df = pd.read_csv(filepath)
            all_evals = []
            
            for newspaper in df['newspaper'].unique():
                print(newspaper)
                df_newspaper = df[df['newspaper'] == newspaper]
                evals = self.query_all_articles_in_newspaper(df_newspaper)
                all_evals.extend(evals)
                
            self.save_results_csv(all_evals, f)        
            
    def query_all_articles_in_newspaper(self, df_newspaper):
        """
        Queries the model on all articles for a specific newspaper and returns evaluations.
        
        Parameters:
        df_newspaper (pd.DataFrame): DataFrame containing articles from a single newspaper.
        
        Returns:
        list: List of evaluations.
        """
        evals = []
        
        for _, row in df_newspaper.iterrows():
            try:
                marks = self.query_model(row['article_content'])
                print(marks)
                evals.append([row['newspaper'], row['article_url'], 
                              row['article_content'], marks[0], marks[1]])       
                if len(evals) == 5:
                    break
            except (IndexError, TypeError, ValueError, SyntaxError):
                continue
        
        return evals
