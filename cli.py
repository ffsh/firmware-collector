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
from firmware_collector.downloader import Downloader


class Collector():
    def __init__(self, config_file):
        super().__init__()
        try:
            with open(config_file, "r") as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            print("Your config.json is missing, check config.json.example")

    def update(self):
        """
        updates the entries in the DB
        """
        api = API(self.config["url"], self.config["username"], self.config["secret"])
        repository = Repository(self.config["db_path"])
        api.load_artifacts()

        artifact_list = api.get_artifact_ids()
        bar = Bar('Processing', max=len(artifact_list))

        for artifact_id in artifact_list:
            repository.create(api.get_artifact(artifact_id))
            bar.next()
        bar.finish()

    def download(self, version):
        downloader = Downloader(self.config)
        downloader.download(version)

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
    parse_group.add_argument('--download', action="store", default=False)
    parse_group.add_argument('--store', action="store_true", default=False)
    parse_group.add_argument('--manifest', action="store", default=False)
    parser.add_argument("--branch", action="store", required=False)
    args = parser.parse_args()

    try:
        collector = Collector("config.json")
        if args.update:
            collector.update()
        elif args.download:
            if args.download == "":
                print("Please provide a version.")
            else:
                collector.download(args.download)
        elif args.store:
            collector.store()
        elif args.manifest:
            collector.manifest(args.manifest, args.branch)
    except ModuleNotFoundError as module_error:
        print("Did you forget to activate the virtual-env?")
        print("Error: {}".format(module_error))
        print("Maybe run: . venv/bin/activate")