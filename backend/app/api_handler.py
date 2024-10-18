import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
import utils

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
PRIMARY_MODEL = "gpt-4o"
BACKUP_MODEL = "gpt-4o-mini" # This has higher token limit


class ApiHandler():
    def __init__(self):
        pass

    # Test version for sending only first page to save on tokens during testing
    def analyze_pdf_first_page(pdf_path, model) -> str:
        first_page = utils.extract_first_page_from_pdf(pdf_path)

        client = OpenAI(api_key=OPENAI_KEY)

        instructions = "Analyze the themes and key points of the text."

        try:
            response = client.chat.completions.create(
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
        
        except openai._exceptions.RateLimitError:
            if (model == PRIMARY_MODEL):
                print("Rate limit reached. Trying backup model.")
                ApiHandler.analyze_pdf_first_page(pdf_path, BACKUP_MODEL)
            else:
                print("Rate limit reached (backup model used). Exiting.")
                return None
        



def main():
    result = ApiHandler.analyze_pdf_first_page("PTK_102+2024.pdf", PRIMARY_MODEL)
    print(result)

if __name__ == "__main__":
    main()