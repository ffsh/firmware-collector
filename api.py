#! python3
import requests
from requests.auth import HTTPBasicAuth 


api_url = "https://api.github.com/repos/ffsh/site/actions/artifacts"

class Artiacts:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.artifacts = []

    def load_artifacts(self):
        self.__load_artifacts_helper(self.url)

    def __load_artifacts_helper(self, link, result=[]):
        if link.endswith("1"):
            self.artifacts = result
        else:
            r = requests.get(self.url)
            result.append([artifact for artifact in r.json()])
            print(r.headers)
            # link = r.headers["link"].split(";")[0].replace("<","").replace(">", "")
            # self.__load_artifacts_helper(link, result)
        


    '<https://api.github.com/repositories/122235734/actions/artifacts?page=2>; rel="next", <https://api.github.com/repositories/122235734/actions/artifacts?page=2>; rel="last"'


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
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)
        return local_filename

def main():    
    a = Artiacts(api_url, "Grotax", "56463ad60ae645c4cd34dc4d16811ec96ecb4fc2")

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