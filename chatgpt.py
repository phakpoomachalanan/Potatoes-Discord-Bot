from os import getenv
from dotenv import load_dotenv
import openai

load_dotenv('.env')

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

async def ask_chat_gpt(message):
    """
    
    """
    msg = message.content + " please make response message under 2000 letters"
    response = await get_ans(msg)
    if (response != "null"):
        await message.channel.send(response, reference=message)
    else:
        await message.channel.send("API request failed", reference=message)

async def get_ans(msg: str):
    """
    
    """
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": msg}
        ]
    )

    res_choices = response["choices"][0]

    if res_choices["finish_reason"] != "null":
        res_msg = response["choices"][0]["message"]["content"]
        return res_msg
    else:
        return "null"