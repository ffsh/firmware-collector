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

    def download(self, username, token, path):
        url = self.archive_download_url
        local_filename = "{}/{}.zip".format(path, self.name)

        with requests.get(url, auth=HTTPBasicAuth(username, token), stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
