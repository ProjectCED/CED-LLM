import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
import utils
from enum import Enum

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

class ApiHandler():
    # Enum for the models available
    class Models(Enum):
        PRIMARY_MODEL = "gpt-4o"
        BACKUP_MODEL = "gpt-4o-mini" # This has higher token limit


    def __init__(self):
        self.__client = OpenAI(api_key=OPENAI_KEY)

    def analyze_pdf(self, pdf_path, model) -> str:
        first_page = utils.extract_text_from_pdf(pdf_path)

        instructions = "Analyze the themes and key points of the text."

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
                        "content": first_page
                    }
                ]
            )

            result = response.choices[0].message.content.strip()
            return result
        
        except openai.RateLimitError:
            if (model == self.Models.PRIMARY_MODEL):
                print("Rate limit reached. Trying backup model.")
                return self.analyze_pdf(pdf_path, self.Models.BACKUP_MODEL)
            else:
                print("Rate limit reached (backup model used). Exiting.")
                return None
        



def main():
    #apiHandler = ApiHandler()
    #result = apiHandler.analyze_pdf("PTK_102+2024.pdf", apiHandler.Models.PRIMARY_MODEL)
    #print(result)
    pass

if __name__ == "__main__":
    main()