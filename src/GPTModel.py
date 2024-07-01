import openai

# Configure with your API key
openai.api_key = 'your_key'

class AbstractGPT():
    
    def query_model(self, query):
        """
        Queries the GPT model with the provided query and returns the model's response.

        Parameters:
        query (str): The query string to be sent to the model.

        Returns:
        str: The content of the model's response.
        """
        # Create a completion using the OpenAI API's chat completion method
        completion = openai.chat.completions.create(
            model=self.model,  # Specify the model to be used
            messages=[
                {"role": "system", "content": "You are an expert of politics and journalism."},  # Set the context for the model
                {"role": "user", "content": query}  # Include the user query
            ]
        )
    
        # Extract the content of the first response choice
        output = completion.choices[0].message.content
        
        # Return the model's response content
        return output

    def name(self):
        return self.model

class GPT35(AbstractGPT):
    def __init__(self):
        self.model = "gpt-3.5-turbo"

class GPT4(AbstractGPT):
    def __init__(self):
        self.model = 'gpt-4'