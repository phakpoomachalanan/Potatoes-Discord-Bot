async def send_msg(message, msg, has_ref=False):
    if (has_ref):
        await message.channel.send(msg, reference=message)
    else:
        await message.channel.send(msg)