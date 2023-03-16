import requests
from module.dis_com import *

solution = ""
meaning = ""
times_ans = 0
sol_dict = dict()
guess_meaning = str()

WORD_URL = "https://random-word-api.herokuapp.com/word?length=5"
DICT_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

async def generate_5_letter_word():
    """
    Get random 5-letter word from random-word-api.herokuapp
    """
    response = requests.get("https://random-word-api.herokuapp.com/word?length=5")
    return response.content.decode("utf-8").strip("[\"]").upper()

async def has_meaning(word: str, is_solution: bool):
    """
    Return True if word has meaning in dictionaryapi
    """
    temp = requests.get(DICT_URL + word).json()
    try: 
        temp = temp[0]["meanings"][0]["definitions"][0]["definition"]
        if (is_solution):
            global meaning
            meaning = temp
        global guess_meaning
        guess_meaning = temp
    except:
        return False
    return True

async def init_wordle():
    global solution, meaning, sol_dict
    sol_dict = dict()
    solution = await generate_5_letter_word()

    while (not await has_meaning(solution, True)):
        solution = await generate_5_letter_word()

    for i in range(5):
        char = solution[i]
        sol_dict[char] = solution.count(char)
    return solution, meaning
    
async def play_wordle(message):
    """
    Wordle main program
    """
    global times_ans

    msg = message.content.upper()

    if (len(msg) != 5):
        await send_msg(message, "5-letter word only. Please try again.", True)
        return

    if (not await has_meaning(msg, False)):
        await send_msg(message, f"No Definitions Found.", True)
        return

    times_ans += 1
    result = check_ans(msg)

    if (result == solution):
        await send_msg(message, f"```{times_ans} tries\n{solution} - {meaning}```", True)
        times_ans  = 0
    else:
        await send_msg(message, f"```{times_ans} tries\n{result}\n{msg} - {guess_meaning}```", True)
        if times_ans == 6:
            times_ans = 0
            await send_msg(message, f"```{solution} - {meaning}```", True)

def check_ans(guess: str):
    """
    Return how close your guess was to the word.
    """
    result = ["" for i in range(5)]
    
    gue_dict = dict()
    now_dict = dict()

    for i in range(5):
        char = guess[i]
        if (char in solution):
            gue_dict[char] = guess.count(char)
            now_dict[char] = 0

    # Correct cases
    for i in range(5):
        char = guess[i]
        if (char == solution[i]):
            now_dict[char] += 1
            result[i] = char

    # Wrong cases/spot
    for i in range(5):
        char = guess[i]
        if (result[i] != ""):
            continue
        if (char in solution and now_dict[char] < sol_dict[char]):
            now_dict[char] += 1
            result[i] = char.lower()
        # Absent cases
        else:
            result[i] = "-"
    
    return "".join(result)