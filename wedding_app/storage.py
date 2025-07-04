"""Azure Blob Storage helper functions for the wedding app."""

from __future__ import annotations

import io
import os
import zipfile
from dataclasses import dataclass
from typing import Iterable, List

try:
    from azure.storage.blob import BlobServiceClient
except Exception:  # pragma: no cover - optional dependency may be missing
    class BlobServiceClient:  # type: ignore
        """Fallback dummy class used when azure dependency is unavailable."""
        pass


def get_blob_service() -> BlobServiceClient:
    """Return a BlobServiceClient using the AZURE_STORAGE_CONNECTION_STRING env."""
    conn_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING not set")
    return BlobServiceClient.from_connection_string(conn_str)


def upload_file(container: str, path: str, file_stream) -> None:
    """Upload a file stream to ``container`` at ``path``."""
    service = get_blob_service()
    blob_client = service.get_blob_client(container=container, blob=path)
    blob_client.upload_blob(file_stream, overwrite=True)


def list_files(container: str, path: str) -> List[str]:
    """List file names under ``path`` in the given container."""
    service = get_blob_service()
    container_client = service.get_container_client(container)
    return [b.name for b in container_client.list_blobs(name_starts_with=path)]


def download_files_as_zip(container: str, files: Iterable[str]) -> io.BytesIO:
    """Download multiple files from Azure into a ZIP archive and return bytes."""
    service = get_blob_service()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name in files:
            blob = service.get_blob_client(container=container, blob=name)
            data = blob.download_blob().readall()
            zf.writestr(os.path.basename(name), data)
    buf.seek(0)
    return buf


def ensure_path(container: str, path: str) -> None:
    """Ensure the given ``path`` exists by uploading an empty placeholder."""
    service = get_blob_service()
    blob_client = service.get_blob_client(container=container, blob=path.rstrip("/") + "/.init")
    if not blob_client.exists():
        blob_client.upload_blob(b"", overwrite=True)
