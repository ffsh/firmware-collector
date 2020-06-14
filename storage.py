#! python3

import os
import re


class Storage:
    def __init__(self, storage_path):
        if os.path.isdir(storage_path):
            self.storage_path = storage_path
        else:
            raise FileNotFoundError

    def save(self, artifact_file):
        print(re.match(r'(\d{4}.\d.\d).(\d)_(\w)+_(\w+)', os.path.basename(artifact_file)))

    def delete(self, artifact_file):
        return True

    def ls(self):
        return [directory.name for directory in os.scandir(self.storage_path)]
