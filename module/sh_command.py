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
    if (msg_content.startswith("$")):
        sh_script = msg_content.strip("$ ")
        if (sh_script[:8] == "git pull"):
            try:
                path = GIT_PATH[sh_script.split(", ")[1]]
            except KeyError:
                await dis.send_msg(message, f'```Cannot find git repo```')
            sh_script = f"git --work-tree={path} --git-dir={path}/.git pull".split()
        result = subprocess.run(sh_script, stdout=subprocess.PIPE).stdout.decode("utf-8")
        if (len(result) == 0):
            result = "No output"
        await dis.send_msg(message, f'```{result}```')
    elif (msg_content == "restart"):
        await dis.send_msg(message, '```Restarting```')
        execv(sys.executable, ['python3'] + sys.argv)
