#! python3

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
        print("lel")

    def export(self, file):
        """
        exports the manifest to a file
        """
        # create file
        # write to file