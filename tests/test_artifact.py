#! python3
import unittest
from firmware_collector.artifact import Artifact


class TestArtifact(unittest.TestCase):

    def test_create(self):
        a_artifact = {
            "id": 8445239,
            "node_id": "MDg6QXJ0aWZhY3Q3Mzk1ODAz",
            "name": "x86-legacy_logs",
            "size_in_bytes": 3203524,
            "url": "https://api.github.com/repos/ffsh/site/actions/artifacts/8445239",
            "archive_download_url": "https://api.github.com/repos/ffsh/site/actions/artifacts/8445239/zip",
            "expired": "false",
            "created_at": "2020-05-29T20:10:24Z",
            "updated_at": "2020-05-29T20:10:36Z"
         }
        a_artifact["stored"] = False

        b_artifact = Artifact(a_artifact)
        self.assertEqual(a_artifact["id"], b_artifact.id)
        self.assertEqual(a_artifact["node_id"], b_artifact.node_id)
        self.assertEqual(a_artifact["name"], b_artifact.name)
        self.assertEqual(a_artifact["size_in_bytes"], b_artifact.size_in_bytes)
        self.assertEqual(a_artifact["url"], b_artifact.url)
        self.assertEqual(a_artifact["archive_download_url"], b_artifact.archive_download_url)
        self.assertEqual(a_artifact["expired"], b_artifact.expired)
        self.assertEqual(a_artifact["created_at"], b_artifact.created_at)
        self.assertEqual(a_artifact["updated_at"], b_artifact.updated_at)
        self.assertEqual(a_artifact["stored"], b_artifact.stored)


if __name__ == '__main__':
    unittest.main()
