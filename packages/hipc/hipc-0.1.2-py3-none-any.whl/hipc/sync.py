from datetime import datetime
import os
from os.path import expandvars as expand
from os.path import join as pjoin
from pathlib import Path
import subprocess
from subprocess import PIPE
import time
import warnings

class Port(object):
    """HPC port object. Sync source code and data, pass python functions
    through here and have them execute on a remote machine.
    
    Args:
        directory (str): The path of the HPC source directory to sync with.
            Can be absolute or relative to $HOME.

    """
    def __init__(self, directory, user, host):
        #: (str) The relative path of the HPC source directory.
        self.directory = directory
        #: (str) The user name on the HPC machine.
        self.user = user
        #: (str) The full domain name of the host machine.
        self.host = host
        #: (str) The account + host domain string
        self.account = user + "@" + host

        # Get remote base directory for this port, default is $HOME.
        self.remote_base = self.get_remote_home()
        self.env_path = pjoin(self.remote_base, self.directory)

        #: Groups of source files to be synced with HPC
        self.src_groups = {}

        #: Store the scratch directory associated with this machine, default
        # to remote home.
        self.scratch_dir = self.remote_base

        # Option to install conda requirements in HPC env
        self._requirements = False

        # By default, add local python files
        self.match_src()

    def upload(self, options="a", dryrun=False, delete=True, verbose=False):
        """Upload source files and data to the HPC machine.

        Args:
            options (str): rsync options.
                Default is ``"a"``.
            dryrun (bool): rsync dry run.
            delete (bool): Option to delete files at destination that are no
                longer in source.
        """
        drystr = "--dry-run" if dryrun else ""
        delstr = "--delete" if delete else ""
        dest_str = f"{self.account}:{self.env_path}"
        vstr = "-"+verbose if verbose else ""

        for root, filters in self.src_groups.items():
            if verbose: print(f"rsync -{options} {vstr} \\\n{filters}{drystr} "
                              f"{delstr} \\\n{root} {dest_str}")
            os.system(f"rsync -{options} {vstr} \\\n{filters}{drystr} "
                              f"{delstr} \\\n{root} {dest_str}")

    def establish_dir(self, path, scratch=False):
        """Create a directory relative to home or the scratch dir."""
        if scratch: abs_path = pjoin(self.scratch_dir, path)
        else: abs_path = pjoin(self.remote_base, path)
        args = ["ssh", "-tt", self.account, "mkdir", "-p", abs_path]
        subp_pipe(args, v=False, verr=False)

    def execute(self, executable, idev=False):
        if idev:
            # Start an MPI interactive job in a tmux session. Access the
            # environment on host with tmux or other server.
            args = ["ssh", "-tt", self.account, (
                f"tmux send \"source /etc/profile;"
                # f"source ~/{profile} && module load python"
                f"&& cd {self.env_path} && {executable}\" Enter")]
        else:
            args = ["ssh", self.account, (
                f"source /etc/profile; " # source ~/{profile} &&
                f"module load python && cd {self.env_path} &&"
                f"{executable}")]
        # Run the process and pipe output back to stdin continuously
        subp_pipe(args)

    def deploy(self, executable, idev=False, download=False):
        self.upload()
        self.execute(executable, idev=idev)
        if download: self.download()

    def __call__(self, module, function, interactive=False, download=True):
        """Call a python function on the HPC machine.

        Args:
            module (str): Name of a python module available in the environment.
            function (str): Name of a function to call from HPC which accepts
                no arguments.
        """
        e = f"python -c \'import {module};{module}.{function}()\'"
        if self._requirements:
            e = f"conda install --yes --file {self._requirements}; {e}"
        self.deploy(e, idev=interactive, download=download)

    def download(self, options=""):
        pass

    def get_remote_home(self):
        """Find the home directory on the remote server."""
        args = ["ssh", "-tt", self.account, "echo \"__remote_home_slug\"; pwd"]
        lines = subp_pipe(args, v=False, verr=False)
        # TODO: fix error message for only connection failure
        if not len(lines): raise RuntimeError("Remote not available")
        remote_home = lines[lines.index("__remote_home_slug")+1]
        return remote_home

    def scratch(self, path):
        """Use the scratch directory instead of the home directory."""
        self.scratch_dir = path

    def match_src(self, include="**.py", exclude=[], root="."):
        """Include and exclude source files for sync operation.

        Args:
            root (callable[str]): A local base directory to export from.
            include (str or list): Include pattern or list of patterns relative to root.
                By default, recursively include python files.
            exclude (str or None): Exclude files matching pattern even if they are 'included'.
        """
        # Start by excluding main files
        exclude = ensure_list(exclude)
        include = ensure_list(include)
        efinal = f"--exclude='**' \\\n" # Exclude the rest
        if root != ".":
            root_base = Path(root).parts[-1]
            exclude = [pjoin(root_base, e) for e in exclude]
            include = [pjoin(root_base, e) for e in include]
            efinal = f"--exclude='{pjoin(root_base, '**')}' \\\n"
        estr = "".join(f"--exclude='{exc}' \\\n" for exc in exclude)
        istr = "".join(f"--include='{inc}' \\\n" for inc in include)
        self.src_groups[root] = estr+istr+efinal

    def add_requirements(path):
        """Add a conda requirements file"""
        self.match_src(path)
        self._requirements = path

def subp_pipe(args, v=True, verr=True):
    """Run the process and pipe output back to stdin continuously."""
    p = subprocess.Popen(args, stdout=PIPE, stderr=PIPE)
    stdout = []
    while not p.poll():
        line = p.stdout.readline().decode().rstrip()
        if not line: break
        if v: print(line, flush=True)
        stdout.append(line)
    err = "".join(s.decode() for s in p.stderr.readlines())
    if err and verr: warnings.warn(err, RuntimeWarning)
    return stdout

def ensure_list(x):
    if not isinstance(x, list): return [x]
    else: return x
