import discord
import openai
import asyncio
from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = getenv("TOKEN")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
CODE_CHANNEL_ID = getenv("CODE_CHANNEL_ID")
CHATGPT_CHANNEL_ID = getenv("CHATGPT_CHANNEL_ID")

client = discord.Client(intents=discord.Intents(members=True, message_content=True, guild_messages=True, guild_reactions=True, guilds=True))
openai.api_key = OPENAI_API_KEY

async def text_to_code(message):
    user = message.autho
    msg = message.content
    lang = msg.split()[0]
    code = msg[len(lang):]

    await message.channel.send(f"```{lang}\nFrom: {user}\n\n{code}```")
    await message.delete()

    return

async def ask_chat_gpt(message):
    msg = message.content

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": msg + " please make response message under 2000 letters"}
        ]
    )

    res_choices = response["choices"][0]
    res_msg = res_choices["message"]["content"]

    if res_choices["finish_reason"] != "null":
        await message.channel.send(res_msg, reference=message)
    else:
        await message.channel.send("API request failed", reference=message)

    return

@client.event
async def on_ready():
    print("Potato")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg_channel = str(message.channel.id)

    if msg_channel == CODE_CHANNEL_ID:
        text_to_code(message)
    elif msg_channel == CHATGPT_CHANNEL_ID:
        await ask_chat_gpt(message)

client.run(TOKEN)