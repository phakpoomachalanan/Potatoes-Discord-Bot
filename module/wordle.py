import requests
import string
import module.dis_com as dis

solution = ""
meaning = ""
times_ans = 0
sol_dict = dict()
guess_meaning = str()
keyboard = dict()

WORD_URL = "https://random-word-api.herokuapp.com/word?length=5"
DICT_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

async def generate_5_letter_word():
    """
    Get random 5-letter word from random-word-api.herokuapp
    """
    response = requests.get(WORD_URL)
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
    except KeyError:
        # KeyError: 0 => no respose from request
        return False
    return True

async def init_wordle():
    global solution, meaning, sol_dict, times_ans, keyboard

    times_ans  = 0

    sol_dict = dict()
    solution = await generate_5_letter_word().upper()
    print(solution)

    while (not await has_meaning(solution, True)):
        solution = await generate_5_letter_word()

    for i in range(5):
        char = solution[i]
        sol_dict[char] = solution.count(char)
    
    keyboard = {key: False for key in string.ascii_uppercase}
    
async def play_wordle(message):
    """
    Wordle main program
    """
    global times_ans

    msg = message.content.strip().upper()

    if ('-' in msg):
        if (msg == "help-me"):
            return
        elif (msg == "key-left"):
            get_key(True)
        elif (msg == "key-used"):
            return
        else:
            return

    if (len(msg) != 5):
        await dis.send_msg(message, "5-letter word only. Please try again.", True)
        return

    if (not await has_meaning(msg, False)):
        await dis.send_msg(message, "No Definitions Found.", True)
        return

    times_ans += 1
    result = check_ans(msg)

    if (msg == solution):
        await dis.send_msg(message, f"{result}\n```{times_ans} tries\n{msg} - {meaning}```", True)
        await init_wordle()
    else:
        await dis.send_msg(message, f"{result}\n```{times_ans} tries\n{msg} - {guess_meaning}```", True)
        if times_ans == 6:
            await dis.send_msg(message, f"```{solution} - {meaning}```", True)
            await init_wordle()

def check_ans(guess: str):
    """
    Return how close your guess was to the word.
    """
    global keyboard
    
    result = [""] * 5
    
    gue_dict = dict()
    now_dict = dict()

    for char in guess:
        keyboard[char] = True
        if (char in solution):
            gue_dict[char] = guess.count(char)
            now_dict[char] = 0

    # Correct cases
    for i in range(5):
        char = guess[i]
        if (char == solution[i]):
            now_dict[char] += 1
            result[i] = f":regional_indicator_{char.lower()}:"

    # Wrong cases/spot
    for i in range(5):
        char = guess[i]
        if (result[i] != ""):
            continue
        if (char in solution and now_dict[char] < sol_dict[char]):
            now_dict[char] += 1
            result[i] = f" {char.upper()} "
        # Absent cases
        else:
            result[i] = ":red_square:"
    
    return " ".join(result)

def get_key(isUsed):
    """
    isUsed == True: return used keys
    isUsed == False: return unused keys
    """
    keys = list()
    for key, val in keyboard.items():
        if (val ^ isUsed):
            keys.append(key)
    return sorted(keys)