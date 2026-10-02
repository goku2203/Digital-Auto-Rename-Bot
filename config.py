# Runtime/deployment configuration. Edit BotSettings in bot_settings.py for UI text,
# rename defaults and other user-facing settings.
import os
import re
import time

id_pattern = re.compile(r'^\d+

class Config:
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    BOT = None

    STRING_SESSION = os.environ.get("STRING_SESSION", "")

    DB_NAME = os.environ.get("DB_NAME", "Digital_Auto_Rename_Bot")
    DB_URL = os.environ.get("DB_URL", "")

    ADMIN = [int(admin) for admin in os.environ.get("ADMIN", "").split() if admin and id_pattern.match(admin)]
    LOG_CHANNEL = int(os.environ["LOG_CHANNEL"]) if os.environ.get("LOG_CHANNEL") else None

    FREE_UPLOAD_LIMIT = BotSettings.FREE_UPLOAD_LIMIT
    UPLOAD_LIMIT_MODE = bool(os.environ.get("UPLOAD_LIMIT_MODE", "true").lower() == "true")
    PREMIUM_MODE = bool(os.environ.get("PREMIUM_MODE", "true").lower() == "true")

    FORCE_SUB = os.environ.get("FORCE_SUB", "").lstrip("@") or None
    PORT = int(os.environ.get("PORT", "8080"))
    BOT_UPTIME = time.time()

from bot_settings import BotSettings

Config_RKN_PIC = BotSettings.START_PIC

class rkn:
    START_TXT = BotSettings.START_TEXT
    ABOUT_TXT = BotSettings.ABOUT_TEXT
    HELP_TXT = BotSettings.HELP_TEXT
    THUMBNAIL = BotSettings.THUMBNAIL_TEXT
    CAPTION = BotSettings.CAPTION_TEXT
    BOT_STATUS = BotSettings.BOT_STATUS_TEXT
    LIVE_STATUS = BotSettings.LIVE_STATUS_TEXT
    DEV_TXT = """<b><u>Sᴩᴇᴄɪᴀʟ Tʜᴀɴᴋꜱ & Dᴇᴠᴇʟᴏᴩᴇʀꜱ</b></u>

» 𝗦𝗢𝗨𝗥𝗖𝗘 𝗖𝗢𝗗𝗘 : <a href=https://github.com/DigitalBotz/Digital-Auto-Rename-Bot>Digital-Auto-Rename-Bot</a>

• ❣️ <a href=https://github.com/RknDeveloper>RknDeveloper</a>
• ❣️ <a href=https://github.com/DigitalBotz>DigitalBotz</a>
• ❣️ <a href=https://github.com/JayMahakal98>Jay Mahakal</a>"""
    RKN_PIC = BotSettings.START_PIC
    RKN_PROGRESS = """<b>

⦿ 📈 𝙿𝚛𝚘𝚐𝚛𝚎𝚜𝚜  : {0}%
⦿ 📦 𝚂𝚒𝚣𝚎      : {1} / {2}
⦿ ⚡ 𝚂𝚙𝚎𝚎𝚍     : {3}/s
⦿ ⏳ 𝙴𝚃𝙰       : {4}

════ 「 Please wait... 」 ════
</b>"""
)

class Config:
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    BOT = None

    STRING_SESSION = os.environ.get("STRING_SESSION", "")

    DB_NAME = os.environ.get("DB_NAME", "Digital_Auto_Rename_Bot")
    DB_URL = os.environ.get("DB_URL", "")

    ADMIN = [int(admin) for admin in os.environ.get("ADMIN", "").split() if admin and id_pattern.match(admin)]
    LOG_CHANNEL = int(os.environ["LOG_CHANNEL"]) if os.environ.get("LOG_CHANNEL") else None

    FREE_UPLOAD_LIMIT = 6442450944
    UPLOAD_LIMIT_MODE = bool(os.environ.get("UPLOAD_LIMIT_MODE", "true").lower() == "true")
    PREMIUM_MODE = bool(os.environ.get("PREMIUM_MODE", "true").lower() == "true")

    FORCE_SUB = os.environ.get("FORCE_SUB", "").lstrip("@") or None
    PORT = int(os.environ.get("PORT", "8080"))
    BOT_UPTIME = time.time()

from bot_settings import BotSettings

Config_RKN_PIC = BotSettings.START_PIC

class rkn:
    START_TXT = BotSettings.START_TEXT
    ABOUT_TXT = BotSettings.ABOUT_TEXT
    HELP_TXT = BotSettings.HELP_TEXT
    THUMBNAIL = BotSettings.THUMBNAIL_TEXT
    CAPTION = BotSettings.CAPTION_TEXT
    BOT_STATUS = BotSettings.BOT_STATUS_TEXT
    LIVE_STATUS = BotSettings.LIVE_STATUS_TEXT
    DEV_TXT = """<b><u>Sᴩᴇᴄɪᴀʟ Tʜᴀɴᴋꜱ & Dᴇᴠᴇʟᴏᴩᴇʀꜱ</b></u>

» 𝗦𝗢𝗨𝗥𝗖𝗘 𝗖𝗢𝗗𝗘 : <a href=https://github.com/DigitalBotz/Digital-Auto-Rename-Bot>Digital-Auto-Rename-Bot</a>

• ❣️ <a href=https://github.com/RknDeveloper>RknDeveloper</a>
• ❣️ <a href=https://github.com/DigitalBotz>DigitalBotz</a>
• ❣️ <a href=https://github.com/JayMahakal98>Jay Mahakal</a>"""
    RKN_PIC = BotSettings.START_PIC
    RKN_PROGRESS = """<b>

⦿ 📈 𝙿𝚛𝚘𝚐𝚛𝚎𝚜𝚜  : {0}%
⦿ 📦 𝚂𝚒𝚣𝚎      : {1} / {2}
⦿ ⚡ 𝚂𝚙𝚎𝚎𝚍     : {3}/s
⦿ ⏳ 𝙴𝚃𝙰       : {4}

════ 「 Please wait... 」 ════
</b>"""
