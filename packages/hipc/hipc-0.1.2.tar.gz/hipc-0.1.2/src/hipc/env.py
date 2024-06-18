"""Use a tag based system to recover file identities."""
import datetime

from hipc import Parameters

class EnvTree():
    """Environment manager for tests on HPC machines. It is usually desirable to
    create a new environment (directory) for every calculation that has a different
    set up inputs. This object makes it easy to create new trees of tests, make them
    searchable, and have them intereact with HPC job managers to determine if it is safe
    to change data in the tree."""

    def __init__(self, root, interactive=False):
        #: (str) The abolute root path of this tree
        self.root = TestNode(root)
        #: Store associate tags
        self.tag_map = {}

        self.index = 1

    def create_env(self, p):
        # For now, independent of p
        ts = datetime.now()
        subdir = f"{self.index} {ts}".replace(" ", "_")
        print(subdir)
        os.makedir()

    def serve()


class TestNode():
    """"""
    def __init__(self, path, p):
        self.path = 
        pass
