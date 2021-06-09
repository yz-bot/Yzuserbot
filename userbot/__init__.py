# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

import os
import re
import sys
import time
import asyncio
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger
from math import ceil
from sys import version_info

from dotenv import load_dotenv
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from requests import get
from telethon.sessions import StringSession
from telethon.sync import TelegramClient, custom, events
from telethon import events, Button
load_dotenv("config.env")

StartTime = time.time()

# Bot Logs setup:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get(
    "CONSOLE_LOGGER_VERBOSE") or "False")

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 8:
    LOGS.info(
        "You MUST have a python version of at least 3.8."
        "Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

# Check if the config was edited by using the already used variable.
# Basically, its the 'virginity check' for the config file ;)
CONFIG_CHECK = (os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________") or None)

if CONFIG_CHECK:
    LOGS.info(
        "Please remove the line mentioned in the first hashtag from the config.env file"
    )
    sys.exit(1)

# Telegram App KEY and HASH
API_KEY = os.environ.get("API_KEY") or None
API_HASH = os.environ.get("API_HASH") or None

# Userbot Session String
STRING_SESSION = os.environ.get("STRING_SESSION") or None

# Logging channel/group ID configuration.
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID") or None)

# Userbot logging feature switch.
BOTLOG = sb(os.environ.get("BOTLOG") or "False")
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER") or "True")

# Default .alive name
ALIVE_NAME = os.environ.get("ALIVE_NAME") or None

ALIVE_LOGO = os.environ.get(
    "ALIVE_LOGO") or "https://telegra.ph/file/f36fe8fc696203737e820.jpg"

# Default .alive username
ALIVE_USERNAME = os.environ.get("ALIVE_USERNAME") or None

# Bleep Blop, this is a bot ;)
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN") or "False")

# Heroku Credentials for updater.
HEROKU_MEMEZ = sb(os.environ.get("HEROKU_MEMEZ") or "False")
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME") or None
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY") or None

# Github Credentials for updater and Gitupload.
GIT_REPO_NAME = os.environ.get("GIT_REPO_NAME") or None
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN") or None

# Custom (forked) repo URL for updater.
UPSTREAM_REPO_URL = (os.environ.get("UPSTREAM_REPO_URL")
                     or "https://github.com/yz-bot/Yzuserbot")

# UPSTREAM_REPO_URL branch, the default is master
UPSTREAM_REPO_BRANCH = os.environ.get("UPSTREAM_REPO_BRANCH") or "YZ"

# Console verbose logging
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get(
    "CONSOLE_LOGGER_VERBOSE") or "False")

# SQL Database URI
DB_URI = os.environ.get("DATABASE_URL") or None

# Chrome Driver and Headless Google Chrome Binaries
CHROME_DRIVER = os.environ.get("CHROME_DRIVER") or "/usr/bin/chromedriver"
GOOGLE_CHROME_BIN = os.environ.get(
    "GOOGLE_CHROME_BIN") or "/usr/bin/google-chrome"

# Anti Spambot Config
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT") or "False")
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT") or "False")

# Time & Date - Country and Time Zone
COUNTRY = str(os.environ.get("COUNTRY") or "")
TZ_NUMBER = int(os.environ.get("TZ_NUMBER") or 7)

# Zipfile module
ZIP_DOWNLOAD_DIRECTORY = os.environ.get("ZIP_DOWNLOAD_DIRECTORY", "./zips")

# Clean Welcome
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME") or "True")

# Last.fm Module
BIO_PREFIX = os.environ.get("BIO_PREFIX") or None
DEFAULT_BIO = os.environ.get("DEFAULT_BIO") or None

# Google Drive Module
G_DRIVE_DATA = os.environ.get("G_DRIVE_DATA") or None
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID") or None
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET") or None
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA") or None
G_DRIVE_FOLDER_ID = os.environ.get("G_DRIVE_FOLDER_ID") or None
TEMP_DOWNLOAD_DIRECTORY = os.environ.get(
    "TMP_DOWNLOAD_DIRECTORY") or "./downloads"

# Terminal Alias
TERM_ALIAS = os.environ.get("TERM_ALIAS") or "Yz Userbot"

# Bot version
BOT_VER = os.environ.get("BOT_VER", "5.0")

CMD_HELP = {}

# JustWatch Country
WATCH_COUNTRY = os.environ.get("WATCH_COUNTRY") or None

# Inline bot helper
BOT_TOKEN = os.environ.get("BOT_TOKEN") or None
BOT_USERNAME = os.environ.get("BOT_USERNAME") or None

# bit.ly module
BITLY_TOKEN = os.environ.get("BITLY_TOKEN", None)

# Setting Up CloudMail.ru and MEGA.nz extractor binaries,
# and giving them correct perms to work properly.
if not os.path.exists("bin"):
    os.mkdir("bin")

binaries = {
    "https://raw.githubusercontent.com/adekmaulana/megadown/master/megadown": "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py": "bin/cmrudl",
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

# 'bot' variable
if STRING_SESSION:
    # pylint: disable=invalid-name
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: disable=invalid-name
    bot = TelegramClient("userbot", API_KEY, API_HASH)


async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "You must set up the BOTLOG_CHATID variable in the config.env or environment variables, for the private error log storage to work."
        )
        sys.exit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "You must set up the BOTLOG_CHATID variable in the config.env or environment variables, for the userbot logging feature to work."
        )
        sys.exit(1)

    elif not BOTLOG or not LOGSPAMMER:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Your account doesn't have rights to send messages to BOTLOG_CHATID "
            "group. Check if you typed the Chat ID correctly.")
        sys.exit(1)

with bot:
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGS.info(
            "BOTLOG_CHATID variabel lingkungan bukan sebuah"
            "entitas yang valid. Periksa variabel lingkungan/file config.env Anda.")
        quit(1)


async def check_alive():
    await bot.send_message(BOTLOG_CHATID, "**YZ USERBOT › BERHASIL DIAKTIFKAN**")
    return

with bot:
    try:
        bot.loop.run_until_complete(check_alive())
    except BaseException:
        LOGS.info(
            "BOTLOG_CHATID variabel lingkungan bukan sebuah"
            "entitas yang valid. Periksa variabel lingkungan/file config.env Anda.")
        quit(1)

def paginate_help(page_number, loaded_modules, prefix):
    number_of_rows = 5
    number_of_cols = 3
    helpable_modules = [p for p in loaded_modules if not p.startswith("_")]
    helpable_modules = sorted(helpable_modules)
    modules = [
        custom.Button.inline("{} {}".format("🍌", x), data="ub_modul_{}".format(x))
        for x in helpable_modules
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "⬅️", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    '❎', b'close'
                ),
                custom.Button.inline(
                    "➡️", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs


with bot:
    try:
        tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=API_KEY,
            api_hash=API_HASH).start(
            bot_token=BOT_TOKEN)

        dugmeler = CMD_HELP
        me = bot.get_me()
        uid = me.id
        logo = "https://telegra.ph/file/50857372d2f7fcfe13b21.jpg"


        @tgbot.on(events.NewMessage(pattern="/start"))
        async def handler(event):
            sender = await event.message.get_sender()
            text = (
                f"Hai {sender.first_name}\nSaya adalah bot assisten {ALIVE_NAME}\n\n [REPO](https://github.com/yz-bot/Yzuserbot) ...")
            await tgbot.send_file(event.chat_id, logo, caption=text,
                                  buttons=[
                                      [
                                          Button.url(
                                              text=" OFFICIAL CHANNELS ",
                                              url="https://t.me/Abcdmukakntl"
                                          )
                                      ]
                                  ]
                                  )

        @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query.startswith(""):
                buttons = paginate_help(0, dugmeler, "helpme")
                result = builder.article(
                    "Please Use Only With .help Command",
                    text="{}\nTotal loaded modules: {}".format(
                        "[YzUserbot](https://github.com/yz-bot/yzuserbot) modules helper.\n",
                        len(dugmeler),
                    ),
                    buttons=buttons,
                    link_preview=False,
                )
            elif query.startswith("tb_btn"):
                result = builder.article(
                    "Yz Helper",
                    text="List of Modules",
                    buttons=[],
                    link_preview=True,
                )
            else:
                result = builder.article(
                    "Yz",
                    text="""You can convert your account to bot and use them. Remember, you can't manage someone else's bot! All installation details are explained from GitHub address below.""",
                    buttons=[
                        [
                            custom.Button.url(
                                "GitHub Repo",
                                "https://github.com/yz-bot/Yzuserbot",
                            ),
                            custom.Button.url(
                                "Channel",
                                "https://t.me/Abcdmukakntl"),
                        ],
                    ],
                    link_preview=False,
                )
            await event.answer([result] if result else None)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_next\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number + 1, dugmeler, "helpme")
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                await event.edit("Button closed!")
            else:
                reply_pop_up_alert = f"Lu deploy sendiri lah ajg, Jangan pakai punya gw {ALIVE_NAME} "
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            
        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_prev\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number - 1, dugmeler, "helpme"  # pylint:disable=E0602
                )
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(b"ub_modul_(.*)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                modul_name = event.data_match.group(1).decode("UTF-8")

                cmdhel = str(CMD_HELP[modul_name])
                if len(cmdhel) > 150:
                    help_string = (
                        str(CMD_HELP[modul_name]).replace("`", "")[:150]
                        + "..."
                        + "\n\nRead more .help "
                        + modul_name
                        + " "
                    )
                else:
                    help_string = str(CMD_HELP[modul_name]).replace("`", "")

                reply_pop_up_alert = (
                    help_string
                    if help_string is not None
                    else "{} No document has been written for module.".format(
                        modul_name
                    )
                )
            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"

            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    except BaseException:
        LOGS.info(
            "Dukungan untuk inline dinonaktifkan pada bot Anda. "
            "Untuk mengaktifkannya, tentukan token bot dan aktifkan mode inline pada bot Anda. "
            "Jika menurut Anda ada masalah selain ini, hubungi kami.")
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGS.info(
            "BOTLOG_CHATID variabel lingkungan bukan sebuah"
            "entitas yang valid. Periksa variabel lingkungan/file config.env Anda."
        )
        sys.exit(1)

# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
ISAFK = False
AFKREASON = None
ZALG_LIST = {}
LOAD_PLUG = {}
