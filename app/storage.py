import os
from urllib.parse import quote
from urllib.request import Request, urlopen

from flask import current_app
from werkzeug.utils import secure_filename


def upload_photo(uploaded_file, filename_stem, folder="listings"):
    """Lädt ein JPEG nach ``<folder>/`` im Storage-Bucket und gibt die öffentliche URL zurück.

    Gibt None zurück, wenn Storage nicht konfiguriert ist oder der Upload fehlschlägt
    (Aufrufer nutzt dann den lokalen Fallback).
    """
    supabase_url = current_app.config.get("SUPABASE_URL")
    storage_key = current_app.config.get("SUPABASE_STORAGE_KEY")
    bucket = current_app.config.get("SUPABASE_STORAGE_BUCKET", "images")
    if not supabase_url or not storage_key or not bucket:
        return None

    original_name = secure_filename(uploaded_file.filename)
    _, extension = os.path.splitext(original_name)
    object_path = f"{folder}/{filename_stem}{extension.lower()}"
    encoded_path = "/".join(quote(part, safe="") for part in object_path.split("/"))
    endpoint = f"{supabase_url}/storage/v1/object/{quote(bucket, safe='')}/{encoded_path}"

    uploaded_file.stream.seek(0)
    data = uploaded_file.stream.read()
    uploaded_file.stream.seek(0)

    request = Request(
        endpoint,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {storage_key}",
            "apikey": storage_key,
            "Content-Type": uploaded_file.mimetype or "image/jpeg",
            "x-upsert": "true",
        },
    )
    try:
        with urlopen(request, timeout=15):
            pass
    except Exception as exc:  # noqa: BLE001 - local fallback should keep the app usable.
        current_app.logger.warning("Supabase Storage upload failed: %s", exc)
        return None

    return f"{supabase_url}/storage/v1/object/public/{quote(bucket, safe='')}/{encoded_path}"


def upload_listing_photo(uploaded_file, filename_stem):
    """Backwards-compatible wrapper: listing photos go into the ``listings/`` folder."""
    return upload_photo(uploaded_file, filename_stem, folder="listings")
