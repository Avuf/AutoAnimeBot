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
from functions.info import AnimeInfo
from functions.schedule import ScheduleTasks, Var
from functions.tools import Tools, asyncio
from functions.utils import AdminUtils
from libs.ariawarp import Torrent
from libs.logger import LOGS, Reporter
from libs.subsplease import SubsPlease
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import UpdateChatParticipantAdd, ChannelParticipantCreator, ChannelParticipantAdmin, ChannelParticipant
from telethon.tl.functions.channels import GetParticipant, GetFullChannel, ExportInvite


tools = Tools()
tools.init_dir()
bot = Bot()
dB = DataBase()
subsplease = SubsPlease(dB)
torrent = Torrent()
schedule = ScheduleTasks(bot)
admin = AdminUtils(dB, bot)

async def is_user_joined(bot, user_id: int, channel: int):
    if user_id in Var.OWNER:
        return True
    try:
        member = await bot(GetParticipant(channel=channel, user_id=user_id))
        participant = member.participant
    except Exception as e: 
        return False
    if isinstance(participant, (ChannelParticipantCreator, ChannelParticipantAdmin, ChannelParticipant)):
        return True
    else:
        return False
        
async def get_invite_link(client, channel):
    try:
        chat_info = await client(GetFullChannel(channel=int(channel)))
        invite_link = chat_info.full_chat.exported_invite
        if invite_link:
            return invite_link.link
        else:
            link = await client(ExportInvite(channel=int(channel)))
            return link.link
    except RPCError as e:
        return f"https://t.me/{channel}"
    
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
        non_member_channels = [channel for channel in Var.AUTH_CHANNELS if not await is_user_joined(bot, event.sender_id, int(channel))]
        if non_member_channels:
            m = await message.reply(f"<code>please wait...</code>")
            buttons = [
                [InlineKeyboardButton("Join Channel", url= await get_invite_link(bot, channel))] for channel in non_member_channels
            ]
            if msg_id:
                buttons.append([Button.url("♻️ REFRESH",   url=f"https://t.me/{((await bot.get_me()).username)}?start={msg_id}")])                                    
            await xnx.edit("**Please Join The Following Channel To Use This Bot 🫡**", buttons=buttons)
    except Exception as e:
        await event.reply(f"err in {e}\n\n{format_exc()}")
    
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
        if event.sender_id in Var.OWNER:
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

@bot.on(events.ChatAction)
async def join_reqs(event):
    if isinstance(event.action_message.action, UpdateChatParticipantAdd):
        user_id = event.action_message.action.user_id
        chat_id = event.chat_id  
        try:
            if chat_id == REQ_CHANNEL1:
                await mdb.add_req_one(user_id)
            elif chat_id == REQ_CHANNEL2:
                await mdb.add_req_two(user_id)
        except Exception as e:
            print(f"Error adding join request: {e}")

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
