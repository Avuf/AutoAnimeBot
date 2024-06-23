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

    API_ID = int(23363032)
    API_HASH = "74134aaa77f0d0725385377e104bf933"
    BOT_TOKEN = "6527490872:AAGneA1tbChM4JtOAhgzTg4uQ59HmBgTqKk"
    SESSION = ""
    WEB = False
    # Database Credentials

    FIREBASE_URL = config("https://auto-anime-as-default-rtdb.firebaseio.com", default=None)
    FIREBASE_SERVICE_ACCOUNT_FILE = config(
        "https://gist.githubusercontent.com/shinigamiezz/0444921a49fb188ee2205a983317ebff/raw/0bb8adcc4035dd54149ca1fcdcb9eaeb17eb9a55/service.json", default=None
    )

    MDB_URI = config("MDB_URI", default="mongodb+srv://Emiliatg:Emiliatg@cluster0.c0a2uor.mongodb.net/?retryWrites=true&w=majority")
    MDB_NAME = config("MDB_NAME", default="Cluster0")
    
    
    # Channels Ids

    BACKUP_CHANNEL = config("BACKUP_CHANNEL", default=0, cast=int)
    MAIN_CHANNEL = config("MAIN_CHANNEL", default=0, cast=int)
    LOG_CHANNEL = int(-1002219868353)
    CLOUD_CHANNEL = config("CLOUD_CHANNEL", default=0, cast=int)
    OWNER = config("OWNER", default=0, cast=int)
    FORCESUB_CHANNEL1 =config("FORCESUB_CHANNEL1", default=0, cast=int)
    FORCESUB_CHANNEL2 =config("FORCESUB_CHANNEL2", default=0, cast=int)

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
