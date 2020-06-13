#! python3
from api import API
from repository import Repository

db_path = "/home/grotax/git/firmware-collector/db.json"

with open("secrets", "r") as f:
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

result = t_repository.read(465456786)

#for shitid in db_ids:
#    if shitid in db_ids:
#        print("Saved artifact to DB: {}".format(shitid))
