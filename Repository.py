#! python3
from tinydb import TinyDB, Query
from artifact import Artifact


class Repository:
    def __init__(self, db_path):
        self.db = TinyDB(db_path)

    def create(self, artifact):
        self.db.insert({
            "id": artifact.id,
            "node_id": artifact.node_id,
            "name": artifact.name,
            "size_in_bytes": artifact.size_in_bytes,
            "url": artifact.url,
            "archive_download_url": artifact.archive_download_url,
            "expired": artifact.expired,
            "created_at": artifact.created_at,
            "updated_at": artifact.updated_at
        },)

    def update(self, id, artifact):
        entry = Query()
        self.db.update({
            "node_id": artifact.node_id,
            "name": artifact.name,
            "size_in_bytes": artifact.size_in_bytes,
            "url": artifact.url,
            "archive_download_url": artifact.archive_download_url,
            "expired": artifact.expired,
            "created_at": artifact.created_at,
            "updated_at": artifact.updated_at
            },
            entry.id == id
        )

    def read(self, id):
        entry = Query()
        result = self.db.search(entry.id == id)
        return Artifact(result)

    def read_all_id(self):
        return [id for artifact in self.db.all()]

    def delete(self, id):
        entry = Query()
        self.db.remove(entry.id == id)
