import discord
import subprocess
from os import getenv, getcwd
from dotenv import load_dotenv
import module.chatgpt as chatgpt
import module.wordle as wordle
import module.text_to_code as ttc

load_dotenv('.env')

TOKEN = getenv("TOKEN")
CODE_CHANNEL_ID = getenv("CODE_CHANNEL_ID")
CHATGPT_CHANNEL_ID = getenv("CHATGPT_CHANNEL_ID")
WORDLE_CHANNEL_ID = getenv("WORDLE_CHANNEL_ID")
SUPER_USER = getenv("SUPER_USER")
SERVER_CHANNEL_ID = getenv("SERVER_CHANNEL_ID")


client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    await wordle.init_wordle()

@client.event
async def on_message(message):
    """
    Main program
    """
    if message.author == client.user:
        return
    
    msg_channel = str(message.channel.id)
    msg_content = str(message.content)

    if (msg_content.startswith("//")):
        return
    if (msg_channel == CODE_CHANNEL_ID):
        await ttc.text_to_code(message)
    elif (msg_channel == CHATGPT_CHANNEL_ID):
        await chatgpt.ask_chat_gpt(message)
    elif (msg_channel == WORDLE_CHANNEL_ID):
        await wordle.play_wordle(message)
    elif (msg_channel == SERVER_CHANNEL_ID):
        if (str(message.author.id) == SUPER_USER):
            if (msg_content.startswith("$")):
                sh_script = msg_content.strip("$ ")
                print(sh_script)
                if (sh_script == "git pull"):
                    result = subprocess.run("git pull", stdout=subprocess.PIPE)
                    # result = subprocess.run("pushd /home/popupie/pupserver/ZideQuest-Backend && git pull && popd", stdout=subprocess.PIPE)
                else:
                    result = subprocess.run(sh_script, stdout=subprocess.PIPE)
                await message.channel.send(f'```{result.stdout.decode("utf-8")}```')

if (__name__ == "__main__"):
    client.run(TOKEN)