import sys
import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from TEAMZYRO import LOGGER, app, userbot
from TEAMZYRO.core.call import ZYRO as ZYROClass
from TEAMZYRO.misc import sudo
from TEAMZYRO.plugins import ALL_MODULES
from TEAMZYRO.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(name).error(
            "𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧"
        )
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

    # Attempt to stream
    try:
        await bot.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("TEAMZYRO").error(
            "𝗣𝗹𝗭 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\n\n𝗕𝗔𝗕𝗬 𝗟𝗢𝗕 𝗬𝗢𝗨 𝗕𝗢𝗧 𝗦𝗧𝗢𝗣........"
        )
        sys.exit(1)
    except Exception:
        pass

    # Call decorators if any
    await bot.decorators()

    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗞𝗔𝗥𝗠𝗔☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

    await idle()

    # Stop all clients
    await app.stop()
    await userbot.stop()
    await bot.stop()
    LOGGER("TEAMZYRO").info("𝗦𝗧𝗢𝗣 𝗕𝗔𝗕𝗬 𝗟𝗢𝗕 𝗠𝗨𝗦𝗜𝗖 🎻 𝗕𝗢𝗧")


if name == "main":
    asyncio.run(init())