# import discord
# import openai
# import asyncio
# from os import getenv
# from dotenv import load_dotenv

# load_dotenv('.env')

# TOKEN = getenv("TOKEN")
# OPENAI_API_KEY = getenv("OPENAI_API_KEY")
# CODE_CHANNEL_ID = getenv("CODE_CHANNEL_ID")
# CHATGPT_CHANNEL_ID = getenv("CHATGPT_CHANNEL_ID")
# WORDLE_CHANNEL_ID = getenv("WORDLE_CHANNEL_ID")

# client = discord.Client(intents=discord.Intents(members=True, message_content=True, guild_messages=True, guild_reactions=True, guilds=True))
# openai.api_key = OPENAI_API_KEY

# solution = ""
# meaning = ""
# times_ans = 0

# async def play_wordle(message):
#     global times_ans
#     if (times_ans == 0):
#         global solution, meaning
#         temp = generate_5_letter_word().split()
#         solution = temp[0]
#         meaning = temp[2]
#     times_ans += 1
#     result = check_ans(message.content)
#     msg_channel = message.channel
#     if (result == solution):
#         await msg_channel.send(f"```{times_ans} tries\n{solution} - {meaning}```")
#     else:
#         await msg_channel.send(f"```{times_ans} tries\n{result}```")
#         if times_ans == 6:
#             times_ans = 0
#             await msg_channel.send(f"{solution} - {meaning}")

# def check_ans(guess):
#     result = ""

#     # https://github.com/dgvai/wordle-algorithm/blob/master/wordle.py
#     splitSolution = list(solution)
#     splitGuess = list(guess)

#     solutionCharsTaken = list(map(lambda x: False, splitSolution))

#     statuses = [None] * len(guess)
#     for (i, letter) in enumerate(splitGuess):
#         if(letter == splitSolution[i]):
#             statuses[i] = 'correct'
#             solutionCharsTaken[i] = True
#             continue
    
#     # Absent Cases

#     for (i, letter) in enumerate(splitGuess):

#         if(statuses[i]) : continue

#         if(letter not in splitSolution):
#             statuses[i] = 'absent'
#             continue

#         # Present Cases
        
#         indexOfPresentChar = splitSolution.index(letter) if not solutionCharsTaken[splitSolution.index(letter)] else -1

#         if(indexOfPresentChar > -1):
#             statuses[i] = 'present'
#             solutionCharsTaken[indexOfPresentChar] = True
#             continue
#         else:
#             statuses[i] = 'absent'
#             continue
    
#     for (i, item) in enumerate(statuses):
#         if (item == 'correct'):
#             result += solution[i]
#         elif (item == 'present'):
#             result += "/"
#         else:
#             result += "-"
#     return result

# def generate_5_letter_word():
#     # response = ask_chat_gpt("generate 5-letter word")
#     # while (response["choices"][0]["finish_reason"] == "null"):
#     #     response = ask_chat_gpt("generate 5-letter word")
#     return ask_chat_gpt("generate 5-letter word")["choices"][0]["message"]["content"]

# async def text_to_code(message):
#     user = message.autho
#     msg = message.content
#     lang = msg.split()[0]
#     code = msg[len(lang):]

#     await message.channel.send(f"```{lang}\nFrom: {user}\n\n{code}```")
#     await message.delete()

#     return

# async def ask_chat_gpt(msg):
#     response = openai.ChatCompletion.create(
#         model = "gpt-3.5-turbo",
#         messages = [
#             {"role": "user", "content": msg}
#         ]
#     )

#     return response

# async def return_ans(message):
#     msg = message.content + " please make response message under 2000 letters"
#     response = ask_chat_gpt(msg)
#     res_choices = response["choices"][0]
#     res_msg = res_choices["message"]["content"]

#     if res_choices["finish_reason"] != "null":
#         await message.channel.send(res_msg, reference=message)
#     else:
#         await message.channel.send("API request failed", reference=message)

#     return

# @client.event
# async def on_ready():
#     print("Potato")

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     msg_channel = str(message.channel.id)

#     if (msg_channel == CODE_CHANNEL_ID):
#         await text_to_code(message)
#     elif (msg_channel == CHATGPT_CHANNEL_ID):
#         await ask_chat_gpt(message)
#     elif (msg_channel == WORDLE_CHANNEL_ID):
#         await play_wordle(message)
#     # print(msg_channel)

# client.run(TOKEN)
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
async def play_wordle(message):
    global times_ans
    if (times_ans == 0):
        global solution, meaning
        temp = generate_5_letter_word().split()
        solution = temp[0]
        meaning = temp[2]
    times_ans += 1
    result = check_ans(message.content)
    msg_channel = message.channel
    if (result == solution):
        await msg_channel.send(f"```{times_ans} tries\n{solution} - {meaning}```")
    else:
        await msg_channel.send(f"```{times_ans} tries\n{result}```")
        if times_ans == 6:
            times_ans = 0
            await msg_channel.send(f"{solution} - {meaning}")

def check_ans(guess):
    result = ""

    # https://github.com/dgvai/wordle-algorithm/blob/master/wordle.py
    splitSolution = list(solution)
    splitGuess = list(guess)

    solutionCharsTaken = list(map(lambda x: False, splitSolution))

    statuses = [None] * len(guess)
    for (i, letter) in enumerate(splitGuess):
        if(letter == splitSolution[i]):
            statuses[i] = 'correct'
            solutionCharsTaken[i] = True
            continue
    
    # Absent Cases

    for (i, letter) in enumerate(splitGuess):

        if(statuses[i]) : continue

        if(letter not in splitSolution):
            statuses[i] = 'absent'
            continue

        # Present Cases
        
        indexOfPresentChar = splitSolution.index(letter) if not solutionCharsTaken[splitSolution.index(letter)] else -1

        if(indexOfPresentChar > -1):
            statuses[i] = 'present'
            solutionCharsTaken[indexOfPresentChar] = True
            continue
        else:
            statuses[i] = 'absent'
            continue
    
    for (i, item) in enumerate(statuses):
        if (item == 'correct'):
            result += solution[i]
        elif (item == 'present'):
            result += "/"
        else:
            result += "-"
    return result

def generate_5_letter_word():
    response = ask_chat_gpt("generate 5-letter word")
    # while (response["choices"][0]["finish_reason"] == "null"):
    #     response = ask_chat_gpt("generate 5-letter word")
    return ask_chat_gpt("generate 5-letter word")["choices"][0]["message"]["content"]

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