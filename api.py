#! python3
import requests
from requests.auth import HTTPBasicAuth


class API:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.artifacts = []

    def load_artifacts(self):
        self.__load_artifacts_helper(self.url)

    def __load_artifacts_helper(self, link, result=[]):
        if link.endswith("1"):
            # end of recursion reached last page
            self.artifacts = result
        else:
            # first page or new pages in available
            r = requests.get(self.url)
            if r.status_code == 200:
                result.append([artifact for artifact in r.json()])
                link = r.headers["link"].split(";")[0].replace("<","").replace(">", "")
                self.__load_artifacts_helper(link, result)
            else:
                # can't load more artifacts api denied
                print("API returned {}".format(r.status_code))
                return result


    def get_artifacts(self):
        return [artifact["id"] for artifact in self.artifacts]

    def get_artifact(self, id):
        return next(artifact for artifact in self.artifacts if artifact["id"] == id)

    def download_artifact(self, id):
        url = self.get_artifact(id)["archive_download_url"]
        local_filename = "{}.zip"

        with requests.get(url, auth=HTTPBasicAuth(self.username, self.password), stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename


def main():
    secret = None
    with open("secrets", "r") as f:
        secret = f.readline()
    a = Artiact("https://api.github.com/repos/ffsh/site/actions/artifacts", "Grotax", secret)

    a.load_artifacts()

    # print(len(a.get_artifacts()))
    # for artifact_id in a.get_artifacts():
    #     if artifact_id == 739580300:
    #         print("true")
    #         print(a.download_artifact(artifact_id))
    #     else:
    #         print(artifact_id)

if __name__ == "__main__":
    main()