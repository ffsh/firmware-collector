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
        self.artifacts = [item for sublist in self.artifacts for item in sublist]

    def __load_artifacts_helper(self, link, result=[]):
        if link == "":
            # end of recursion reached last page
            self.artifacts = result
        else:
            next_link = ""  # Reset
            # first page or new pages in available
            r = requests.get(link, auth=HTTPBasicAuth(self.username, self.token))
            if r.status_code == 200:
                result.append([Artifact(a) for a in r.json()["artifacts"]])
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
        #print(self.artifacts)
        for artifact in self.artifacts:
            if artifact.id == id:
                return artifact
        #return next(artifact for artifact in self.artifacts if artifact["id"] == id)

    def download_artifact(self, id):
        url = self.get_artifact(id).archive_download_url
        local_filename = "{}.zip"

        with requests.get(url, auth=HTTPBasicAuth(self.username, self.token), stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
