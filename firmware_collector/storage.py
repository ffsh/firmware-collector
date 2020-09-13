#! python3

import os
import re
import zipfile
from firmware_collector.manifest import Manifest

class Storage:
    def __init__(self, storage_path):
        if os.path.isdir(storage_path):
            self.storage_path = storage_path
        else:
            raise FileNotFoundError

    def save(self, artifact_file):

        #if not os.path.isfile(artifact_file):
            #return None

        filename = os.path.basename(artifact_file)
        filename_parsed = re.match(r'(\d{4}.\d.\d).(\d)_(.*)+_(\w+).zip', filename)
        print(filename_parsed.group(0))
        release_name = "{}.{}".format(filename_parsed.group(1), filename_parsed.group(2))
        release_dir = "{}/{}".format(self.storage_path, release_name)

        if not os.path.isdir(release_dir):
            os.mkdir(release_dir)

        with zipfile.ZipFile(artifact_file, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith("master.manifest"):
                    zip_ref.extract(file, "{}/temp".format(release_dir))
                    if os.path.isfile("{}/sysupgrade/master.manifest".format(release_dir)):
                        manifest = Manifest()
                        manifest.load("{}/sysupgrade/master.manifest".format(release_dir))
                        manifest_part = Manifest()
                        manifest_part.load("{}/temp/master.manifest".format(release_dir))
                        manifest.merge(manifest_part)
                        manifest.export("{}/sysupgrade/master.manifest".format(release_dir))

                if file.startswith('images/factory/'):
                    zip_ref.extract(file, "{}/factory".format(release_dir))
                elif file.startswith('images/sysupgrade/'):
                    zip_ref.extract(file, "{}/sysupgrade".format(release_dir))
                elif file.startswith('images/other/'):
                    zip_ref.extract(file, "{}/other".format(release_dir))

    def delete(self, artifact_file):
        return True

