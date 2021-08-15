#! python3
import argparse
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
    def __init__(self):
        super().__init__()
        try:
            self.config = {}
            self.config["url"] = os.environ['ffsh_url']
            self.config["username"] = os.environ['ffsh_username']
            self.config["secret"] = os.environ['ffsh_secret']
            self.config["db_path"] = "/tmp/ffsh/database_store"
            self.config["download_path"] = "/tmp/ffsh/download_store"
            self.config["firmware_path"] = "/tmp/ffsh/firmware_store"
        except KeyError as e:
            print("You are missing a environment variable {}".format(e))
        try:
            Path(self.config["download_path"]).mkdir(parents=True, exist_ok=True)
            Path(self.config["firmware_path"]).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print("Something went wrong with the path:\n{}".format(e))

    def update(self):
        """
        updates the entries in the DB
        """
        api = API(self.config["url"], self.config["username"], self.config["secret"])
        db_path = Path(self.config["db_path"]) / "repo.db"
        print(db_path)
        repository = Repository(db_path)
        api.load_artifacts()

        artifact_list = api.get_artifact_ids()
        bar = Bar('Processing', max=len(artifact_list))

        for artifact_id in artifact_list:
            repository.create(api.get_artifact(artifact_id))
            bar.next()
        bar.finish()

    def download(self, version):
        """
        download all files
        """
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

    def create_stores(self):
        Path(self.config["db_path"]).mkdir(parents=True, exist_ok=True)
        Path(self.config["download_path"]).mkdir(parents=True, exist_ok=True)
        Path(self.config["firmware_path"]).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is the firmware-collector automation interface')
    parse_group = parser.add_mutually_exclusive_group()
    parse_group.add_argument('--update', action="store_true", default=False)
    parse_group.add_argument('--download', action="store", default=False)
    parse_group.add_argument('--store', action="store_true", default=False)
    parse_group.add_argument('--manifest', action="store", default=False)
    parser.add_argument("--branch", action="store", required=False)
    args = parser.parse_args()

    try:
        collector = Collector()
        try:
            collector.create_stores()
        except Exception as e:
            print("Can't create directories {}".format(e))
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