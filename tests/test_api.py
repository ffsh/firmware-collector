#! python3
import unittest
from firmware_collector import api


class TestArtifact(unittest.TestCase):

    def __init__(self):
        super().__init__()

    def test_load_artifacts(self):
        # api.load_artifacts()
        pass


if __name__ == '__main__':
    unittest.main()
