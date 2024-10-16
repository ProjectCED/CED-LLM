import pymupdf
import aiohttp
import os
from dotenv import load_dotenv
import asyncio

GPT_URL = "https://ced-llm.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"
load_dotenv()
GPT_KEY = os.getenv("GPT_KEY")


class ApiHandler():
    def __init__(self):
        pass


    def read_first_page(file_path: str):
        text = ""
        with pymupdf.open(file_path) as pdf:
            page = pdf.load_page(0)
            text += page.get_textpage().extractTEXT()
        return text


    async def send_text_promt(prompt: str):
        async with aiohttp.ClientSession() as session:
            # Role can be "user", "system", "tool" or "assistant"
            message = {"role": "user", "content": prompt}
            async with session.post(GPT_URL, json={"messages": [message]}, headers={"api-key": GPT_KEY}) as response:
                if (response.status != 200):
                    response.raise_for_status()
                return await response.json()
    
    
    # TODO: Add way to select blueprint to send as one message
    # TODO: Problem with sending long text, need to split it into smaller parts. text2 is an example of a text length that works.
    async def send_pdf(file_path: str):
        text = ApiHandler.read_first_page(file_path)

        text2 = """
Puhemies Jussi Halla-aho: Ainoaan käsittelyyn esitellään päiväjärjestyksen 2. asia. Nyt
annetaan vastaus edustaja Niina Malmin ynnä muiden välikysymykseen palkkatasa-arvos-
ta.
Työministeri Arto Satosen vastauksen ja edustaja Niina Malmin puheenvuoron jälkeen
välikysymyskeskustelu käydään etukäteen varattujen puheenvuorojen osalta nopeatahtise-
na. Aluksi pidetään yksi ryhmäpuheenvuorokierros, jossa puheenvuorojen pituus on enin-
tään 5 minuuttia. Muut ennakolta varatut puheenvuorot käytetään ryhmäpuheenvuorojär-
jestyksessä, ja niiden pituus on enintään 5 minuuttia. Puhemiesneuvosto suosittaa, että no-
peatahtisen keskusteluosuuden jälkeenkin pidettävät puheenvuorot kestävät enintään 5 mi-
nuuttia. Lisäksi voin myöntää harkitsemassani järjestyksessä vastauspuheenvuoroja. —
Ministeri Satonen, olkaa hyvä.
        """

        async with aiohttp.ClientSession() as session:
            # Role can be "user", "system", "tool" or "assistant"
            instruction = {"role": "system", "content": "Analyze the themes and key points of the text."}
            message = {"role": "user", "content": text}
            async with session.post(GPT_URL, json={"messages": [instruction, message]}, headers={"api-key": GPT_KEY}) as response:
                if (response.status != 200):
                    response.raise_for_status()
                json = await response.json()
                return json['choices'][0]['message']['content']
            

async def main():
    text = await ApiHandler.send_pdf("PTK_102+2024.pdf")
    print(text)
    

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())