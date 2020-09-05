import requests
from requests.auth import HTTPBasicAuth


class Artifact:
    """Reflects a GitHub Artifact

    id:                   id of the Artifact
    node_id:              node_id
    name :                name of the artifact
    size_in_bytes:        size in bytes
    url:                  url to the artifact
    archive_download_url: download url
    expired:              if true its no longer available
    created_at:           created date Y-M-DTh:m:sZ
    updated_at:           updated date Y-M-DTh:m:sZ
    stored:               True if artifact was downloaded
    """
    def __init__(self, artifact):
        self.id = artifact["id"]
        self.node_id = artifact["node_id"]
        self.name = artifact["name"]
        self.size_in_bytes = artifact["size_in_bytes"]
        self.url = artifact["url"]
        self.archive_download_url = artifact["archive_download_url"]
        self.expired = artifact["expired"]
        self.created_at = artifact["created_at"]
        self.updated_at = artifact["updated_at"]
        self.stored = artifact["stored"]
