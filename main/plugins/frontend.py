#Github.com/Vasusen-code

import time, os

from .. import bot as Drone
from .. import userbot, Bot
from .. import FORCESUB as fs
from main.plugins.pyroplug import get_msg
from main.plugins.helpers import get_link, join

from telethon import events
from pyrogram.errors import FloodWait

from ethon.telefunc import force_sub

ft = f"要使用此机器人，您必须加入 @{fs}。"

message = "请发送您要开始保存的消息链接，作为对此消息的回复。"

@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.text == message:
            return
    try:
        link = get_link(event.text)
        if not link:
            return
    except TypeError:
        return
    s, r = await force_sub(event.client, fs, event.sender_id, ft)
    if s == True:
        await event.reply(r)
        return
    edit = await event.reply("处理中！")
    try:
        if 't.me/+' in link:
            q = await join(userbot, link)
            await edit.edit(q)
            return
        if 't.me/' in link:
            await get_msg(userbot, Bot, Drone, event.sender_id, edit.id, link, 0)
    except FloodWait as fw:
        return await Drone.send_message(event.sender_id, f'由于 Telegram 的 FloodWait，请在 {fw.x} 秒后再试。')
    except Exception as e:
        print(e)
        await Drone.send_message(event.sender_id, f"克隆 `{link}` 时发生错误\n\n**错误:** {str(e)}")
