import asyncio
import uvloop

# Event loop ko initialize karne ka sahi tareeka
try:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    pass

try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import pyrogram
import pyromod.listen  # noqa
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import config
from ..logging import LOGGER


class VIPBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "VIPMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.mention = self.me.mention

        # Create the button
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏",
                        url=f"https://t.me/{self.username}?startgroup=true",
                    )
                ]
            ]
        )

        # Try to send a message to the logger group
        if config.LOG_GROUP_ID:
            try:
                await self.send_photo(
                    config.LOG_GROUP_ID,
                    photo=config.START_IMG_URL,
                    caption=f"Hey\n║\n║┣⪼Saya Started\n║\n║┣⪼ {self.name}\n║\n║┣⪼ID:- `{self.id}` \n║\n║┣⪼@{self.username} \n║ \n║┣⪼SAYA\n║\n❁",
                    reply_markup=button,
                )
            except pyrogram.errors.ChatWriteForbidden as e:
                LOGGER(__name__).error(f"Bot cannot write to the log group: {e}")
                try:
                    await self.send_message(
                        config.LOG_GROUP_ID,
                        f"Hey\n║\n║┣⪼Saya Started\n║\n║◈ {self.name}\n║\n║┣⪼ID:- `{self.id}` \n║\n║┣⪼@{self.username} \n║ \n║┣⪼SAYA\n║\n❁",
                        reply_markup=button,
                    )
                except Exception as e:
                    LOGGER(__name__).error(f"Failed to send message in log group: {e}")
            except Exception as e:
                LOGGER(__name__).error(
                    f"Unexpected error while sending to log group: {e}"
                )
        else:
            LOGGER(__name__).warning(
                "LOG_GROUP_ID is not set, skipping log group notifications."
            )

        # Setting commands
        if config.SET_CMDS:
            try:
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
                        BotCommand("help", "ɢᴇᴛ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ"),
                        BotCommand("ping", "ᴄʜᴇᴄᴋ ɪғ ᴛʜᴇ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "sᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ʀᴇǫᴜᴇsᴛᴇᴅ sᴏɴɢ"),
                        BotCommand("stop", "sᴛᴏᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ sᴏɴɢg"),
                        BotCommand("pause", "ᴘᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ sᴏɴɢ"),
                        BotCommand("resume", "ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴘᴀᴜsᴇᴅ sᴏɴɢ"),
                        BotCommand("queue", "ᴄʜᴇᴄᴋ ᴛʜᴇ ǫᴜᴇᴜᴇ ᴏғ sᴏɴɢs"),
                        BotCommand("skip", "sᴋɪᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ sᴏɴɢ"),
                        BotCommand("volume", "ᴀᴅᴊᴜsᴛ ᴛʜᴇ ᴍᴜsɪᴄ ᴠᴏʟᴜᴍᴇ"),
                        BotCommand("lyrics", "ɢᴇᴛ ʟʏʀɪᴄs ᴏғ ᴛʜᴇ sᴏɴɢ"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
                        BotCommand("ping", "ᴄʜᴇᴄᴋ ᴛʜᴇ ᴘɪɴɢ"),
                        BotCommand("help", "ɢᴇᴛ ʜᴇʟᴘ"),
                        BotCommand("vctag", "ᴛᴀɢ ᴀʟʟ ғᴏʀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"),
                        BotCommand("stopvctag", "sᴛᴏᴘ ᴛᴀɢɢɪɴɢ ғᴏʀ ᴠᴄ"),
                        BotCommand("tagall", "ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs ʙʏ ᴛᴇxᴛ"),
                        BotCommand("cancel", "ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴛᴀɢɢɪɴɢ"),
                        BotCommand("settings", "ɢᴇᴛ ᴛʜᴇ sᴇᴛᴛɪɴɢs"),
                        BotCommand("reload", "ʀᴇʟᴏᴀᴅ ᴛʜᴇ ʙᴏᴛ"),
                        BotCommand("play", "ᴘʟᴀʏ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ sᴏɴɢ"),
                        BotCommand("vplay", "ᴘʟᴀʏ ᴠɪᴅᴇᴏ ᴀʟᴏɴɢ ᴡɪᴛʜ ᴍᴜsɪᴄ"),
                        BotCommand("end", "ᴇᴍᴘᴛʏ ᴛʜᴇ ǫᴜᴇᴜᴇ"),
                        BotCommand("playlist", "ɢᴇᴛ ᴛʜᴇ ᴘʟᴀʏʟɪsᴛ"),
                        BotCommand("stop", "sᴛᴏᴘ ᴛʜᴇ sᴏɴɢ"),
                        BotCommand("lyrics", "ɢᴇᴛ ᴛʜᴇ sᴏɴɢ ʟʏʀɪᴄs"),
                        BotCommand("song", "ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ sᴏɴɢ"),
                        BotCommand("video", "ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ᴠɪᴅᴇᴏ sᴏɴɢ"),
                        BotCommand("gali", "ʀᴇᴘʟʏ ᴡɪᴛʜ ғᴜɴ"),
                        BotCommand("shayri", "ɢᴇᴛ ᴀ sʜᴀʏᴀʀɪi"),
                        BotCommand("love", "ɢᴇᴛ ᴀ ʟᴏᴠᴇ sʜᴀʏᴀʀɪ"),
                        BotCommand("sudolist", "ᴄʜᴇᴄᴋ ᴛʜᴇ sᴜᴅᴏ ʟɪsᴛ"),
                        BotCommand("owner", "ᴄʜᴇᴄᴋ ᴛʜᴇ ᴏᴡɴᴇʀ"),
                        BotCommand("update", "ᴜᴘᴅᴀᴛᴇ ʙᴏᴛ"),
                        BotCommand("gstats", "ɢᴇᴛ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ"),
                        BotCommand("repo", "ᴄʜᴇᴄᴋ ᴛʜᴇ ʀᴇᴘᴏ"),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER(__name__).error(f"Failed to set bot commands: {e}")

        # Check if bot is an admin in the logger group
        if config.LOG_GROUP_ID:
            try:
                chat_member_info = await self.get_chat_member(
                    config.LOG_GROUP_ID, self.id
                )
                if chat_member_info.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).error(
                        "Saya"
                    )
            except Exception as e:
                LOGGER(__name__).error(f"Saya Bug: {e}")

        LOGGER(__name__).info(f"Saya {self.name}")
