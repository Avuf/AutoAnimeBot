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

from decouple import config


class Var:
    # Telegram Credentials

    API_ID = int(22413676)
    API_HASH = "654970bafe567f9d618a257e93660551"
    BOT_TOKEN = "7151855821:AAGHjXGoGael0vvM2sRgMXktX_zWtN4uedw"
    SESSION = ""
    WEB = False
    # Database Credentials

    FIREBASE_URL = "https://auto-anime-as-default-rtdb.firebaseio.com"
    FIREBASE_SERVICE_ACCOUNT_FILE = "https://gist.githubusercontent.com/shinigamiezz/0444921a49fb188ee2205a983317ebff/raw/0bb8adcc4035dd54149ca1fcdcb9eaeb17eb9a55/service.json"
    MDB_URI = config("MDB_URI", default="mongodb+srv://Emiliatg:Emiliatg@cluster0.c0a2uor.mongodb.net/?retryWrites=true&w=majority")
    MDB_NAME = config("MDB_NAME", default="Cluster0")
    
    
    # Channels Ids

    BACKUP_CHANNEL = config("-1002168406189", default=0, cast=int)
    MAIN_CHANNEL = config("-1002177615094", default=0, cast=int)
    LOG_CHANNEL = int(-1002247750933)
    CLOUD_CHANNEL = config("-1002204000606", default=0, cast=int)
    OWNER = int(6052897917)
                   
    FORCESUB_CHANNEL1 = int(-1002177615094)
    FORCESUB_CHANNEL2 = int(-1002168406189)

    LINK1 = None
    LINK2 = None

    # Other Configs

    THUMB = config(
        "THUMBNAIL", default="https://graph.org/file/ad1b25807b81cdf1dff65.jpg"
    )
    FFMPEG = config("FFMPEG", default="ffmpeg")
    CRF = config("CRF", default="27")
    SEND_SCHEDULE = config("SEND_SCHEDULE", default=False, cast=bool)
    RESTART_EVERDAY = config("RESTART_EVERDAY", default=True, cast=bool)
    FORCESUB_CHANNEL_LINK = config("FORCESUB_CHANNEL_LINK", default="", cast=str)
