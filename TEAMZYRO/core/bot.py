import sys
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
import config

from ..logging import LOGGER  # Make sure your folder structure supports this


class ZYRO(Client):
    def init(self, session_name: str = "ZYROMUSIC", in_memory: bool = False):
        """
        session_name : name of the session (persistent if in_memory=False)
        in_memory : whether to keep session in memory only
        """
        LOGGER(name).info("Starting Bot...")
        super().init(
            name=session_name,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=in_memory,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        # Store bot info
        self.id = self.me.id
        self.name = f"{self.me.first_name} {self.me.last_name or ''}".strip()
        self.username = self.me.username
        self.mention = self.me.mention

        # Send startup message to log channel
        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ : {self.name}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
                ),
                parse_mode=ParseMode.HTML,
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(name).error(
                "Bot cannot access the log group/channel. "
                "Make sure the bot is added to your log group/channel."
            )
            sys.exit(1)
        except Exception as ex:
            LOGGER(name).error(
                f"Failed to send startup message.\nReason: {type(ex).name}: {ex}"
            )
            sys.exit(1)

        # Check if bot is admin in log channel
        try:
            member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(name).error(
                    "Bot is not an admin in the log group/channel. Please promote it."
                )
                sys.exit(1)
        except Exception as ex:
            LOGGER(name).error(
                f"Failed to verify admin status.\nReason: {type(ex).name}: {ex}"
            )
            sys.exit(1)

        LOGGER(name).info(f"Music Bot Started as {self.name} (@{self.username})")

    async def stop(self):
        await super().stop()
        LOGGER(name).info("Bot stopped successfully.")