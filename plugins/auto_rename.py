# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
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

import re
import os
from pathlib import Path
from typing import Dict, Optional, Tuple
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import asyncio
from helper.database import digital_botz
import re
from pathlib import Path
from typing import Dict

class EnhancedAutoRenamer:
    def __init__(self):
        self.renaming_operations = {} 
        
    def extract_all_info(self, filename: str) -> Dict:
        """Extract all possible information from filename"""
        info = {
            'title': '',
            'year': '',
            'season': '',
            'episode': '',
            'quality': '',
            'source': '',
            'video_codec': '',
            'audio_codec': '',
            'language': '',
            'bit_depth': '',
            'hdr': '',
            'release_group': '',
            'original_name': Path(filename).stem,
            'extension': Path(filename).suffix.lstrip('.')
        }
        
        # 1. Remove ONLY leading release/source boxes like [HindiAnimeZone.com]
        #    Do not remove normal (...) content from anywhere else.
        clean_name = re.sub(r'^\s*(?:\[[^\]]*\]|\([^\)]*\))\s*', '', filename)

        # 2. Remove leading website/source prefix if it appears before the real title.
        #    Examples:
        #      [HindiAnimeZone.com] Liar Game ...
        #      HindiAnimeZone.com - Liar Game ...
        clean_name = re.sub(
            r'^\s*(?:[a-zA-Z0-9-]+\.)?(?:com|net|org|in|cc|site|bz)\S*\s*(?:[-|:]+\s*)?',
            '',
            clean_name,
            flags=re.IGNORECASE
        )

        # 3. Remove @username tags automatically from the source filename.
        #    This keeps your metadata title @anime_love9, but removes usernames
        #    from the actual output filename.
        clean_name = re.sub(r'@[a-zA-Z0-9_]+', '', clean_name)

        # 4. Replace dots/underscores with spaces and normalize whitespace.
        clean_name = clean_name.replace('.', ' ').replace('_', ' ')
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()

        # 5. Title is everything before year/quality/season.
        title_match = re.search(r'^(.+?)(?=\s*(?:19|20)\d{2}|\s*\d{3,4}p|\s*S\d{1,2}|\s*Season)', clean_name, re.IGNORECASE)
        
        if title_match:
            info['title'] = title_match.group(1).strip()
        else:
            info['title'] = clean_name.strip()
        
        # Year extraction
        year_match = re.search(r'[\(\[]?(\d{4})[\)\]]?', clean_name)
        if year_match:
            info['year'] = year_match.group(1)
        
        # Season and Episode extraction (multiple patterns)
        # Pattern 1: S01E01 or S01EP01
        s_e_match = re.search(r'[Ss](\d{1,2})[EePp]?(\d{1,3})', clean_name)
        if s_e_match:
            info['season'] = f"S{s_e_match.group(1).zfill(2)}"
            info['episode'] = f"E{s_e_match.group(2).zfill(2)}"
        
        # Pattern 2: Season 1 Episode 1
        if not info['season']:
            season_match = re.search(r'[Ss]eason\s*(\d{1,2})', clean_name, re.IGNORECASE)
            episode_match = re.search(r'[Ee]pisode\s*(\d{1,3})', clean_name, re.IGNORECASE)
            if season_match:
                info['season'] = f"S{season_match.group(1).zfill(2)}"
            if episode_match:
                info['episode'] = f"E{episode_match.group(1).zfill(2)}"
        
        # Quality extraction
        quality_match = re.search(r'(\d{3,4}p|4[Kk]|UHD|HD|SD|HDRip|WEBRip|BluRay)', clean_name, re.IGNORECASE)
        if quality_match:
            info['quality'] = quality_match.group(1).upper()
        
        # Video codec
        codec_match = re.search(r'(x264|x265|HEVC|H\.264|H\.265|AVC)', clean_name, re.IGNORECASE)
        if codec_match:
            info['video_codec'] = codec_match.group(1).lower()
        
        # Audio codec
        audio_match = re.search(r'(DD\+?5\.1|DDP?5\.1|DD5\.1|DD2\.0|AAC|AC3|DTS)', clean_name, re.IGNORECASE)
        if audio_match:
            info['audio_codec'] = audio_match.group(1).upper()
        
        # Language detection
        languages = ['Hindi', 'English', 'Malayalam', 'Tamil', 'Telugu', 'Kannada', 'Dual']
        for lang in languages:
            if re.search(lang, clean_name, re.IGNORECASE):
                info['language'] = lang
                break
        
        # Source type
        sources = ['BluRay', 'WEBRip', 'WEB-DL', 'HDRip', 'DVDRip', 'TVRip', 'AMZN', 'Netflix', 'Hotstar']
        for source in sources:
            if re.search(source, clean_name, re.IGNORECASE):
                info['source'] = source
                break
        
        # Bit depth and HDR
        if '10bit' in clean_name.lower():
            info['bit_depth'] = '10bit'
        if 'hdr' in clean_name.lower():
            info['hdr'] = 'HDR'
        
        return info
    
    def _clean_title(self, title: str) -> str:
        """Clean and format title"""
        # Remove common release group tags
        title = re.sub(r'[@#~\[\]\{\}\(\)]', '', title)
        # Replace multiple spaces
        title = re.sub(r'\s+', ' ', title)
        # Capitalize first letter of each word
        return title.strip().title()
    
    def apply_format_template(self, info: Dict, template: str) -> str:
        """Apply user's format template to extracted info"""
        # Available placeholders mapping
        placeholders = {
            '{title}': info.get('title', ''),
            '{year}': info.get('year', ''),
            '{season}': info.get('season', ''),
            '{episode}': info.get('episode', ''),
            '{quality}': info.get('quality', ''),
            '{source}': info.get('source', ''),
            '{video_codec}': info.get('video_codec', ''),
            '{audio_codec}': info.get('audio_codec', ''),
            '{language}': info.get('language', ''),
            '{bit_depth}': info.get('bit_depth', ''),
            '{hdr}': info.get('hdr', ''),
            '{original}': info.get('original_name', ''),
            '{filename}': info.get('original_name', ''),
            '{ext}': info.get('extension', '')
        }
        
        # Replace all placeholders
        for placeholder, value in placeholders.items():
            template = template.replace(placeholder, value)
        
        # Clean up any empty parentheses or brackets
        template = re.sub(r'\(\s*\)', '', template)  # Remove empty parentheses
        template = re.sub(r'\[\s*\]', '', template)  # Remove empty brackets
        template = re.sub(r'\s+', ' ', template)  # Remove extra spaces
        template = template.strip()
        
        return template

@Client.on_message(filters.command(["autorename", "setformat"]))
async def set_format_command(client: Client, message: Message):
    """Set auto rename format template"""
    user_id = message.from_user.id
    
    if len(message.command) < 2:
        # Show current format if set
        current_format = await digital_botz.get_format_template(user_id)
        if current_format:
            reply_text = f"📝 **Your Current Format:**\n`{current_format}`\n\n"
        else:
            reply_text = "❌ No format set yet!\n\n"
        
        reply_text += "**Available Placeholders:**\n"
        placeholders = [
            "`{filename}` - Original File Name. ", 
            "`{title}` - Movie/Series title",
            "`{year}` - Release year",
            "`{season}` - Season number (S01)",
            "`{episode}` - Episode number (E01)",
            "`{quality}` - Video quality (1080p, 4K)",
            "`{source}` - Source type (BluRay, WEBRip)",
            "`{video_codec}` - Video codec (x264, x265)",
            "`{audio_codec}` - Audio codec (DD+5.1)",
            "`{language}` - Language (Hindi, English)",
            "`{bit_depth}` - Bit depth (10bit)",
            "`{hdr}` - HDR info",
            "`{ext}` - File extension"
        ]
        
        reply_text += "\n".join(placeholders)
        reply_text += "\n\n**Example Formats:**\n"
        reply_text += "• `{title} ({year}) {quality} {language}.{ext}`\n"
        reply_text += "• `{title} {season}{episode} {quality}.{ext}`\n"
        reply_text += "• `{title} {quality} {source} {video_codec}.{ext}`\n\n"
        reply_text += "**Usage:** `/autorename {title} ({year}) {quality} {language}.{ext}`"
        
        buttons = [
            [
                InlineKeyboardButton("🎬 Movie Format", callback_data="format_movie"),
                InlineKeyboardButton("📺 Series Format", callback_data="format_series")
            ],
            [
                InlineKeyboardButton("🎵 Music Format", callback_data="format_music"),
                InlineKeyboardButton("📄 Document Format", callback_data="format_doc")
            ],
            [
                InlineKeyboardButton("✍️ Custom Format", callback_data="format_custom")
            ]
        ]
        
        await message.reply_text(
            reply_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return
    
    # Set new format
    format_template = " ".join(message.command[1:])
    await digital_botz.add_user_format_template(user_id, format_template)
    await message.reply_text(f"✅ Format set successfully!\n\n`{format_template}`")

@Client.on_callback_query(filters.regex(r"^format_"))
async def format_callback(client, callback_query):
    """Handle format selection callback"""
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    formats = {
        "format_movie": "{title} ({year}) {quality} {source} {video_codec} {language}.{ext}",
        "format_series": "{title} {season}{episode} {quality} {source} {video_codec}.{ext}",
        "format_music": "{title} - {language} ({year}).{ext}",
        "format_doc": "{title} ({quality}).{ext}",
        "format_custom": "{title} {quality} {language}.{ext}"
    }
    
    if data in formats:
        await digital_botz.add_user_format_template(user_id, formats[data])
        await callback_query.message.edit_text(
            f"✅ Format set to **{data.split('_')[1].title()}**!\n\n`{formats[data]}`"
        )
    await callback_query.answer()


# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
