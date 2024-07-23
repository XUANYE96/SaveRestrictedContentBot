#Tg:MaheshChauhan/DroneBots
#Github.com/Vasusen-code

"""
插件适用于公共和私有频道！
"""

import time, os, asyncio

from .. import bot as Drone
from .. import userbot, Bot, AUTH
from .. import FORCESUB as fs
from main.plugins.pyroplug import get_bulk_msg
from main.plugins.helpers import get_link, screenshot

from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo

from pyrogram import Client 
from pyrogram.errors import FloodWait

from ethon.pyfunc import video_metadata
from ethon.telefunc import force_sub

ft = f"要使用此机器人，您必须加入 @{fs}。"

batch = []

@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/cancel'))
async def cancel(event):
    if not event.sender_id in batch:
        return await event.reply("当前没有活动的批次。")
    batch.clear()
    await event.reply("已完成。")
    
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/batch'))
async def _batch(event):
    if not event.is_private:
        return
    s, r = await force_sub(event.client, fs, event.sender_id, ft) 
    if s == True:
        await event.reply(r)
        return       
    if event.sender_id in batch:
        return await event.reply("您已经开始了一个批次，请等待其完成！")
    async with Drone.conversation(event.chat_id) as conv: 
        if s != True:
            await conv.send_message("请发送您要开始保存的消息链接，作为对此消息的回复。", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("未找到链接。")
                    return conv.cancel()
            except Exception as e:
                print(e)
                await conv.send_message("无法再等待您的回复！")
                return conv.cancel()
            await conv.send_message("请发送您要从给定消息中保存的文件数量/范围，作为对此消息的回复。", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                print(e)
                await conv.send_message("无法再等待您的回复！")
                return conv.cancel()
            try:
                value = int(_range.text)
                if value > 100:
                    await conv.send_message("单个批次最多只能获取 100 个文件。")
                    return conv.cancel()
            except ValueError:
                await conv.send_message("范围必须是整数！")
                return conv.cancel()
            batch.append(event.sender_id)
            await run_batch(userbot, Bot, event.sender_id, _link, value) 
            conv.cancel()
            batch.clear()

async def run_batch(userbot, client, sender, link, _range):
    for i in range(_range):
        timer = 60
        if i < 25:
            timer = 5
        if i < 50 and i > 25:
            timer = 10
        if i < 100 and i > 50:
            timer = 15
        if not 't.me/c/' in link:
            if i < 25:
                timer = 2
            else:
                timer = 3
        try: 
            if not sender in batch:
                await client.send_message(sender, "批次已完成。")
                break
        except Exception as e:
            print(e)
            await client.send_message(sender, "批次已完成。")
            break
        try:
            await get_bulk_msg(userbot, client, sender, link, i) 
        except FloodWait as fw:
            if int(fw.x) > 299:
                await client.send_message(sender, "由于 FloodWait 超过 5 分钟，正在取消批次。")
                break
            await asyncio.sleep(fw.x + 5)
            await get_bulk_msg(userbot, client, sender, link, i)
        protection = await client.send_message(sender, f"休眠 `{timer}` 秒以避免 FloodWait 并保护帐户！")
        await asyncio.sleep(timer)
        await protection.delete()
