from dis_com import *
from lang import lang as language

async def text_to_code(message):
    """
    Get message from user in CODE_CHANNEL_ID then send that message in code block 
    """
    user = message.author
    msg = message.content
    lang = msg.split()[0]
    code = msg[len(lang):]

    if (lang in language):
        await send_msg(message, f"```{lang}\nFrom: {user}\n\n{code}```")
    else:
        await send_msg(message, f"```c\nFrom: {user}\n\n{msg}```")
    await message.delete()