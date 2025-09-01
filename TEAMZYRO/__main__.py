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
        LOGGER(__name__).error("𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝 ❌")
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

    # Start main app
    await app.start()

    # Load all plugins
    for all_module in ALL_MODULES:
        importlib.import_module("TEAMZYRO.plugins." + all_module)
    LOGGER("TEAMZYRO.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 🥳")

    # Start userbot
    await userbot.start()

    # Initialize ZYRO bot instance
    bot = ZYROClass()
    await bot.start()

    try:
        await bot.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("TEAMZYRO").error("𝗣𝗹𝗲𝗮𝘀𝗲 𝗦𝘁𝗮𝗿𝘁 𝗬𝗼𝘂𝗿 𝗟𝗼𝗴 𝗚𝗿𝗼𝘂𝗽 𝗩𝗼𝗶𝗰𝗲𝗖𝗵𝗮𝘁 ❗")
        sys.exit(1)

    await bot.decorators()

    LOGGER("TEAMZYRO").info("✅ Bot Successfully Started!")

    await idle()

    await app.stop()
    await userbot.stop()
    await bot.stop()
    LOGGER("TEAMZYRO").info("🛑 Bot Stopped")

if __name__ == "__main__":
    asyncio.run(init())
