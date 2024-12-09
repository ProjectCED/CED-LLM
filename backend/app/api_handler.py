import json
import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
import app.utils as utils
import requests

PRIMARY_MODEL = "gpt-4o"
BACKUP_MODEL = "gpt-4o-mini" # This has higher token limit

class ApiHandler():
    def __init__(self):
        load_dotenv()
        OPENAI_KEY = os.getenv("OPENAI_KEY")
        self.__client = OpenAI(api_key=OPENAI_KEY)

    def analyze_text(self, text, model=PRIMARY_MODEL) -> str:
        # TODO: Create separate file for instructions in both Finnish and English
        instructions = "Analyze the themes and key points of the text."

        # Try to get the response from the chat completions API
        try:
            response = self.__client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": instructions
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )

            result = response.choices[0].message.content.strip()
            return result
        
        # If the rate limit is reached, try the backup model, if the backup model also fails, return None
        except openai.RateLimitError:
            if (model == PRIMARY_MODEL):
                return self.analyze_text(text, BACKUP_MODEL)
            else:
                return None
            
    def analyze_file(self, filepath, model=PRIMARY_MODEL) -> str:
        text = utils.extract_text_from_file(filepath)
        if text is None:
            return None
        return self.analyze_text(text, model)
    
    def test_file_read(self, filepath: str) -> str:
        text = utils.extract_text_from_file(filepath)
        if text is None:
            return None
        return text

    def mistral_analyze(self, prompt) -> str:
        """
        Analyzes the given prompt using the Mistral model via an API call.

        Args:
            prompt (str): The input prompt to be analyzed by the Mistral model.

        Returns:
            str: The combined JSON response from the API call as a string. If an error occurs, 
                a dictionary with an "error" key and the error message is returned.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
            json.JSONDecodeError: If the response contains invalid JSON.
        """
        data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
        }
        try:
            response = requests.post("http://ollama:11434/api/generate", json=data, stream=False)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            # Read the response in chunks and assemble it into a complete JSON object
            response_text = ""
            for chunk in response.iter_content(chunk_size=8192):
                response_text += chunk.decode('utf-8')

            print("Raw response text:", response_text)  # Print the raw response text for debugging

            # Combine the response text into a single JSON object
            combined_response = {}
            json_objects = response_text.split('\n')
            for obj in json_objects:
                if obj.strip():  # Skip empty lines
                    try:
                        json_obj = json.loads(obj)
                        combined_response.update(json_obj)
                    except json.JSONDecodeError as e:
                        print(f"Failed to decode JSON object: {obj}")
                        return {"error": "Invalid JSON response"}

            return combined_response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {"error": str(e)}
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {response_text}")
            return {"error": "Invalid JSON response"}
    
    
        

def main():
    #apiHandler = ApiHandler()
    #result = apiHandler.analyze_file("PTK_102+2024.pdf", PRIMARY_MODEL)
    #print(result)
    pass

if __name__ == "__main__":
    main()