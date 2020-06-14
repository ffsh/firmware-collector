#! python3

from storage import Storage


try:
    t_storage = Storage("/some/apth")
except FileNotFoundError:
    print("Storage path not avaiable")


t_storage = Storage("/home/grotax/git/firmware-collector/artifact_store")

print("Found the follwoing dirs: {}".format(t_storage.ls()))

try:
    t_storage.save("/home/grotax/git/firmware-collector/downloads/2020.1.2.1_testTarget_output.zip")
except FileNotFoundError:
    print("Storage path not avaiable")


