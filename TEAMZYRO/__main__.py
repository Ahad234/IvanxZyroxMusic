import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall, GroupCallNotFoundError

import config
from TEAMZYRO import LOGGER, app, userbot
from TEAMZYRO.core.call import ZYRO
from TEAMZYRO.misc import sudo
from TEAMZYRO.plugins import ALL_MODULES
from TEAMZYRO.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    # Check string sessions
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("❌ String Session Not Filled. Please add at least one Pyrogram session.")
        exit()

    # Load sudo users
    await sudo()

    # Load banned users from database
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER("TEAMZYRO").warning(f"⚠️ Could not load banned users: {e}")

    # Start bot client
    await app.start()

    # Load plugins
    for all_module in ALL_MODULES:
        importlib.import_module("TEAMZYRO.plugins." + all_module)

    LOGGER("TEAMZYRO.plugins").info("✅ All Features Loaded Successfully!")

    # Start userbot and pytgcalls
    await userbot.start()
    await ZYRO.start()

    # Test stream to check VC
    try:
        await ZYRO.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except (NoActiveGroupCall, GroupCallNotFoundError):
        LOGGER("TEAMZYRO").warning("⚠️ No active voice chat found. Bot is running in idle mode.")
    except Exception as e:
        LOGGER("TEAMZYRO").error(f"❌ Stream start failed: {e}")

    # Load decorators
    await ZYRO.decorators()

    LOGGER("TEAMZYRO").info("╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎ MADE BY MR KARMA ☠︎︎\n╚═════ஜ۩۞۩ஜ════╝")

    # Keep bot alive
    await idle()

    # Stop all clients on exit
    await app.stop()
    await userbot.stop()
    LOGGER("TEAMZYRO").info("👋 Bot stopped. Goodbye!")


if __name__ == "__main__":
    asyncio.run(init())