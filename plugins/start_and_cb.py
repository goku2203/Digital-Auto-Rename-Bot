# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support
"""
Apache License 2.0
Copyright (c) 2025 @Digital_Botz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Telegram Link : https://t.me/Digital_Botz 
Repo Link : https://github.com/DigitalBotz/Digital-Auto-Rename-Bot
License Link : https://github.com/DigitalBotz/Digital-Auto-Rename-Bot/blob/main/LICENSE
"""

# extra imports
import random, asyncio, datetime, pytz, time, psutil, shutil

# pyrogram imports
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery

# bots imports
from helper.database import digital_botz
from config import Config, rkn
from bot_settings import BotSettings
from helper.utils import humanbytes
from plugins import __version__ as _bot_version_, __developer__, __database__, __library__, __language__, __programer__
from plugins.file_rename import upload_doc


@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    start_button = [[        
        InlineKeyboardButton('Uᴩᴅᴀ𝚃ᴇꜱ', url='https://t.me/Digital_Botz'),
        InlineKeyboardButton('Sᴜᴩᴩᴏʀ𝚃', url='https://t.me/DigitalBotz_Support')
        ],[
        InlineKeyboardButton('Aʙᴏυᴛ', callback_data='about'),
        InlineKeyboardButton('Hᴇʟᴩ', callback_data='help'),
        InlineKeyboardButton('⚙️ Sᴇᴛᴛɪɴɢꜱ', callback_data='settings')
         ]]
        
    
    user = message.from_user
    await digital_botz.add_user(client, message) 
    if Config.RKN_PIC:
        await message.reply_photo(Config.RKN_PIC, caption=rkn.START_TXT.format(user.mention), reply_markup=InlineKeyboardMarkup(start_button))    
    else:
        await message.reply_text(text=rkn.START_TXT.format(user.mention), reply_markup=InlineKeyboardMarkup(start_button), disable_web_page_preview=True)

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        start_button = [[        
        InlineKeyboardButton('Uᴩᴅᴀ𝚃ᴇꜱ', url='https://t.me/Digital_Botz'),
        InlineKeyboardButton('Sᴜᴩᴩᴏʀ𝚃', url='https://t.me/DigitalBotz_Support')
        ],[
        InlineKeyboardButton('Aʙᴏυᴛ', callback_data='about'),
        InlineKeyboardButton('Hᴇʟᴩ', callback_data='help'),
        InlineKeyboardButton('⚙️ Sᴇᴛᴛɪɴɢꜱ', callback_data='settings')       
         ]]
            
        
        await query.message.edit_text(
            text=rkn.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup(start_button))
        
    elif data == "settings":
        user_id = query.from_user.id
        mode = await digital_botz.get_rename_mode(user_id)
        upload_type = await digital_botz.get_upload_type(user_id)
        mode_text = "🤖 AUTO" if mode == "auto" else "✍️ MANUAL"
        type_text = {"doc": "📁 DOCUMENT", "video": "🎥 VIDEO", "audio": "🎵 AUDIO"}.get(upload_type, "Not set")
        await query.message.edit_text(
            "⚙️ **Your Settings**\n\n"
            f"◈ Rename Mode: **{mode_text}**\n"
            f"◈ Output Type: **{type_text}**\n\nChoose an option below:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🤖 Rename Mode", callback_data="mode")],
                [InlineKeyboardButton("📤 Output Type", callback_data="settings_type")],
                [InlineKeyboardButton("✖️ Cancel", callback_data="settings_cancel")]
            ])
        )
        await query.answer()

    elif data == "mode":
        current_mode = await digital_botz.get_rename_mode(query.from_user.id)
        mode_text = "AUTO ✅" if current_mode == "auto" else "MANUAL ✅"
        await query.message.edit_text(
            f"⚙️ **Rename Mode Settings**\n\nCurrent Mode: **{mode_text}**\n\nChoose how the bot should handle incoming files.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🤖 Auto", callback_data="mode_auto"),
                 InlineKeyboardButton("✍️ Manual", callback_data="mode_manual")],
                [InlineKeyboardButton("✖️ Cancel", callback_data="mode_cancel")]
            ])
        )
        await query.answer()

    elif data == "mode_auto":
        await digital_botz.set_rename_mode(query.from_user.id, "auto")
        await query.message.edit_text(
            "✅ **Auto Mode Enabled**\n\nIncoming files will use your saved auto-rename format.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ Cancel", callback_data="mode_cancel")]])
        )
        await query.answer("Auto mode saved ✅")

    elif data == "mode_manual":
        await digital_botz.set_rename_mode(query.from_user.id, "manual")
        await query.message.edit_text(
            "✅ **Manual Mode Enabled**\n\nIncoming files will ask you for the new filename.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ Cancel", callback_data="mode_cancel")]])
        )
        await query.answer("Manual mode saved ✅")

    elif data == "mode_manual_rename":
        await query.message.edit_text(
            "✍️ **Manual Rename**\\n\\nReply to this message with the new filename.\\n\\nExample: `One Piece - 01.mkv`",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ Cancel", callback_data="mode_cancel")]])
        )
        await query.answer()

    elif data == "mode_cancel":
        try:
            await query.message.delete()
        except:
            pass
        await query.answer()

    elif data == "help":
        await query.message.edit_text(
            text=rkn.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("ᴛʜᴜᴍʙɴᴀɪʟ", callback_data = "thumbnail"),
                InlineKeyboardButton("ᴄᴀᴘᴛɪᴏɴ", callback_data = "caption")
                ],[          
                
                InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data = "about"),
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data = "start")
                
                  ]]))         
        
    elif data == "about":
        about_button = [[
         #⚠️ don't change source code & source link ⚠️ #
        InlineKeyboardButton("𝚂ᴏᴜʀᴄᴇ", callback_data = "source_code"), #Whoever is deploying this repo is given a warning ⚠️ not to remove this repo link #first & last warning ⚠️
        InlineKeyboardButton("ʙᴏᴛ sᴛᴀᴛᴜs", callback_data = "bot_status")
        ],[
        InlineKeyboardButton("ʟɪᴠᴇ sᴛᴀᴛᴜs", callback_data = "live_status")           
        ]]
        
        about_button[-1].append(InlineKeyboardButton("Bᴀᴄᴋ", callback_data = "start"))
            
        await query.message.edit_text(
            text=rkn.ABOUT_TXT.format(client.mention, __developer__, __programer__, __library__, __language__, __database__, _bot_version_),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(about_button))    
        
    

    elif data == "thumbnail":
        await query.message.edit_text(
            text=rkn.THUMBNAIL,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Bᴀᴄᴋ", callback_data = "help")]])) 
      
    elif data == "caption":
        await query.message.edit_text(
            text=rkn.CAPTION,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Bᴀᴄᴋ", callback_data = "help")]])) 
      
        
    elif data == "bot_status":
        total_users = await digital_botz.total_users_count()
        
        total_premium_users = "Disabled ✅"
        
        uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))    
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        await query.message.edit_text(
            text=rkn.BOT_STATUS.format(uptime, total_users, total_premium_users, sent, recv),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Bᴀᴄᴋ", callback_data = "about")]])) 
      
    elif data == "live_status":
        currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))    
        total, used, free = shutil.disk_usage(".")
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        await query.message.edit_text(
            text=rkn.LIVE_STATUS.format(currentTime, cpu_usage, ram_usage, total, used, disk_usage, free, sent, recv),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Bᴀᴄᴋ", callback_data = "about")]])) 
      
    elif data == "source_code":
        await query.message.edit_text(
            text=rkn.DEV_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
           #Whoever is deploying this repo is given a warning ⚠️ not to remove this repo link #first & last warning ⚠️   
                InlineKeyboardButton("💞 Sᴏᴜʀᴄᴇ Cᴏᴅᴇ 💞", url="https://github.com/DigitalBotz/Digital-Auto-Rename-Bot")
            ],[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("◀️ Bᴀᴄᴋ", callback_data = "start")
                 ]])          
        )
            
    elif data.startswith("upload"):
        await upload_doc(client, query)
            
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()

# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Update Channel @Digital_Botz & @DigitalBotz_Support
