#! python3
# from artifact import Artifact
from api import API

with open("secret", "r") as f:
    secret = f.readline()

t_api = API("https://api.github.com/repos/ffsh/site/actions/artifacts", "Grotax", secret)
#https://api.github.com/repositories/122235734/actions/artifacts?page=2
#https://api.github.com/repos/ffsh/site/actions/artifacts
t_api.load_artifacts()
print(t_api.get_artifacts())
#print(t_api.get_artifact(8517669).name)
#t_api.download_artifact(t_api.get_artifact(8517669), "/home/grotax/git/firmware-collector/download_store/")

