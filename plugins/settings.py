from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import digital_botz


def mode_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🤖 Auto", callback_data="mode_auto"),
            InlineKeyboardButton("✍️ Manual", callback_data="mode_manual")
        ],
        [InlineKeyboardButton("✖️ Cancel", callback_data="mode_cancel")]
    ])


async def show_mode(message, user_id):
    current_mode = await digital_botz.get_rename_mode(user_id)
    mode_text = "AUTO ✅" if current_mode == "auto" else "MANUAL ✅"
    await message.reply_text(
        f"⚙️ **Rename Mode Settings**\n\n"
        f"Current Mode: **{mode_text}**\n\n"
        "Choose how the bot should handle incoming files.",
        reply_markup=mode_keyboard()
    )


@Client.on_message(filters.private & filters.command("mode"))
async def mode_command(client, message):
    await show_mode(message, message.from_user.id)


@Client.on_message(filters.private & filters.command("settings"))
async def settings_command(client, message):
    user_id = message.from_user.id
    mode = await digital_botz.get_rename_mode(user_id)
    upload_type = await digital_botz.get_upload_type(user_id)
    mode_text = "🤖 AUTO" if mode == "auto" else "✍️ MANUAL"
    type_text = {
        "doc": "📁 DOCUMENT",
        "video": "🎥 VIDEO",
        "audio": "🎵 AUDIO",
    }.get(upload_type, "Not set")

    await message.reply_text(
        "⚙️ **Your Settings**\n\n"
        f"◈ Rename Mode: **{mode_text}**\n"
        f"◈ Output Type: **{type_text}**\n\n"
        "Choose an option below:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 Rename Mode", callback_data="mode")],
            [InlineKeyboardButton("📤 Output Type", callback_data="settings_type")],
            [InlineKeyboardButton("✖️ Cancel", callback_data="settings_cancel")]
        ])
    )


@Client.on_callback_query(filters.regex(r"^settings_type$"))
async def settings_type_callback(client, query):
    current = await digital_botz.get_upload_type(query.from_user.id)
    current_text = {
        "doc": "DOCUMENT",
        "video": "VIDEO",
        "audio": "AUDIO",
    }.get(current, "NOT SET")

    await query.message.edit_text(
        f"📤 **Output Type**\n\nCurrent: **{current_text}**\n\nSelect your default output type:",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📁 Document", callback_data="settings_type_doc"),
                InlineKeyboardButton("🎥 Video", callback_data="settings_type_video")
            ],
            [InlineKeyboardButton("🎵 Audio", callback_data="settings_type_audio")],
            [InlineKeyboardButton("◀️ Back", callback_data="settings_back")],
            [InlineKeyboardButton("✖️ Cancel", callback_data="settings_cancel")]
        ])
    )
    await query.answer()


@Client.on_callback_query(filters.regex(r"^settings_type_(doc|video|audio)$"))
async def settings_type_select(client, query):
    selected = query.data.rsplit("_", 1)[-1]
    await digital_botz.set_upload_type(query.from_user.id, selected)
    label = {"doc": "DOCUMENT", "video": "VIDEO", "audio": "AUDIO"}[selected]
    await query.message.edit_text(
        f"✅ **Output Type Saved**\n\nDefault output: **{label}**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙️ Back to Settings", callback_data="settings_back")],
            [InlineKeyboardButton("✖️ Cancel", callback_data="settings_cancel")]
        ])
    )
    await query.answer(f"{label} saved ✅")


@Client.on_callback_query(filters.regex(r"^settings_back$"))
async def settings_back(client, query):
    mode = await digital_botz.get_rename_mode(query.from_user.id)
    upload_type = await digital_botz.get_upload_type(query.from_user.id)
    mode_text = "🤖 AUTO" if mode == "auto" else "✍️ MANUAL"
    type_text = {"doc": "📁 DOCUMENT", "video": "🎥 VIDEO", "audio": "🎵 AUDIO"}.get(upload_type, "Not set")
    await query.message.edit_text(
        "⚙️ **Your Settings**\n\n"
        f"◈ Rename Mode: **{mode_text}**\n"
        f"◈ Output Type: **{type_text}**\n\n"
        "Choose an option below:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 Rename Mode", callback_data="mode")],
            [InlineKeyboardButton("📤 Output Type", callback_data="settings_type")],
            [InlineKeyboardButton("✖️ Cancel", callback_data="settings_cancel")]
        ])
    )
    await query.answer()


@Client.on_callback_query(filters.regex(r"^settings_cancel$"))
async def settings_cancel(client, query):
    try:
        await query.message.delete()
    except Exception:
        pass
    await query.answer()
