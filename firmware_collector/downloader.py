from firmware_collector.api import API
from firmware_collector.repository import Repository
import multiprocessing as mp


class Downloader:
    """
    Manages the dowloads with mp
    """

    def __init__(self, config):
        super().__init__()
        self.config = config

    def __match(self, artifact, version):
        """
        checks if this file should be downloaded
        """
        if not artifact.stored and artifact.name.endswith("output") and version in artifact.name:
            return True

    def dowload_helper(self, api, artifact):
        try:
            api.download_artifact(artifact, self.config["download_path"])
        except Exception as exception:
            print("Download failed {}".format(exception))

    def download(self, version):
        """
        downloads all the artifacts, that are not yet downloaded"
        """
        api = API(self.config["url"], self.config["username"], self.config["secret"])
        repository = Repository(self.config["db_path"])
        pool = mp.Pool(mp.cpu_count())

        download_list = []

        for a_id in repository.read_all_id():
            artifact = repository.read(a_id)
            if self.__match(artifact, version):
                download_list.append(artifact)
        print("Starting download of {} files".format(len(download_list)))

        for artifact in download_list:
            pool.apply_async(self.dowload_helper, args=(api, artifact))
            artifact.stored = True

        pool.close()
        pool.join()

        for artifact in download_list:
            if artifact.stored:
                repository.update(artifact.id, artifact)
