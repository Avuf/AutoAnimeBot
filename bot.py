#    This file is part of the AutoAnime distribution.
#    Copyright (c) 2024 Kaif_00z
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in <
# https://github.com/kaif-00z/AutoAnimeBot/blob/main/LICENSE > .

# if you are using this following code then don't forgot to give proper
# credit to t.me/kAiF_00z (github.com/kaif-00z)

import re
from traceback import format_exc
import os
import sys
import subprocess
import html

from telethon import Button, events

from core.bot import Bot
from core.executors import Executors
from database import DataBase
from database.db import mdb
from functions.info import AnimeInfo
from functions.schedule import ScheduleTasks, Var
from functions.tools import Tools, asyncio
from functions.utils import AdminUtils
from libs.ariawarp import Torrent
from libs.logger import LOGS, Reporter
from libs.subsplease import SubsPlease
from telethon.tl.functions.messages import ExportChatInviteRequest


tools = Tools()
tools.init_dir()
bot = Bot()
dB = DataBase()
subsplease = SubsPlease(dB)
torrent = Torrent()
schedule = ScheduleTasks(bot)
admin = AdminUtils(dB, bot)

async def is_requested_one(bot, event):
    user = await mdb.get_req_one(int(event.sender.id))
    if user:
        return True
    if event.sender.id in Var.OWNER:
        return True
    return False
    
async def is_requested_two(bot, event):
    user = await mdb.get_req_two(int(event.sender.id))
    if user:
        return True
    if event.sender.id in Var.OWNER:
        return True
    return False
    

@bot.on(
    events.NewMessage(
        incoming=True, pattern="^/update ?(.*)", func=lambda e: e.is_private
    )
)
async def _update(event):
    try:
        git_output = subprocess.check_output(['git', 'pull'], stderr=subprocess.STDOUT, universal_newlines=True)
        git_output_escaped = html.escape(git_output)
        update = await event.reply(f'<pre>{git_output_escaped}</pre>')
        if "Already up to date" in git_output.strip():
            return
        restart_message = await update.reply("<code>Bot Updated</code>")
        os.execl(sys.executable, sys.executable, 'bot.py')
    except subprocess.CalledProcessError as e:
        await event.reply(f'Git pull failed:\n{html.escape(e.output)}')
    except Exception as e:
        await event.reply(f'Error occurred during update: {html.escape(str(e))}')

@bot.on(
    events.NewMessage(
        incoming=True, pattern="^/start ?(.*)", func=lambda e: e.is_private
    )
)
async def _start(event):
    xnx = await event.reply("`Please Wait...`")
    msg_id = event.pattern_match.group(1)
    dB.add_broadcast_user(event.sender_id)
    btn = []
    try:
        if Var.FORCESUB_CHANNEL1 and not await is_requested_one(bot, event):
            if Var.LINK1 is None:
                result1 = await bot(ExportChatInviteRequest(
                    peer=FORCESUB_CHANNEL1,
                    request_needed=True 
                ))
                Var.LINK1 = result1.link
            btn.append([Button.url("🚀 JOIN CHANNEL", url=Var.LINK1)])
            if Var.FORCESUB_CHANNEL2 and not await is_requested_two(bot, event):
                if Var.LINK2 is None:
                    result2 = await bot(ExportChatInviteRequest(
                        peer=FORCESUB_CHANNEL2,
                        request_needed=True 
                    ))
                    Var.LINK2 = result2.link
                btn.append([Button.url("🚀 JOIN CHANNEL", url=Var.LINK2)]) 
            btn.append([Button.url("♻️ REFRESH",   url=f"https://t.me/{((await bot.get_me()).username)}?start={msg_id}")])                                    
            await event.reply("**Please Request to Join The Following Channel To Use This Bot 🫡**", buttons=btn)
    except Exception as e:
        await event.reply("err in req {e}")
 
    if msg_id:
        if msg_id.isdigit():
            msg = await bot.get_messages(Var.BACKUP_CHANNEL, ids=int(msg_id))
            await event.reply(msg)
        else:
            items = dB.get_store_items(msg_id)
            if items:
                for id in items:
                    msg = await bot.get_messages(Var.CLOUD_CHANNEL, ids=id)
                    await event.reply(file=[i for i in msg])
    else:
        if event.sender_id == Var.OWNER:
            return await xnx.edit(
                "** <                ADMIN PANEL                 > **",
                buttons=admin.admin_panel(),
            )
        await event.reply(
            f"**Enjoy Ongoing Anime's Best Encode 24/7 🫡**",
            buttons=[
                [
                    Button.url("👨‍💻 DEV", url="t.me/kaif_00z"),
                    Button.url(
                        "💖 OPEN SOURCE",
                        url="https://github.com/kaif-00z/AutoAnimeBot/",
                    ),
                ]
            ],
        )
    await xnx.delete()


@bot.on(events.callbackquery.CallbackQuery(data=re.compile("tas_(.*)")))
async def _(e):
    await tools.stats(e)


@bot.on(events.callbackquery.CallbackQuery(data="slog"))
async def _(e):
    await admin._logs(e)


@bot.on(events.callbackquery.CallbackQuery(data="sret"))
async def _(e):
    await admin._restart(e, schedule)


@bot.on(events.callbackquery.CallbackQuery(data="entg"))
async def _(e):
    await admin._encode_t(e)


@bot.on(events.callbackquery.CallbackQuery(data="butg"))
async def _(e):
    await admin._btn_t(e)


@bot.on(events.callbackquery.CallbackQuery(data="scul"))
async def _(e):
    await admin._sep_c_t(e)


@bot.on(events.callbackquery.CallbackQuery(data="cast"))
async def _(e):
    await admin.broadcast_bt(e)


@bot.on(events.callbackquery.CallbackQuery(data="bek"))
async def _(e):
    await e.edit(buttons=admin.admin_panel())


async def anime(data):
    try:
        torr = [data.get("480p"), data.get("720p"), data.get("1080p")]
        anime_info = AnimeInfo(torr[0].title)
        poster = await tools._poster(bot, anime_info)
        if dB.is_separate_channel_upload():
            chat_info = await tools.get_chat_info(bot, anime_info, dB)
            await poster.edit(
                buttons=[
                    [
                        Button.url(
                            f"EPISODE {anime_info.data.get('episode_number', '')}".strip(),
                            url=chat_info["invite_link"],
                        )
                    ]
                ]
            )
            poster = await tools._poster(bot, anime_info, chat_info["chat_id"])
        btn = [[]]
        original_upload = dB.is_original_upload()
        button_upload = dB.is_button_upload()
        for i in torr:
            try:
                filename = f"downloads/{i.title}"
                reporter = Reporter(bot, i.title)
                await reporter.alert_new_file_founded()
                await torrent.download_magnet(i.link, "./downloads/")
                exe = Executors(
                    bot,
                    dB,
                    {
                        "original_upload": original_upload,
                        "button_upload": button_upload,
                    },
                    filename,
                    AnimeInfo(i.title),
                    reporter,
                )
                result, _btn = await exe.execute()
                if result:
                    if _btn:
                        if len(btn[0]) == 2:
                            btn.append([_btn])
                        else:
                            btn[0].append(_btn)
                        await poster.edit(buttons=btn)
                    asyncio.ensure_future(exe.further_work())
                    continue
                await reporter.report_error(_btn, log=True)
            except BaseException:
                await reporter.report_error(str(format_exc()), log=True)
    except BaseException:
        LOGS.error(str(format_exc()))


try:
    bot.loop.run_until_complete(subsplease.on_new_anime(anime))
    bot.run()
except KeyboardInterrupt:
    subsplease._exit()
