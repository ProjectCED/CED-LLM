import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
import app.utils as utils

PRIMARY_MODEL = "gpt-4o"
BACKUP_MODEL = "gpt-4o-mini" # This has higher token limit

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

    def analyze_text(self, text: str, blueprint: dict, model: str = PRIMARY_MODEL) -> str:
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
        instructions = "Analyze the themes and key points of the text"
        if blueprint is not None and "questions" in blueprint:
            instructions += " using the following questions:\n"  + "\n".join(blueprint["questions"])

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
                return self.analyze_text(text, BACKUP_MODEL)
            else:
                return None
            
    def analyze_file(self, filepath: str, blueprint: dict, model: str = PRIMARY_MODEL) -> str:
        """
        Extracts the text from the given file and analyzes it using `analyze_text()`.

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
        return self.analyze_text(text, blueprint, model)