#! python3

import os
import re
import zipfile

class Storage:
    def __init__(self, storage_path):
        if os.path.isdir(storage_path):
            self.storage_path = storage_path
        else:
            raise FileNotFoundError

    def save(self, artifact_file):
        match_the_catch = re.match(r'(\d{4}.\d.\d).(\d)_(\w)+_(\w+)', os.path.basename(artifact_file))
        
        release_name = "{}.{}".format(match_the_catch[1], match_the_catch[2])
        release_dir = "{}/{}".format(self.storage_path, release_name)

        if not os.path.isdir(release_dir):
            os.mkdir(release_dir)
        
        with zipfile.ZipFile(artifact_file, 'r') as zip_ref:
            zip_ref.extractall(release_dir)


        print("Gluon Version:" + match_the_catch[1])
        print("FFSH Version:" + match_the_catch[2])

    def delete(self, artifact_file):
        return True

    def ls(self):
        return [directory.name for directory in os.scandir(self.storage_path)]
