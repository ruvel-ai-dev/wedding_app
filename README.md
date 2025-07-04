# Wedding QR Upload App

This Flask application allows wedding guests to upload photos and videos via QR codes. Media is stored in Azure Blob Storage and can be viewed in a simple gallery.

## Setup

1. Install dependencies from `requirements.txt`.
2. Set `AZURE_STORAGE_CONNECTION_STRING` and optional `AZURE_BLOB_CONTAINER` environment variables.
3. Run with `python -m wedding_app.app`.

## Features

- Create events with multiple sub-events.
- Generate QR codes for each sub-event.
- Guests upload media without authentication.
- View galleries and download all media as a ZIP file.
