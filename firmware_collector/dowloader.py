from firmware_collector.api import API
from firmware_collector.repository import Repository
from progress.bar import Bar
import multiprocessing as mp


class Downloader:

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.progress = None

    def __match(self, artifact, version):
        """
        checks if this file should be downloaded
        """
        if not artifact.stored and artifact.name.endswith("output") and version in artifact.name:
            return True

    def dowload_helper(self, api, artifact):
        try:
            api.download_artifact(artifact, self.config["download_path"])
            artifact.stored = True
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

        self.progress = Bar('Dowloading', max=len(download_list))
        for artifact in download_list:
            pool.apply_async(self.dowload_helper, args=(api, artifact), callback=self.progress.next())
        pool.close()
        pool.join()
        self.progress.finish()

        for artifact in download_list:
            if artifact.stored:
                repository.update(artifact.id, artifact)
