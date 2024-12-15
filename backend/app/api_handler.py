import json
import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
import app.utils as utils
import requests

PRIMARY_MODEL = "gpt-4o"
BACKUP_MODEL = "gpt-4o-mini" # This has higher token limit
MISTRAL_MODEL = "mistral"

class ApiHandler():
    """
    Handler class for interacting with LLMs. Currently only supports OpenAI's GPT-4o/GPT-4o-mini models.
    Should be initialized once and used through one instance.
    """
    def __init__(self):
        """
        Constructor for the ApiHandler class. Initializes the OpenAI client with the OPENAI_KEY from the .env file.
        """
        load_dotenv()
        OPENAI_KEY = os.getenv("OPENAI_KEY")
        self.__client = OpenAI(api_key=OPENAI_KEY)

    def openai_analyze(self, text: str, blueprint: dict, model: str = PRIMARY_MODEL) -> str:
        """
        Analyzes the given text using the specified model and blueprint. Model is set to GPT-4o by default.
        If the rate limit is reached and the backup model is not yet used, tries to generate result with the backup model.
        (Currently GPT-4o-mini). If the backup model also fails, returns None.

        Args:
            text (string): Text to be analyzed. If analyzing files (PDF/txt), use `analyze_file()` instead.
            blueprint (dict): Blueprint dict containing questions for the LLM.
                Can be null if analyzing with 'default/automatic blueprint'.
            model (str, optional): GPT Model to be used for analysis. Defaults to PRIMARY_MODEL (GPT-4o).
        
        Returns:
            string: Analysis result text generated by the LLM.
                Can be None if the rate limit even for the backup model (GPT-4o-mini) is reached.
        """
        # TODO: Create separate file for instructions in both Finnish and English
        instructions = (
            "You are an expert in text analysis. Please read the provided text carefully "
            "and then produce a structured analysis with the following components:\n\n"

            "1. **Main Themes**: Identify and summarize the core themes or central ideas present in the text.\n"
            "2. **Key Points**: Highlight the most important details, arguments, or statements that stand out.\n"
            "3. **Notable Quotes or Passages**: Include any direct quotes or paraphrased sections that are especially significant or illustrative.\n"
            "4. **Overall Sentiment**: Describe the general tone or emotional quality of the text (e.g., optimistic, critical, neutral, etc.).\n\n"

            "If there are specific questions provided, answer each of them thoroughly after completing your summary. "
            "Make sure your answers are clear, concise, and directly address the questions.\n"
        )

        if blueprint is not None and "questions" in blueprint:
            instructions += (
                "\nAdditionally, please answer the following questions:\n" +
                "\n".join(f"- {question}" for question in blueprint["questions"])
            )
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
            if (model != BACKUP_MODEL):
                return self.openai_analyze(text, blueprint, BACKUP_MODEL)
            else:
                return None
            
    def analyze_file(self, filepath: str, blueprint: dict, model: str = PRIMARY_MODEL) -> str:
        """
        Extracts the text from the given file and analyzes it using `openai_analyze()`.

        Args:
            filepath (string): Absolute path to the file to be analyzed. Supports PDF and txt files.
            blueprint (dict): Blueprint dict containing questions for the LLM.
                Can be null if analyzing with 'default/automatic blueprint'.
            model (str, optional): GPT Model to be used for analysis. Defaults to PRIMARY_MODEL (GPT-4o).

        Returns:
            string: Analysis result text generated by the LLM.
                Can be None if the rate limit even for the backup model (GPT-4o-mini) is reached.
        """
        text = utils.extract_text_from_file(filepath)
        if text is None:
            return None
        return self.analyze(text, blueprint, model)

    def mistral_analyze(self, text, blueprint) -> str:
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
        instructions = (
            "You are an expert in text analysis. Please read the provided text carefully "
            "and then produce a structured analysis with the following components:\n\n"

            "1. **Main Themes**: Identify and summarize the core themes or central ideas present in the text.\n"
            "2. **Key Points**: Highlight the most important details, arguments, or statements that stand out.\n"
            "3. **Notable Quotes or Passages**: Include any direct quotes or paraphrased sections that are especially significant or illustrative.\n"
            "4. **Overall Sentiment**: Describe the general tone or emotional quality of the text (e.g., optimistic, critical, neutral, etc.).\n\n"

            "If there are specific questions provided, answer each of them thoroughly after completing your summary. "
            "Make sure your answers are clear, concise, and directly address the questions.\n"
        )

        if blueprint is not None and "questions" in blueprint:
            instructions += (
                "\nAdditionally, please answer the following questions:\n" +
                "\n".join(f"- {question}" for question in blueprint["questions"])
            )

        instructions += "\n\n" + text
        
        data = {
            "model": MISTRAL_MODEL,
            "prompt": instructions,
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

    def analyze(self, text: str, blueprint: dict, model: str) -> str:
        """
        Analyzes the given text using the specified model and blueprint. Model is set to GPT-4o by default.
        If the rate limit is reached and the backup model is not yet used, tries to generate result with the backup model.
        (Currently GPT-4o-mini). If the backup model also fails, returns None.

        Args:
            text (string): Text to be analyzed. If analyzing files (PDF/txt), use `analyze_file()` instead.
            blueprint (dict): Blueprint dict containing questions for the LLM.
                Can be null if analyzing with 'default/automatic blueprint'.
            model (str, optional): GPT Model to be used for analysis. Defaults to PRIMARY_MODEL (GPT-4o).
        
        Returns:
            string: Analysis result text generated by the LLM.
                Can be None if the rate limit even for the backup model (GPT-4o-mini) is reached.
        """
        if model.strip().lower() == "mistral":
            return self.mistral_analyze(text, blueprint)
        else:
            return self.openai_analyze(text, blueprint)         

def main():
    #apiHandler = ApiHandler()
    #result = apiHandler.analyze_file("PTK_102+2024.pdf", PRIMARY_MODEL)
    #print(result)
    pass

if __name__ == "__main__":
    main()
