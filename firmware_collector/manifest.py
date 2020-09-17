#! python3

import re


class Manifest():
    def __init__(self, branch="", date="", priority="", body="", signature=""):
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
            imported = import_file.read()

        result = imported.split("\n\n")
        header = result[0]
        body = result[1]

        if "---" in body:
            body, signature = body.split("---")
        else:
            signature = ""

        pattern = re.compile(r'BRANCH=(\w+)\nDATE=(.*)\nPRIORITY=(\d)')
        header = pattern.match(header)

        self.branch = header.group(1)
        self.date = header.group(2)
        self.priority = header.group(3)
        self.body = body.lstrip("\n").rstrip("\n")
        self.signature = signature.strip("\n")

    def export(self, file):
        """
        exports the manifest to a file
        """
        with open(file, "w") as export_file:
            # the autoupdate doesn't like the space that the sign script will leave if there is a newline
            if self.signature != "":
                print("BRANCH={branch}\nDATE={date}\nPRIORITY={priority}\n\n\n{body}\n---\n{signature}".format(
                    branch=self.branch,
                    date=self.date,
                    priority=self.priority,
                    body=self.body,
                    signature=self.signature), file=export_file, end='')
            else:
                print("BRANCH={branch}\nDATE={date}\nPRIORITY={priority}\n\n\n{body}".format(
                    branch=self.branch,
                    date=self.date,
                    priority=self.priority,
                    body=self.body), file=export_file, end='')