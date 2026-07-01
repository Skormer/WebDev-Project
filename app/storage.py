import os
from urllib.parse import quote
from urllib.request import Request, urlopen

from flask import current_app
from werkzeug.utils import secure_filename


def upload_listing_photo(uploaded_file, filename):
    """Upload a listing JPEG to Supabase Storage and return its public URL.

    Returns None when storage is not configured or the upload fails, so callers can
    keep using the local filesystem fallback.
    """
    supabase_url = current_app.config.get("SUPABASE_URL")
    storage_key = current_app.config.get("SUPABASE_STORAGE_KEY")
    bucket = current_app.config.get("SUPABASE_STORAGE_BUCKET", "listing-photos")
    if not supabase_url or not storage_key or not bucket:
        return None

    original_name = secure_filename(uploaded_file.filename)
    _, extension = os.path.splitext(original_name)
    object_path = f"listings/{filename}{extension.lower()}"
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
