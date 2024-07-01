import google.generativeai as genai
import ast
import time
from google.api_core.exceptions import InternalServerError

# Configure with your API key
genai.configure(api_key='your_key')

class AbstractGemini:
    
    def output_is_well_formed(self, output):
        """
        Checks if the output from the AI model is well-formed.
        
        Parameters:
        output (str): The output from the AI model as a string.
        
        Returns:
        bool: True if the output is a well-formed list of integers, False otherwise.
        """
        try:
            result = ast.literal_eval(output)
            return isinstance(result, list) and all(isinstance(x, int) for x in result)
        except (ValueError, SyntaxError):
            return False

    def query_model(self, query):
        """
        Queries the AI model with a given query and checks if the output is well-formed.
        
        Parameters:
        query (str): The query to be sent to the AI model.
        
        Returns:
        str: The output from the AI model.
        
        Raises:
        ValueError: If there is an internal server error or the output is not well-formed.
        """
        time.sleep(3)  # Delay to avoid rate limiting
        try:
            response = self.model.generate_content(query)
        except InternalServerError:
            raise ValueError("Internal Server Error occurred while querying the model.")
        
        output = response.text
        if not self.output_is_well_formed(output):
            raise ValueError("The output from the model is not well-formed.")
        
        return output
    
class Gemini(AbstractGemini):
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')


class Gemini15(AbstractGemini):

    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
