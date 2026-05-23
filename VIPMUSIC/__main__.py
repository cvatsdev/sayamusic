import asyncio
import importlib
import sys

from pyrogram import idle

import config
from config import BANNED_USERS
from VIPMUSIC import HELPABLE, LOGGER, app, userbot
from VIPMUSIC.core.call import VIP
from VIPMUSIC.plugins import ALL_MODULES
from VIPMUSIC.utils.database import get_banned_users, get_gbanned


async def init():
    # Validate required environment variables
    if not config.API_ID or not config.API_HASH or not config.BOT_TOKEN:
        LOGGER("VIPMUSIC").error(
            "❌ CRITICAL: Missing required environment variables!\n"
            "Please set: API_ID, API_HASH, and BOT_TOKEN\n"
            "Get them from: https://my.telegram.org/apps"
        )
        return False

    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("VIPMUSIC").error(
            "❌ No Assistant Clients Vars Defined!.. Exiting Process.\n"
            "Set at least one of: STRING_SESSION, STRING_SESSION2, STRING_SESSION3, STRING_SESSION4, STRING_SESSION5"
        )
        return False

    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("VIPMUSIC").warning(
            "⚠️ No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )

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
    try:
        await app.start()
        LOGGER("VIPMUSIC").info("✅ Main Bot Started Successfully")
    except Exception as e:
        LOGGER("VIPMUSIC").error(f"❌ Failed to start main bot: {str(e)}")
        return False

    # Load plugins
    try:
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(all_module)

            if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
                if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                    HELPABLE[imported_module.__MODULE__.lower()] = imported_module
        LOGGER("VIPMUSIC.plugins").info("✅ Successfully Imported All Modules ")
    except Exception as e:
        LOGGER("VIPMUSIC").error(f"❌ Failed to load plugins: {str(e)}")

    # Start userbot (assistant clients)
    try:
        await userbot.start()
        LOGGER("VIPMUSIC").info("✅ Assistant Clients Started Successfully")
    except Exception as e:
        LOGGER("VIPMUSIC").error(f"❌ Failed to start assistant clients: {str(e)}")
        # Don't return False here - bot can still work without assistants

    # Start voice client
    try:
        await VIP.start()
        await VIP.decorators()
        LOGGER("Saya").info("✅ Voice Client Started Successfully")
    except Exception as e:
        LOGGER("VIPMUSIC").error(f"⚠️ Failed to start voice client: {str(e)}")
        # Don't return False here - bot can still work without voice

    LOGGER("Saya").info("🎵 Saya Music Bot Started Successfully!")
    await idle()
    return True


if __name__ == "__main__":
    try:
        result = asyncio.get_event_loop_policy().get_event_loop().run_until_complete(init())
        if result is False:
            LOGGER("Saya").error("❌ Startup failed due to missing configuration")
            sys.exit(1)
    except Exception as e:
        LOGGER("Saya").error(f"❌ Unexpected error during startup: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        LOGGER("Saya").info("Bot stopped by user")
        sys.exit(0)
