import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from TEAMZYRO import LOGGER, app, userbot
from TEAMZYRO.core.call import ZYRO
from TEAMZYRO.misc import sudo
from TEAMZYRO.plugins import ALL_MODULES
from TEAMZYRO.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("String Session Not Filled, Please Fill At Least One Pyrogram Session")
        exit()

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER("TEAMZYRO").warning(f"Could not load banned users: {e}")

    await app.start()

    for all_module in ALL_MODULES:
        importlib.import_module("TEAMZYRO.plugins." + all_module)

    LOGGER("TEAMZYRO.plugins").info("All Features Loaded Successfully ✅")

    await userbot.start()
    await ZYRO.start()

    try:
        await ZYRO.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("TEAMZYRO").warning("Voice chat not active. Bot is idle.")
    except Exception as e:
        LOGGER("TEAMZYRO").error(f"Stream failed: {e}")

    await ZYRO.decorators()

    LOGGER("TEAMZYRO").info("╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎ MADE BY MR KARMA ☠︎︎\n╚═════ஜ۩۞۩ஜ════╝")

    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("TEAMZYRO").info("Bot Stopped. Goodbye 👋")


if __name__ == "__main__":
    asyncio.run(init())