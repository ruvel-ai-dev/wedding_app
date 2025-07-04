"""Flask application for QR-based wedding media uploads."""

from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
import io

from flask import Flask, render_template, request, redirect, url_for, send_file

from . import storage


AZURE_CONTAINER = os.environ.get("AZURE_BLOB_CONTAINER", "wedding-media")

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, static_folder=str(BASE_DIR / "static"))


def event_path(event_id: str) -> str:
    return f"events/{event_id}/"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/event/create", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        name = request.form.get("name", "event")
        subevents_raw = request.form.get("subevents", "mehndi,nikkah,reception")
        subevents = [s.strip() for s in subevents_raw.split(",") if s.strip()]
        if not subevents:
            subevents = ["main"]
        event_id = uuid.uuid4().hex[:8]
        meta = {"name": name, "subevents": subevents}

        storage.ensure_path(AZURE_CONTAINER, event_path(event_id))
        storage.upload_file(
            AZURE_CONTAINER,
            f"events/{event_id}/event.json",
            io.BytesIO(json.dumps(meta).encode()),
        )

        # generate qr codes
        import qrcode

        qr_dir = BASE_DIR / "static" / "qr" / event_id
        qr_dir.mkdir(parents=True, exist_ok=True)
        for s in subevents:
            url = request.url_root.rstrip("/") + url_for("upload", event_id=event_id, subevent=s)
            img = qrcode.make(url)
            img.save(qr_dir / f"{s}.png")

        return redirect(url_for("admin", event_id=event_id))

    return render_template("create_event.html")


@app.route("/upload/<event_id>/<subevent>", methods=["GET", "POST"])
def upload(event_id: str, subevent: str):
    if request.method == "POST" and "file" in request.files:
        f = request.files["file"]
        storage.upload_file(
            AZURE_CONTAINER,
            f"events/{event_id}/{subevent}/{f.filename}",
            f.stream,
        )
        return redirect(request.url)
    return render_template("upload.html", event_id=event_id, subevent=subevent)


@app.route("/gallery/<event_id>/<subevent>")
def gallery(event_id: str, subevent: str):
    prefix = f"events/{event_id}/{subevent}/"
    files = storage.list_files(AZURE_CONTAINER, prefix)
    urls = [f"https://{AZURE_CONTAINER}.blob.core.windows.net/{name}" for name in files]
    return render_template("gallery.html", urls=urls, event_id=event_id, subevent=subevent)


@app.route("/admin/<event_id>")
def admin(event_id: str):
    qr_dir = BASE_DIR / "static" / "qr" / event_id
    images = [f"qr/{event_id}/" + p.name for p in qr_dir.glob("*.png")] if qr_dir.exists() else []
    return render_template("admin.html", event_id=event_id, qr_images=images)


@app.route("/download/<event_id>.zip")
def download_zip(event_id: str):
    prefix = f"events/{event_id}/"
    files = storage.list_files(AZURE_CONTAINER, prefix)
    buf = storage.download_files_as_zip(AZURE_CONTAINER, files)
    return send_file(buf, as_attachment=True, download_name=f"{event_id}.zip")


if __name__ == "__main__":
    app.run(debug=True)
