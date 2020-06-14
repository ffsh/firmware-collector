#! python3
import requests
from requests.auth import HTTPBasicAuth
from artifact import Artifact


class API:
    def __init__(self, url, username, token):
        self.url = url
        self.username = username
        self.token = token
        self.artifacts = []

    def load_artifacts(self):
        self.__load_artifacts_helper(self.url)

    def __load_artifacts_helper(self, link, result=[]):
        if link == "":
            # end of recursion reached last page
            self.artifacts = result
        else:
            next_link = ""  # Reset
            # first page or new pages in available
            r = requests.get(link, auth=HTTPBasicAuth(self.username, self.token))
            if r.status_code == 200:
                for artifact in r.json()["artifacts"]:
                    artifact["stored"] = False
                    result.append(Artifact(artifact))
                links = requests.utils.parse_header_links(r.headers["link"].rstrip(">").replace(">,<", ",<"))
                for link in links:
                    if link["rel"] == "next":
                        next_link = link["url"]
                self.__load_artifacts_helper(next_link, result)
            else:
                # can't load more artifacts api denied
                print("API returned {}".format(r.status_code))
                self.artifacts = result

    def get_artifacts(self):
        return [artifact.id for artifact in self.artifacts]

    def get_artifact(self, id):
        for artifact in self.artifacts:
            if artifact.id == id:
                return artifact

    def download_artifact(self, artifact, download_dir):
        url = artifact.archive_download_url
        local_filename = "{}{}.zip".format(download_dir, artifact.name)

        with requests.get(url, auth=HTTPBasicAuth(self.username, self.token), stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=None):
                    if(chunk):
                        f.write(chunk)
        return local_filename
