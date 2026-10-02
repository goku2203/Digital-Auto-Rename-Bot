# Central editable bot settings and UI text.
# Keep deployment secrets in environment variables; do not hardcode them here.

import os

class BotSettings:
    START_PIC = os.environ.get("RKN_PIC", "https://files.catbox.moe/94kw2e.jpg")
    FORCE_SUB = os.environ.get("FORCE_SUB", "anime_love9").lstrip("@")
    LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "")
    FREE_UPLOAD_LIMIT = 0  # Fixed the missing attribute error

    START_TEXT = """<b>Hi {} 👋

Welcome to the Advanced Rename Bot! 🚀

What I can do:
• Rename your files easily 📁
• Change or add custom thumbnails 🖼️
• Convert Video to File & File to Video 🔄
• Set custom captions for your files 📝

Created By : @Goku_Stark 💞</b>"""

    ABOUT_TEXT = """<b>╭───────────⍟
├🤖 ᴍy ɴᴀᴍᴇ : {}
├🖥️ Dᴇᴠᴇʟᴏᴩᴇʀꜱ : {}
├👨‍💻 Pʀᴏɢʀᴀᴍᴇʀ : {}
├📕 Lɪʙʀᴀʀy : {}
├✏️ Lᴀɴɢᴜᴀɢᴇ: {}
├💾 Dᴀᴛᴀ Bᴀꜱᴇ: {}
├📊 ᴠᴇʀsɪᴏɴ: <a href=https://github.com/DigitalBotz/Digital-Auto-Rename-Bot>{}</a></b>
╰───────────────⍟ """

    HELP_TEXT = """<b>•></b> /start Tʜᴇ Bᴏᴛ.

✏️ <b><u>Hᴏᴡ Tᴏ Rᴇɴᴀᴍᴇ A Fɪʟᴇ</u></b>
<b>•></b> Sᴇɴᴅ Aɴʏ Fɪʟᴇ Aɴᴅ ᴄʜᴏᴏsᴇ Tʜᴇ Oᴜᴛᴘᴜᴛ Fᴏʀᴍᴀᴛ.
ℹ️ <a href=https://t.me/DigitalBotz_Support>SUPPORT GROUP</a>"""

    THUMBNAIL_TEXT = """🌌 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Tʜᴜᴍʙɴᴀɪʟ</u></b>

<b>•></b> Sᴇɴᴅ Aɴʏ Pʜᴏᴛᴏ Tᴏ Sᴇᴛ A Pᴇʀᴍᴀɴᴇɴᴛ Tʜᴜᴍʙɴᴀɪʟ.
<b>•></b> /del_thumb - delete thumbnail.
<b>•></b> /view_thumb - view thumbnail."""

    CAPTION_TEXT = """📑 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Cᴜsᴛᴏᴍ Cᴀᴩᴛɪᴏɴ</u></b>

<b>•></b> /set_caption - set caption.
<b>•></b> /see_caption - view caption.
<b>•></b> /del_caption - delete caption."""

    BOT_STATUS_TEXT = """⚡️ ʙᴏᴛ sᴛᴀᴛᴜs ⚡️

⌚️ ʙᴏᴛ ᴜᴩᴛɪᴍᴇ: `{}`
👭 ᴛᴏᴛᴀʟ ᴜsᴇʀs: `{}`
💸 ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs: `{}`
֍ ᴜᴘʟᴏᴀᴅ: `{}`
⊙ ᴅᴏᴡɴʟᴏᴀᴅ: `{}`"""

    LIVE_STATUS_TEXT = """⚡ ʟɪᴠᴇ sᴇʀᴠᴇʀ sᴛᴀᴛᴜs ⚡

ᴜᴘᴛɪᴍᴇ: `{}`
ᴄᴘᴜ: `{}%`
ʀᴀᴍ: `{}%`
ᴛᴏᴛᴀʟ ᴅɪsᴋ: `{}`
ᴜsᴇᴅ sᴘᴀᴄᴇ: `{} {}%`
ғʀᴇᴇ sᴘᴀᴄᴇ: `{}`
ᴜᴘʟᴏᴀᴅ: `{}`
ᴅᴏᴡɴʟᴏᴀᴅ: `{}`
V3 [STABLE]"""

    MODE_AUTO = "🤖 Auto"
    MODE_MANUAL = "✍️ Manual"
    CANCEL_BUTTON = "✖️ Cancel"

    OUTPUT_TYPE_LABELS = {
        "doc": "📁 DOCUMENT",
        "video": "🎥 VIDEO",
        "audio": "🎵 AUDIO",
    }

    AUTO_FORMATS = {
        "movie": "{title} ({year}) {quality} {source} {video_codec} {language}.{ext}",
        "series": "{title} {season}{episode} {quality} {source} {video_codec}.{ext}",
        "music": "{title} - {language} ({year}).{ext}",
        "doc": "{title} ({quality}).{ext}",
        "custom": "{title} {quality} {language}.{ext}",
    }
