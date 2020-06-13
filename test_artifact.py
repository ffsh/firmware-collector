#! python3
from artifact import Artifact


some_artifact = {
    "id": 8445239,
    "node_id": "MDg6QXJ0aWZhY3Q3Mzk1ODAz",
    "name": "x86-legacy_logs",
    "size_in_bytes": 3203524,
    "url": "https://api.github.com/repos/ffsh/site/actions/artifacts/8445239",
    "archive_download_url": "https://api.github.com/repos/ffsh/site/actions/artifacts/8445239/zip",
    "expired": "false",
    "created_at": "2020-05-29T20:10:24Z",
    "updated_at": "2020-05-29T20:10:36Z"
}

with open("secrets", "r") as f:
    secret = f.readline()

art = Artifact(some_artifact)
art.download("Grotax", secret, "/home/grotax/git/firmware-collector/downloads")
print(dir(art))