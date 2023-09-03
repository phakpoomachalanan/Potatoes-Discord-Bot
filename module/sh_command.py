import subprocess
import module.dis_com as dis

async def command(message):
    msg_content = message.content
    if (msg_content.startswith("$")):
        sh_script = msg_content.strip("$ ")
        print(sh_script)
        if (sh_script == "git pull"):
            sh_script = "git --work-tree=/home/popupie/pupserver/ZideQuest-Backend --git-dir=/home/popupie/pupserver/ZideQuest-Backend/.git pull".split()
            # sh_script = "git --work-tree=/Users/puppie/Code/Potatoes-Discord-Bot --git-dir=/Users/puppie/Code/Potatoes-Discord-Bot/.git pull".split()
            result = subprocess.run(sh_script, stdout=subprocess.PIPE).stdout.decode("utf-8")
        else:
            result = subprocess.run(sh_script, stdout=subprocess.PIPE).stdout.decode("utf-8")
        if (len(result) == 0):
            result = "No output"
        await dis.send_msg(message, f'```{result}```')