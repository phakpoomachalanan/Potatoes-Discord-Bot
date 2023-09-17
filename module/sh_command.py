import subprocess
import json
import sys
from os import getenv, execv
from dotenv import load_dotenv
import module.dis_com as dis

load_dotenv('.env')
GIT_PATH = json.loads(getenv("GIT_PATH"))

async def command(message):
    msg_content = message.content
    temp = str()
    if (msg_content.startswith("$")):
        sh_script = msg_content.strip("$ ")
        if (sh_script[:8] == "git pull"):
            try:
                temp = sh_script.split(", ")[1]
                path = GIT_PATH[temp]
            except KeyError:
                await dis.send_msg(message, f'```Cannot find git repo```')
            sh_script = f"git --work-tree={path} --git-dir={path}/.git pull".split()
        else:
            return
        result = subprocess.run(sh_script, stdout=subprocess.PIPE).stdout.decode("utf-8")
        if (len(result) == 0):
            result = "No output"
        await dis.send_msg(message, f'```{result}```')
        if (temp == "Potato"):
            execv(sys.executable, ['python3'] + sys.argv)
    elif (msg_content == "restart"):
        await dis.send_msg(message, '```Restarting```')
        execv(sys.executable, ['python3'] + sys.argv)
