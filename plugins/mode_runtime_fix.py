# Runtime compatibility fix for the persistent rename mode flow.
from plugins import file_rename

try:
    from plugins import start_and_cb
except Exception:
    start_and_cb = None

_original_upload_doc = file_rename.upload_doc


async def upload_doc_fixed(bot, update, requested_name=None):
    upload_type = update.data.split("#", 1)[1]
    upload_type = {
        "doc": "document",
        "document": "document",
        "video": "video",
        "audio": "audio",
    }.get(upload_type, upload_type)

    # upload_doc reads this module-level value while processing the file.
    file_rename.upload_type = upload_type
    return await _original_upload_doc(bot, update, requested_name=requested_name)


file_rename.upload_doc = upload_doc_fixed
if start_and_cb is not None:
    start_and_cb.upload_doc = upload_doc_fixed
