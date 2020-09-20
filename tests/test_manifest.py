import unittest
from firmware_collector.manifest import Manifest
import os


class TestArtifact(unittest.TestCase):

    def test_create_empty(self):
        manifest = Manifest()
        self.assertEqual(manifest.branch, "")
        self.assertEqual(manifest.date, "")
        self.assertEqual(manifest.priority, "")
        self.assertEqual(manifest.body, "")
        self.assertEqual(manifest.signature, "")

    def test_create_data(self):
        data = {
            "branch": "stable",
            "date": "2020-05-04 22:25:45+02:00",
            "priority": "1",
            "body":
            """8devices-carambola2-board 2020.1.2-242-testing c8a7d3db620e91ad4d935bfc3df59f1a60bb3a2f11aa19a24b2f3d965cb88d06 4259844 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
8devices-carambola2-board 2020.1.2-242-testing c8a7d3db620e91ad4d935bfc3df59f1a60bb3a2f11aa19a24b2f3d965cb88d06 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
8devices-carambola2-board 2020.1.2-242-testing cffca7ec6dee0f4e1cb95fe79275a34cf791b92f76ba74e4d3e74c113e7eed40e5ae576c7f8da1e9cdc4dec71f14f8457111870647aafc5f41b048749d34b671 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
alfa-network-ap121f 2020.1.2-242-testing a21015a1cc0c46201e09fcdb87a9b03d9ecd0169ff1f8cab97a7e8b39767b87e 4326145 gluon-ffsh-2020.1.2-242-testing-alfa-network-ap121f-sysupgrade.bin""",
            "signature": "4b93f300b95e89342b2d49dc5fe4fbf1d89028ad48e00a09ecc2af86beb6380fea1cd8aa9f9f05a740dfa18589e7223a138920b7eb0639914b473cf4f37e7b04"
        }
        manifest = Manifest(data["branch"], data["date"], data["priority"], data["body"], data["signature"])
        self.assertEqual(manifest.branch, data["branch"])
        self.assertEqual(manifest.date, data["date"])
        self.assertEqual(manifest.priority, data["priority"])
        self.assertEqual(manifest.body, data["body"])
        self.assertEqual(manifest.signature, data["signature"])

    def test_merge(self):
        data1 = {
            "branch": "stable",
            "date": "2020-05-04 22:25:45+02:00",
            "priority": "1",
            "body":
            """8devices-carambola2-board 2020.1.2-242-testing c8a7d3db620e91ad4d935bfc3df59f1a60bb3a2f11aa19a24b2f3d965cb88d06 4259844 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
8devices-carambola2-board 2020.1.2-242-testing c8a7d3db620e91ad4d935bfc3df59f1a60bb3a2f11aa19a24b2f3d965cb88d06 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
8devices-carambola2-board 2020.1.2-242-testing cffca7ec6dee0f4e1cb95fe79275a34cf791b92f76ba74e4d3e74c113e7eed40e5ae576c7f8da1e9cdc4dec71f14f8457111870647aafc5f41b048749d34b671 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
alfa-network-ap121f 2020.1.2-242-testing a21015a1cc0c46201e09fcdb87a9b03d9ecd0169ff1f8cab97a7e8b39767b87e 4326145 gluon-ffsh-2020.1.2-242-testing-alfa-network-ap121f-sysupgrade.bin""",
            "signature": "4b93f300b95e89342b2d49dc5fe4fbf1d89028ad48e00a09ecc2af86beb6380fea1cd8aa9f9f05a740dfa18589e7223a138920b7eb0639914b473cf4f37e7b04"
        }
        data2 = {
            "branch": "stable",
            "date": "2020-05-04 22:25:45+02:00",
            "priority": "1",
            "body":
            """d-link-dir-615-d1 2020.1.2-242-testing a682e5a1063f14dbe9c3e3b50d953dfbdb18acecbf21e44d9f74495e44c965e0 gluon-ffsh-2020.1.2-242-testing-d-link-dir-615-d1-sysupgrade.bin
d-link-dir-615-d1 2020.1.2-242-testing a4e3adc705f5c9d1e09b5197d6b0e2b3741490ee02b2d4ccf18599e35fd09343588303017144c5c2dbaea54c641152875c43b1c692335dea360ebc46d0cd9200 gluon-ffsh-2020.1.2-242-testing-d-link-dir-615-d1-sysupgrade.bin
d-link-dir-615-d2 2020.1.2-242-testing a682e5a1063f14dbe9c3e3b50d953dfbdb18acecbf21e44d9f74495e44c965e0 3408646 gluon-ffsh-2020.1.2-242-testing-d-link-dir-615-d2-sysupgrade.bin
d-link-dir-615-d2 2020.1.2-242-testing a682e5a1063f14dbe9c3e3b50d953dfbdb18acecbf21e44d9f74495e44c965e0 gluon-ffsh-2020.1.2-242-testing-d-link-dir-615-d2-sysupgrade.bin
d-link-dir-615-d2 2020.1.2-242-testing a4e3adc705f5c9d1e09b5197d6b0e2b3741490ee02b2d4ccf18599e35fd09343588303017144c5c2dbaea54c641152875c43b1c692335dea360ebc46d0cd9200 gluon-ffsh-2020.1.2-242-testing-d-link-dir-615-d2-sysupgrade.bin
d-link-dir-615-d3 2020.1.2-242-testing a682e5a1063f14dbe9c3e3b50d953dfbdb18acecbf21e44d9f74495e44c965e0 3408646 gluon-ffsh-2020.1.2-242-testing-d-link-dir-615-d3-sysupgrade.bin
d-link-dir-615-d3 2020.1.2-242-testing a682e5a1063f14dbe9c3e3b50d953dfbdb18acecbf21e44d9f74495e44c965e0 gluon-ffsh-2020.1.2-242-testing-d-link-dir-615-d3-sysupgrade.bin
d-link-dir-615-d3 2020.1.2-242-testing a4e3adc705f5c9d1e09b5197d6b0e2b3741490ee02b2d4ccf18599e35fd09343588303017144c5c2dbaea54c641152875c43b1c692335dea360ebc46d0cd9200 gluon-ffsh-2020.1.2-242-testing-d-link-dir-615-d3-sysupgrade.bin
d-link-dir-615-d4 2020.1.2-242-testing a682e5a1063f14dbe9c3e3b50d953dfbdb18acecbf21e44d9f74495e44c965e0 3408646 gluon-ffsh-2020.1.2-242-testing-d-link-dir-615-d4-sysupgrade.bin""",
            "signature": "4b93f300b95e89342b2d49dc5fe4fbf1d89028ad48e00a09ecc2af86beb6380fea1cd8aa9f9f05a740dfa18589e7223a138920b7eb0639914b473cf4f37e7b04"
        }
        manifest1 = Manifest(data1["branch"], data1["date"], data1["priority"], data1["body"], data1["signature"])
        manifest2 = Manifest(data2["branch"], data2["date"], data2["priority"], data2["body"], data2["signature"])
        manifest1.merge(manifest2)
        new_body = "{}\n{}".format(data1["body"], data2["body"])
        self.assertEqual(manifest1.branch, data1["branch"])
        self.assertEqual(manifest1.date, data1["date"])
        self.assertEqual(manifest1.priority, data1["priority"])
        self.assertEqual(manifest1.body, new_body)
        self.assertEqual(manifest1.signature, data1["signature"])

    def test_export(self):
        data = {
            "branch": "stable",
            "date": "2020-05-04 22:25:45+02:00",
            "priority": "1",
            "body":
            """8devices-carambola2-board 2020.1.2-242-testing c8a7d3db620e91ad4d935bfc3df59f1a60bb3a2f11aa19a24b2f3d965cb88d06 4259844 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
8devices-carambola2-board 2020.1.2-242-testing c8a7d3db620e91ad4d935bfc3df59f1a60bb3a2f11aa19a24b2f3d965cb88d06 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
8devices-carambola2-board 2020.1.2-242-testing cffca7ec6dee0f4e1cb95fe79275a34cf791b92f76ba74e4d3e74c113e7eed40e5ae576c7f8da1e9cdc4dec71f14f8457111870647aafc5f41b048749d34b671 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
alfa-network-ap121f 2020.1.2-242-testing a21015a1cc0c46201e09fcdb87a9b03d9ecd0169ff1f8cab97a7e8b39767b87e 4326145 gluon-ffsh-2020.1.2-242-testing-alfa-network-ap121f-sysupgrade.bin""",
            "signature": "4b93f300b95e89342b2d49dc5fe4fbf1d89028ad48e00a09ecc2af86beb6380fea1cd8aa9f9f05a740dfa18589e7223a138920b7eb0639914b473cf4f37e7b04"
        }
        manifest = Manifest(data["branch"], data["date"], data["priority"], data["body"], data["signature"])
        manifest.export("stable.manifest")
        with open("stable.manifest", "r") as manifest_file:
            self.assertTrue(manifest_file.readlines())
        os.remove("stable.manifest")

    def test_load(self):
        self.maxDiff = None
        data = {
            "branch": "stable",
            "date": "2020-05-04 22:25:45+02:00",
            "priority": "1",
            "body":
            """8devices-carambola2-board 2020.1.2-242-testing c8a7d3db620e91ad4d935bfc3df59f1a60bb3a2f11aa19a24b2f3d965cb88d06 4259844 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
8devices-carambola2-board 2020.1.2-242-testing c8a7d3db620e91ad4d935bfc3df59f1a60bb3a2f11aa19a24b2f3d965cb88d06 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
8devices-carambola2-board 2020.1.2-242-testing cffca7ec6dee0f4e1cb95fe79275a34cf791b92f76ba74e4d3e74c113e7eed40e5ae576c7f8da1e9cdc4dec71f14f8457111870647aafc5f41b048749d34b671 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
alfa-network-ap121f 2020.1.2-242-testing a21015a1cc0c46201e09fcdb87a9b03d9ecd0169ff1f8cab97a7e8b39767b87e 4326145 gluon-ffsh-2020.1.2-242-testing-alfa-network-ap121f-sysupgrade.bin""",
            "signature": "4b93f300b95e89342b2d49dc5fe4fbf1d89028ad48e00a09ecc2af86beb6380fea1cd8aa9f9f05a740dfa18589e7223a138920b7eb0639914b473cf4f37e7b04"
        }
        manifest = Manifest(data["branch"], data["date"], data["priority"], data["body"], data["signature"])
        manifest.export("stable.manifest")
        with open("stable.manifest", "r") as manifest_file:
            self.assertTrue(manifest_file.readlines())
        manifest2 = Manifest()
        manifest2.load("stable.manifest")
        manifest2.export("stable2.manifest")
        self.assertEqual(manifest2.branch, data["branch"])
        self.assertEqual(manifest2.date, data["date"])
        self.assertEqual(manifest2.priority, data["priority"])
        self.assertEqual(manifest2.body, data["body"])
        self.assertEqual(manifest2.signature, data["signature"])

    def test_load_no_signature(self):
        self.maxDiff = None
        data = {
            "branch": "stable",
            "date": "2020-05-04 22:25:45+02:00",
            "priority": "1",
            "body":
            """8devices-carambola2-board 2020.1.2-242-testing c8a7d3db620e91ad4d935bfc3df59f1a60bb3a2f11aa19a24b2f3d965cb88d06 4259844 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
8devices-carambola2-board 2020.1.2-242-testing c8a7d3db620e91ad4d935bfc3df59f1a60bb3a2f11aa19a24b2f3d965cb88d06 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
8devices-carambola2-board 2020.1.2-242-testing cffca7ec6dee0f4e1cb95fe79275a34cf791b92f76ba74e4d3e74c113e7eed40e5ae576c7f8da1e9cdc4dec71f14f8457111870647aafc5f41b048749d34b671 gluon-ffsh-2020.1.2-242-testing-8devices-carambola2-board-sysupgrade.bin
alfa-network-ap121f 2020.1.2-242-testing a21015a1cc0c46201e09fcdb87a9b03d9ecd0169ff1f8cab97a7e8b39767b87e 4326145 gluon-ffsh-2020.1.2-242-testing-alfa-network-ap121f-sysupgrade.bin"""
        }
        manifest = Manifest(data["branch"], data["date"], data["priority"], data["body"])
        manifest.export("no-sig.manifest")
        with open("no-sig.manifest", "r") as manifest_file:
            self.assertTrue(manifest_file.readlines())
        manifest2 = Manifest()
        manifest2.load("no-sig.manifest")
        manifest2.export("no-sig2.manifest")
        self.assertEqual(manifest2.branch, data["branch"])
        self.assertEqual(manifest2.date, data["date"])
        self.assertEqual(manifest2.priority, data["priority"])
        self.assertEqual(manifest2.body, data["body"])
        # self.assertEqual(manifest2.signature, data["signature"])

if __name__ == '__main__':
    unittest.main()
