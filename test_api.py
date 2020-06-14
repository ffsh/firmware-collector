#! python3
# from artifact import Artifact
from api import API

with open("secrets", "r") as f:
    secret = f.readline()

t_api = API("https://api.github.com/repos/ffsh/site/actions/artifacts", "Grotax", secret)
#https://api.github.com/repositories/122235734/actions/artifacts?page=2
#https://api.github.com/repos/ffsh/site/actions/artifacts
t_api.load_artifacts()
print(t_api.get_artifacts())
print(t_api.get_artifact(8445234).name)


