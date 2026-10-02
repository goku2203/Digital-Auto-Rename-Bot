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

import aiohttp, asyncio, warnings, pytz, datetime
import logging

from pyrogram import Client, __version__, errors
from pyrogram.raw.all import layer
from pyrogram import idle

from config import Config
from plugins.web_support import web_server
from plugins.file_rename import app

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler('BotLog.txt'), logging.StreamHandler()]
)
logging.getLogger("pyrofork").setLevel(logging.WARNING)

class DigitalAutoRenameBot(Client):
    def __init__(self):
        super().__init__(
            name="DigitalRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            sleep_threshold=5,
            max_concurrent_transmissions=50
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = Config.BOT_UPTIME
        self.premium = Config.PREMIUM_MODE
        self.uploadlimit = Config.UPLOAD_LIMIT_MODE
        Config.BOT = self

        app = aiohttp.web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await aiohttp.web.TCPSite(app, bind_address, Config.PORT).start()

        # Import each plugin exactly once. Dynamic re-importing duplicates handlers and can break the bot.
        import plugins.admin_panel
        import plugins.settings
        import plugins.start_and_cb
        import plugins.thumb_and_cap
        print("Digital Botz Plugins Loaded")\n        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")

        for id in Config.ADMIN:
            if Config.STRING_SESSION:
                try:
                    await self.send_message(id, f"𝟮𝗚𝗕+ ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\nNote: 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐬𝐭𝐫𝐢𝐧𝐠 𝐬𝐞𝐬𝐬𝐢𝐨𝐧 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐓𝐡𝐞𝐧 𝐬ᴜᴘᴘᴏʀᴛs 𝟐𝐆𝐁+ 𝐟ɪʟᴇs.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
                except:
                    pass
            else:
                try:
                    await self.send_message(id, f"𝟮𝗚𝗕- ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
                except:
                    pass

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`")
            except:
                print("Pʟᴇᴀsᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")

    async def stop(self, *args):
        for id in Config.ADMIN:
            try:
                await self.send_message(id, f"**Bot Stopped....**")
            except:
                pass
        print("Bot Stopped 🙄")
        await super().stop()


digital_instance = DigitalAutoRenameBot()

def main():
    async def start_services():
        if Config.STRING_SESSION:
            await asyncio.gather(app.start(), digital_instance.start())
        else:
            await asyncio.gather(digital_instance.start())

        await idle()

        if Config.STRING_SESSION:
            await asyncio.gather(app.stop(), digital_instance.stop())
        else:
            await digital_instance.stop()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user!")
    finally:
        loop.close()

if __name__ == "__main__":
    warnings.filterwarnings("ignore", message="There is no current event loop")
    try:
        main()
    except errors.FloodWait as ft:
        print(f"⏳ FloodWait: Sleeping for {ft.value} seconds")
        asyncio.run(asyncio.sleep(ft.value))
        print("Now Ready For Deploying!")
        main()

# Rkn Developer
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Update Channel @Digital_Botz & @DigitalBotz_Support
