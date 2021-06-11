#! python3

import re
import zipfile
from pathlib import Path
from firmware_collector.manifest import Manifest


class Storage:
    def __init__(self, storage_path):
        self.storage_path = Path(storage_path)
        if not self.storage_path.exists():
            raise FileNotFoundError

    def save(self, artifact_file):
        filename = Path(artifact_file).name
        filename_parsed = re.match(r'(\d{4}.\d.\d).(\d)(-[a-z]+\d)?_(.*)+_(\w+).zip', filename)

        release_name = "{}.{}".format(filename_parsed.group(1), filename_parsed.group(2))
        release_dir = self.storage_path / (release_name)

        if not release_dir.exists():
            release_dir.mkdir()

        with zipfile.ZipFile(artifact_file, 'r') as zip_ref:
            for file in zip_ref.infolist():
                if file.filename.endswith("stable.manifest"):
                    file.filename = Path(file.filename).name

                    manifest_path = release_dir / "sysupgrade" / "stable.manifest"
                    if manifest_path.exists():
                        zip_ref.extract(file, "/tmp")
                        manifest = Manifest()
                        manifest.load(manifest_path)
                        manifest_part = Manifest()
                        manifest_part.load(Path("/tmp") / "stable.manifest")
                        manifest.merge(manifest_part)
                        manifest.export(manifest_path)
                    else:
                        zip_ref.extract(file, manifest_path.parent)

                if file.filename.startswith('images/factory/'):
                    file.filename = Path(file.filename).name
                    if file.filename != "factory":
                        zip_ref.extract(file, release_dir / "factory")
                elif file.filename.startswith('images/sysupgrade/'):
                    file.filename = Path(file.filename).name
                    if file.filename != "sysupgrade":
                        zip_ref.extract(file, release_dir / "sysupgrade")
                elif file.filename.startswith('images/other/'):
                    file.filename = Path(file.filename).name
                    if file.filename != "other":
                        zip_ref.extract(file, release_dir / "other")

    def delete(self, artifact_file):
        return True
