import aiohttp
import os
from dotenv import load_dotenv
import asyncio

GPT_URL = "https://ced-llm.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"
load_dotenv()
GPT_KEY = os.getenv("GPT_KEY")

async def get_gpt_response(prompt: str):
    async with aiohttp.ClientSession() as session:
        # Role can be "user", "system", "tool" or "assistant"
        message = {"role": "user", "content": prompt}
        async with session.post(GPT_URL, json={"messages": [message]}, headers={"api-key": GPT_KEY}) as response:
            if (response.status != 200):
                response.raise_for_status()
            return await response.json()