import asyncio
import sys
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from TEAMZYRO.core.bot import ZYRO
from TEAMZYRO.core.userbot import Userbot
from TEAMZYRO import LOGGER, api
from TEAMZYRO.core.call import ZYRO as ZYROClass
from TEAMZYRO.misc import sudo
from TEAMZYRO.plugins import ALL_MODULES
from TEAMZYRO.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# ------------------ Initialize clients here ------------------
app = ZYRO()
userbot = Userbot()

async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("❌ String Session not found. Fill at least one STRINGx in config!")
        sys.exit(1)

    await sudo()

    # Load banned users
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    # Start main bot
    await app.start()

    # Load all plugins
    for all_module in ALL_MODULES:
        importlib.import_module("TEAMZYRO.plugins." + all_module)
    LOGGER("TEAMZYRO.plugins").info("✅ All modules loaded successfully!")

    # Start userbot
    await userbot.start()

    # Initialize ZYRO Voice Call Handler
    bot = ZYROClass()
    await bot.start()

    try:
        await bot.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("TEAMZYRO").error("❌ Please start a voice chat in your LOG GROUP before running the bot.")
        sys.exit(1)

    await bot.decorators()

    LOGGER("TEAMZYRO").info("🥳 Bot started successfully!")

    await idle()

    await app.stop()
    await userbot.stop()
    await bot.stop()
    LOGGER("TEAMZYRO").info("🛑 Bot stopped successfully!")

if __name__ == "__main__":
    asyncio.run(init())
