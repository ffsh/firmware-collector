#! python3
import argparse
import json
import os
import re
from pathlib import Path
from progress.bar import Bar
from firmware_collector.api import API
from firmware_collector.repository import Repository
from firmware_collector.storage import Storage
from firmware_collector.manifest import Manifest


class Collector():
    def __init__(self, config_file):
        super().__init__()
        with open(config_file, "r") as config_file:
            self.config = json.load(config_file)

    def update(self):
        """
        updates the entries in the DB
        """
        api = API(self.config["url"], self.config["username"], self.config["secret"])
        repository = Repository(self.config["db_path"])
        api.load_artifacts()
        for artifact_id in api.get_artifact_ids():
            repository.create(api.get_artifact(artifact_id))

    def download(self):
        """
        downloads all the artifacts, that are not yet downloaded"
        """
        api = API(self.config["url"], self.config["username"], self.config["secret"])
        repository = Repository(self.config["db_path"])

        download_list = []
        for a_id in repository.read_all_id():
            artifact = repository.read(a_id)
            if not artifact.stored and artifact.name.endswith("output"):
                download_list.append(artifact)

        bar = Bar('Processing', max=len(download_list))
        for artifact in download_list:
            bar.next()
            try:
                api.download_artifact(artifact, self.config["download_path"])
                artifact.stored = True
                repository.update(artifact.id, artifact)
            except Exception as exception:
                print("Download failed {}".format(exception))
        bar.finish()

    def store(self):
        """
        stores the images from the download dir in a proper way
        """
        # repository = Repository(self.config["db_path"])
        storage = Storage(self.config["firmware_path"])
        file_list = [file for file in os.scandir(self.config["download_path"])]

        bar = Bar('Processing', max=len(file_list))
        for artifact in file_list:
            bar.next()
            storage.save(artifact.path)
        bar.finish()

    def manifest(self, version, branch):
        version_pattern = re.compile(r'(\d{4}.\d.\d).(\d)')
        if version_pattern.match(version) and branch is not None:
            manifest = Manifest()
            manifest_path = Path(self.config["firmware_path"]) / version / "sysupgrade" / "stable.manifest"
            manifest.load(manifest_path)
            manifest.set_branch(branch)
            manifest.export(manifest_path.parent / "{}.{}".format(branch, "manifest"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is the firmware-collector cli')
    parse_group = parser.add_mutually_exclusive_group()
    parse_group.add_argument('--update', action="store_true", default=False)
    parse_group.add_argument('--download', action="store_true", default=False)
    parse_group.add_argument('--store', action="store_true", default=False)
    parse_group.add_argument('--manifest', action="store", default=False)
    parser.add_argument("--branch", action="store", required=False)
    args = parser.parse_args()

    collector = Collector("config.json")

    if args.update:
        collector.update()
    elif args.download:
        collector.download()
    elif args.store:
        collector.store()
    elif args.manifest:
        collector.manifest(args.manifest, args.branch)
