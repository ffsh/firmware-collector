#! python3

import os
import re
import zipfile
import shutil


class Storage:
    def __init__(self, storage_path):
        if os.path.isdir(storage_path):
            self.storage_path = storage_path
        else:
            raise FileNotFoundError

    def save(self, artifact_file):

        if not os.path.isfile(artifact_file):
            print("file " + artifact_file)
            return None

        print("basename: " + os.path.basename(artifact_file))
        match_the_catch = re.match(r'(\d{4}.\d.\d).(\d)_(.*)+_(\w+).zip', os.path.basename(artifact_file))
        print(match_the_catch.group(0))
        release_name = "{}.{}".format(match_the_catch.group(1), match_the_catch.group(2))
        release_dir = "{}/{}".format(self.storage_path, release_name)

        if not os.path.isdir(release_dir):
            os.mkdir(release_dir)

        with zipfile.ZipFile(artifact_file, 'r') as zip_ref:
            zip_ref.extractall(release_dir)

        print("{}/images/factory --->".format(release_dir), "{}/factory".format(release_dir))
        shutil.copytree("{}/images/factory".format(release_dir), "{}/factory".format(release_dir), dirs_exist_ok=True)
        shutil.copytree("{}/images/sysupgrade".format(release_dir), "{}/sysupgrade".format(release_dir), dirs_exist_ok=True)

        #shutil.rmtree("{}/packages".format(release_dir))
        #shutil.rmtree("{}/images".format(release_dir))

        print("Gluon Version:" + match_the_catch.group(1))
        print("FFSH Version:" + match_the_catch.group(2))

    def delete(self, artifact_file):
        return True

