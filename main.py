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
WORDLE_CHANNEL_ID = getenv("WORDLE_CHANNEL_ID")

client = discord.Client(intents=discord.Intents(members=True, message_content=True, guild_messages=True, guild_reactions=True, guilds=True))
openai.api_key = OPENAI_API_KEY

solution = "qwert".upper()
meaning = "asd"
times_ans = 0

async def play_wordle(message):
    global times_ans

    if (times_ans == 0):
        global solution, meaning
        temp = await generate_5_letter_word()
        print(temp)
        temp = temp.split()
        solution = temp[0].upper()
        meaning = " ".join(temp[2:])

    msg_channel = message.channel
    msg = message.content.upper()

    if (len(msg) != 5):
        await msg_channel.send("5-letter word only. Please try again.")
        return

    times_ans += 1
    result = check_ans(msg)

    if (result == solution):
        await msg_channel.send(f"```{times_ans} tries\n{solution} - {meaning}```", refernce=message)
        times_ans  = 0
    else:
        await msg_channel.send(f"```{times_ans} tries\n{result}```", refernce=message)
        if times_ans == 6:
            times_ans = 0
            await msg_channel.send(f"{solution} - {meaning}", refernce=message)

def check_ans(guess):
    result = ""
    
    print(solution)
    print(guess)
    for i in range(5):
        if (guess[i] == solution[i]):
            result += solution[i]
        elif (guess[i] in solution):
            result += solution[i].lower()
        else:
            result += "-"
    
    return result

async def generate_5_letter_word():
    response = await get_ans("generate one word with 5-letters and meaning. answer format word - meaning")
    return response

async def text_to_code(message):
    user = message.autho
    msg = message.content
    lang = msg.split()[0]
    code = msg[len(lang):]

    await message.channel.send(f"```{lang}\nFrom: {user}\n\n{code}```")
    await message.delete()

    return

async def ask_chat_gpt(message):
    msg = message.content + " please make response message under 2000 letters"
    response = await get_ans(msg)
    if (response != "null"):
        await message.channel.send(response, reference=message)
    else:
        await message.channel.send("API request failed", reference=message)

async def get_ans(msg):
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

@client.event
async def on_ready():
    print("Potato")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg_channel = str(message.channel.id)

    if (msg_channel == CODE_CHANNEL_ID):
        await text_to_code(message)
    elif (msg_channel == CHATGPT_CHANNEL_ID):
        await ask_chat_gpt(message)
    elif (msg_channel == WORDLE_CHANNEL_ID):
        await play_wordle(message)

client.run(TOKEN)