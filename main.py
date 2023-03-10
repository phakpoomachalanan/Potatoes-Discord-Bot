import discord
import openai
import asyncio
from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = getenv("TOKEN")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")

CODE_CHANNEL_ID = "1083305217799487508"
CHATGPT_CHANNEL_ID = "1083327345080926208"

client = discord.Client(intents=discord.Intents(members=True, message_content=True, guild_messages=True, guild_reactions=True, guilds=True))
openai.api_key = OPENAI_API_KEY

async def textToCode(message):
    msg = message.content
    lang = msg.split()[0]
    user = message.author

    await message.channel.send(f"```{lang}\nFrom: {user}\n\n{msg[len(lang):]}```")
    await message.delete()

    return

async def askChatGpt(message):
    msg = message.content
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": msg}
        ]
    )

    if response["choices"][0]["finish_reason"] != "null":
        await message.channel.send(response["choices"][0]["message"]["content"], reference=message)
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
        textToCode(message)
    elif msg_channel == CHATGPT_CHANNEL_ID:
        await askChatGpt(message)

client.run(TOKEN)