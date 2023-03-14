import discord
import openai
import asyncio
import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = getenv("TOKEN")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
CODE_CHANNEL_ID = getenv("CODE_CHANNEL_ID")
CHATGPT_CHANNEL_ID = getenv("CHATGPT_CHANNEL_ID")
WORDLE_CHANNEL_ID = getenv("WORDLE_CHANNEL_ID")

WORD_URL = "https://random-word-api.herokuapp.com/word?length=5"
DICT_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

client = discord.Client(intents=discord.Intents(members=True, message_content=True, guild_messages=True, guild_reactions=True, guilds=True))
openai.api_key = OPENAI_API_KEY

solution = "qwert".upper()
meaning = "idk"
times_ans = 0
sol_dict = dict()

async def play_wordle(message):
    """
    Wordle main program
    """
    global times_ans

    if (times_ans == 0):
        global solution, meaning
        solution = await generate_5_letter_word()

        while (not has_meaning(solution, True)):
            solution = await generate_5_letter_word()

        print(solution, meaning)
        for i in range(5):
            char = solution[i]
            sol_dict[char] = solution.count(char)

    msg_channel = message.channel
    msg = message.content.upper()

    if (not has_meaning(msg, False)):
        await msg_channel.send(f"No Definitions Found.", reference=message)
        return

    if (len(msg) != 5):
        await msg_channel.send("5-letter word only. Please try again.", reference=message)
        return

    times_ans += 1
    result = check_ans(msg)

    if (result == solution):
        await msg_channel.send(f"```{times_ans} tries\n{solution} - {meaning}```", reference=message)
        times_ans  = 0
    else:
        await msg_channel.send(f"```{times_ans} tries\n{result}```", reference=message)
        if times_ans == 6:
            times_ans = 0
            await msg_channel.send(f"```{solution} - {meaning}```", reference=message)

def has_meaning(word: str, is_solution: bool):
    """
    Return True if word has meaning in dictionaryapi
    """
    temp = requests.get(DICT_URL + word).json()
    try: 
        temp = temp[0]["meanings"][0]["definitions"][0]["definition"]
        if (is_solution):
            global meaning
            meaning = temp
    except:
        return False
    return True

def check_ans(guess: str):
    """
    Return how close your guess was to the word.
    """
    result = ["" for i in range(5)]
    
    gue_dict = dict()
    now_dict = dict()

    # Correct cases
    for i in range(5):
        char = guess[i]
        if (char in solution):
            gue_dict[char] = guess.count
            now_dict[char] = 0

    # Wrong cases
    for i in range(5):
        char = guess[i]
        # Wrong spot
        if (char == solution[i]):
            now_dict[char] += 1
            result[i] = solution[i]
        # Absent cases
        else:
            result[i] = "-"

    for i in range(5):
        char = guess[i]
        if (char in solution and now_dict[char] < sol_dict[char]):
            now_dict[char] += 1
            result[i] = char.lower()
    
    return "".join(result)

async def generate_5_letter_word():
    """
    Get random 5-letter word from random-word-api.herokuapp
    """
    response = requests.get("https://random-word-api.herokuapp.com/word?length=5")
    return response.content.decode("utf-8").strip("[\"]").upper()

async def text_to_code(message):
    """
    Get message from user in CODE_CHANNEL_ID then send that message in code block 
    """
    user = message.author
    msg = message.content
    lang = msg.split()[0]
    code = msg[len(lang):]

    await message.channel.send(f"```{lang}\nFrom: {user}\n\n{code}```")
    await message.delete()

    return

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

@client.event
async def on_ready():
    print("Potato")

@client.event
async def on_message(message):
    """
    Main program
    """
    if message.author == client.user:
        return
    
    msg_channel = str(message.channel.id)
    
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