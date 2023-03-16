import discord
from os import getenv
from dotenv import load_dotenv
from module.chatgpt import *
from module.wordle import *
from module.text_to_code import *

load_dotenv('.env')

TOKEN = getenv("TOKEN")
CODE_CHANNEL_ID = getenv("CODE_CHANNEL_ID")
CHATGPT_CHANNEL_ID = getenv("CHATGPT_CHANNEL_ID")
WORDLE_CHANNEL_ID = getenv("WORDLE_CHANNEL_ID")
WORDLE_ANS_CHANNEL_ID = getenv("WORDLE_ANS_CHANNEL_ID")

client = discord.Client(intents=discord.Intents(members=True, message_content=True, guild_messages=True, guild_reactions=True, guilds=True))

@client.event
async def on_ready():
    solution, meaning = await init_wordle()
    channel = client.get_channel(int(WORDLE_ANS_CHANNEL_ID))
    await channel.send(f"{solution} - {meaning}")

@client.event
async def on_message(message):
    """
    Main program
    """
    if message.author == client.user:
        return
    
    msg_channel = str(message.channel.id)
    # print(msg_channel)
    
    if (message.content.startswith("//")):
        return
    if (msg_channel == CODE_CHANNEL_ID):
        await text_to_code(message)
    elif (msg_channel == CHATGPT_CHANNEL_ID):
        await ask_chat_gpt(message)
    elif (msg_channel == WORDLE_CHANNEL_ID):
        await play_wordle(message)

if (__name__ == "__main__"):
    client.run(TOKEN)