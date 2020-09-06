#! python3
from api import API
from repository import Repository

db_path = "/home/grotax/git/firmware-collector/db.json"

with open("secret", "r") as f:
    secret = f.readline()

t_api = API("https://api.github.com/repos/ffsh/site/actions/artifacts", "Grotax", secret)
t_repository = Repository(db_path)

t_api.load_artifacts()

current_ids = t_api.get_artifacts()

db_ids = t_repository.read_all_id()



for artifact_id in current_ids:
    print("want to insert: {}".format(artifact_id))
    #if artifact_id not in db_ids:
    t_repository.create(t_api.get_artifact(artifact_id))

db_ids = t_repository.read_all_id()
#print(db_ids)

#result = t_repository.read(465456786)

def dowload_all(db_ids):
    for a_id in db_ids:
        artifact = t_repository.read(a_id)
        if artifact.name.endswith("output"):
            print(t_repository.read(a_id).name)
        if not artifact.stored:
            t_api.download_artifact(artifact, "/home/grotax/git/firmware-collector/download_store")
            artifact.stored = True
            t_repository.update(artifact.id, artifact)

#dowload_all(db_ids)
