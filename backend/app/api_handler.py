import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
import app.utils as utils

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
    
    def test_file_read(self, filepath):
        text = utils.extract_text_from_file(filepath)
        if text is None:
            return None
        return text
    
    def test_simple_return(self, text):
        return text
        

def main():
    #apiHandler = ApiHandler()
    #result = apiHandler.analyze_file("PTK_102+2024.pdf", PRIMARY_MODEL)
    #print(result)
    pass

if __name__ == "__main__":
    main()