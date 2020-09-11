#! python3

import re


class Manifest():
    def __init__(self, branch=None, date=None, priority=None, body=None, signature=None):
        self.branch = branch
        self.date = date
        self.priority = priority
        self.body = body
        self.signature = signature

    def set_branch(self, branch):
        """
        set the branch, allowing you to hand out the same manfiest in more than one version
        """
        self.branch = branch

    def merge(self, manifest):
        """
        merges the body of the incoming manfiest into this one
        """
        self.body = "{}\n{}".format(self.body, manifest.body)

    def load(self, file):
        """
        loads the manifest from file
        """
        with open(file, "r") as import_file:
            imported = import_file.readlines()
        # imported needs to be parsed
        pattern = re.compile(r'BRANCH=(\w+)\nDATE=(.*)\nPRIORITY(=\d)\n\n(.*\n*)*(-{3}|)(.+)*')
        matched = re.match(pattern, imported)
        self.branch = matched[1]
        self.date = matched[2]
        self.priority = matched[3]
        self.body = matched[4]
        self.signature = matched[5]

    def export(self, file):
        """
        exports the manifest to a file
        """
        with open(file, "rw") as export_file:
            export_file.write("BRANCH={}\n".format(self.branch))
            export_file.write("DATE={}\n".format(self.date))
            export_file.write("PRIORITY={}\n\n".format(self.priority))
            export_file.write("{}\n".format(self.body))
            export_file.write("---\n")
            export_file.write("{}".format(self.signature))