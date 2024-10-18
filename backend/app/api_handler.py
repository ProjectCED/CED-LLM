import pymupdf
import os
from dotenv import load_dotenv
from openai import OpenAI

GPT_URL = "https://ced-llm.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"
load_dotenv()
GPT_KEY = os.getenv("GPT_KEY")


class ApiHandler():
    def __init__(self):
        pass



def main():
    text = ApiHandler.send_pdf("PTK_102+2024.pdf")
    print(text)
    

if __name__ == "__main__":
    main()