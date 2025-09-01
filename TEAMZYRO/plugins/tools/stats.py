import platform
from sys import version as pyver

import psutil
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.errors import MessageIdInvalid
from pyrogram.types import InputMediaPhoto, Message
from pytgcalls.__version__ import __version__ as pytgver

import config
from TEAMZYRO import app
from TEAMZYRO.core.userbot import assistants
from TEAMZYRO.misc import SUDOERS, mongodb
from TEAMZYRO.plugins import ALL_MODULES
from TEAMZYRO.utils.database import get_served_chats, get_served_users, get_sudoers
from TEAMZYRO.utils.decorators.language import language, languageCB
from TEAMZYRO.utils.inline.stats import back_stats_buttons, stats_buttons
from config import BANNED_USERS


# ✅ Debug added
@app.on_message(filters.command(["stats", "gstats"]) & filters.group)  # removed ~BANNED_USERS for testing
@language
async def stats_global(client, message: Message, _):
    print("✅ /stats triggered by", message.from_user.id)  # Debug log

    upl = stats_buttons(_, True if message.from_user.id in SUDOERS else False)

    try:
        await message.reply_photo(
            photo=config.STATS_IMG_URL if config.STATS_IMG_URL else "https://telegra.ph/file/6e1d9b1c8c6d9e9a9c3f6.jpg",  # fallback img
            caption=_["gstats_2"].format(app.mention),
            reply_markup=upl,
        )
    except Exception as e:
        print("❌ Error in stats_global:", e)
        await message.reply("⚠️ Stats command failed. Check logs.")


@app.on_callback_query(filters.regex("stats_back"))
@languageCB
async def home_stats(client, CallbackQuery, _):
    upl = stats_buttons(_, True if CallbackQuery.from_user.id in SUDOERS else False)
    await CallbackQuery.edit_message_text(
        text=_["gstats_2"].format(app.mention),
        reply_markup=upl,
    )


@app.on_callback_query(filters.regex("TopOverall"))
@languageCB
async def overall_stats(client, CallbackQuery, _):
    await CallbackQuery.answer()
    upl = back_stats_buttons(_)
    await CallbackQuery.edit_message_text(_["gstats_1"].format(app.mention))

    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())

    text = _["gstats_3"].format(
        app.mention,
        len(assistants),
        len(BANNED_USERS),
        served_chats,
        served_users,
        len(ALL_MODULES),
        len(SUDOERS),
        config.AUTO_LEAVING_ASSISTANT,
        config.DURATION_LIMIT_MIN,
    )

    med = InputMediaPhoto(media=config.STATS_IMG_URL, caption=text)
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(
            photo=config.STATS_IMG_URL, caption=text, reply_markup=upl
        )


@app.on_callback_query(filters.regex("bot_stats_sudo"))
@languageCB
async def bot_stats(client, CallbackQuery, _):
    if CallbackQuery.from_user.id not in SUDOERS:
        return await CallbackQuery.answer(_["gstats_4"], show_alert=True)

    upl = back_stats_buttons(_)
    await CallbackQuery.edit_message_text(_["gstats_1"].format(app.mention))

    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = str(round(psutil.virtual_memory().total / (1024.0**3))) + " ɢʙ"

    try:
        cpu_freq = psutil.cpu_freq().current
        cpu_freq = f"{round(cpu_freq / 1000, 2)}ɢʜᴢ" if cpu_freq >= 1000 else f"{round(cpu_freq, 2)}ᴍʜᴢ"
    except:
        cpu_freq = "ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ"

    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0**3)
    used = hdd.used / (1024.0**3)
    free = hdd.free / (1024.0**3)

    call = await mongodb.command("dbstats")
    datasize = call["dataSize"] / 1024
    storage = call["storageSize"] / 1024

    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())

    text = _["gstats_5"].format(
        app.mention,
        len(ALL_MODULES),
        platform.system(),
        ram,
        p_core,
        t_core,
        cpu_freq,
        pyver.split()[0],
        pyrover,
        pytgver,
        str(total)[:4],
        str(used)[:4],
        str(free)[:4],
        served_chats,
        served_users,
        len(BANNED_USERS),
        len(await get_sudoers()),
        str(datasize)[:6],
        storage,
        call["collections"],
        call["objects"],
    )

    med = InputMediaPhoto(media=config.STATS_IMG_URL, caption=text)
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(
            photo=config.STATS_IMG_URL, caption=text, reply_markup=upl
        )
