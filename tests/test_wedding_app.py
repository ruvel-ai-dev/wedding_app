import importlib.util
from pathlib import Path
import io
import zipfile
import types
import sys


spec_storage = importlib.util.spec_from_file_location(
    "storage", Path(__file__).resolve().parents[1] / "wedding_app" / "storage.py"
)
storage = importlib.util.module_from_spec(spec_storage)
spec_storage.loader.exec_module(storage)

flask = types.ModuleType("flask")
flask.Flask = lambda *a, **kw: types.SimpleNamespace(route=lambda *a, **kw: (lambda f: f), static_folder="static")
flask.render_template = lambda *a, **kw: ""
flask.request = types.SimpleNamespace(form={}, files={})
flask.redirect = lambda x: x
flask.url_for = lambda *a, **kw: f"/u/{kw.get('subevent','')}"
flask.send_file = lambda *a, **kw: None
orig_flask = sys.modules.get("flask")
sys.modules["flask"] = flask

root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
app_mod = importlib.import_module("wedding_app.app")
if orig_flask is not None:
    sys.modules["flask"] = orig_flask
else:
    del sys.modules["flask"]


def test_event_path():
    assert app_mod.event_path("abc") == "events/abc/"


class DummyBlob:
    def __init__(self, name):
        self.name = name
    def download_blob(self):
        class B:
            def readall(self_inner):
                return b"data-" + self.name.encode()
        return B()


class DummyContainer:
    def __init__(self):
        self.uploaded = []
    def get_blob_client(self, container=None, blob=None):
        if blob:
            return DummyBlob(blob)
        return DummyBlob(container)
    def list_blobs(self, name_starts_with=None):
        for n in ["a.txt", "b.txt"]:
            yield DummyBlob(name_starts_with + n)


class DummyService:
    def __init__(self):
        self.container = DummyContainer()
    @classmethod
    def from_connection_string(cls, *a, **k):
        return cls()
    def get_blob_client(self, container=None, blob=None):
        return self.container.get_blob_client(container, blob)
    def get_container_client(self, *a, **k):
        return self.container


def test_download_zip(monkeypatch):
    monkeypatch.setattr(storage, "BlobServiceClient", DummyService)
    monkeypatch.setenv("AZURE_STORAGE_CONNECTION_STRING", "conn")
    buf = storage.download_files_as_zip("c", ["path/a.txt", "path/b.txt"])
    z = zipfile.ZipFile(buf)
    assert set(z.namelist()) == {"path/a.txt", "path/b.txt"}

