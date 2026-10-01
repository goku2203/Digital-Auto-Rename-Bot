# Runtime fixes for autorename filename parsing and source-message cleanup.
# Loaded after the normal plugins so the existing rename flow is preserved.

import re
from pyrogram import Client, filters
from plugins import file_rename
from plugins.auto_rename import EnhancedAutoRenamer


_original_clean = EnhancedAutoRenamer._clean_source_filename
_original_apply = EnhancedAutoRenamer.apply_format_template
_original_upload_doc = file_rename.upload_doc


@classmethod
def _clean_source_filename_fixed(cls, filename: str) -> tuple:
    base, extension = cls._split_ext(filename)

    # Remove bracketed/domain prefix only from the beginning.
    # Example: [HindiAnimeZone.me] Title -> Title
    base = re.sub(r"^\s*\[[^\]]*\]\s*", "", base, count=1)
    base = re.sub(
        r"^\s*(?:https?://)?(?:www\.)?[A-Za-z0-9][A-Za-z0-9-]*(?:\.[A-Za-z0-9-]+)*\.(?:com|net|org|in|cc|site|bz|me|tv|xyz|co|info|club|pro|to|ws|ink|cool|vip|wiki|art)\b[\s_.|:-]*",
        "",
        base,
        count=1,
        flags=re.IGNORECASE,
    )

    base = base.replace("_", " ").replace(".", " ")
    for word in ["Tamil TV Toons", "HindiAnimeZone", "ToonWorld4All"]:
        base = re.sub(rf"(?i)\b{re.escape(word)}\b", "", base)
    base = re.sub(r"\[.*?\]|\(.*?\)", "", base)
    base = re.sub(r"@[A-Za-z0-9_]+", "", base)
    base = re.sub(r"\s+", " ", base).strip(" -|:")
    return base, extension


EnhancedAutoRenamer._clean_source_filename = _clean_source_filename_fixed


def apply_format_template_fixed(self, info, template):
    # Replace placeholders first. Missing values become empty strings.
    values = {
        "{title}": info.get("title", ""),
        "{year}": info.get("year", ""),
        "{season}": info.get("season", ""),
        "{episode}": info.get("episode", ""),
        "{quality}": info.get("quality", ""),
        "{source}": info.get("source", ""),
        "{video_codec}": info.get("video_codec", ""),
        "{audio_codec}": info.get("audio_codec", ""),
        "{language}": info.get("language", ""),
        "{bit_depth}": info.get("bit_depth", ""),
        "{hdr}": info.get("hdr", ""),
        "{original}": info.get("original_name", ""),
        "{filename}": info.get("original_name", ""),
        "{ext}": info.get("extension", ""),
    }
    for key, value in values.items():
        template = template.replace(key, value)

    # Clean missing season/episode/quality without changing literal text such as
    # "Multi audio" in the user's template.
    template = re.sub(r"\s+", " ", template).strip()
    template = re.sub(r"\s+\.", ".", template)
    template = re.sub(r"\.{2,}", ".", template)
    return self._normalize_output_name(template)


EnhancedAutoRenamer.apply_format_template = apply_format_template_fixed


async def upload_doc_fixed(bot, update, requested_name=None):
    result = await _original_upload_doc(bot, update, requested_name=requested_name)

    # Delete the original incoming file only after the renamed upload succeeds.
    try:
        if getattr(result, "text", "") == "Uploaded Successfully....":
            original = getattr(update.message, "reply_to_message", None)
            if original:
                await bot.delete_messages(update.message.chat.id, original.id)
    except Exception as e:
        print(f"[AUTORENAME] Original message cleanup failed: {e}")

    return result


file_rename.upload_doc = upload_doc_fixed
