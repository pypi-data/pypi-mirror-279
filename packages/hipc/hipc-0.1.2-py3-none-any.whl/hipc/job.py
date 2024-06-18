import os
import json
import multiprocessing as mp

class Parameters(object):
    """An structure of parameters which can be indexed
    like a dictionary. The intended use is to create a set of
    parameters with a unique set of easy to remember keys with readable
    values (numbers, strings, not collections and general objects).

    Args:
        filename (str): The file name of the parameter save.
    """

    def __init__(self, p={}):
        #: (set) Named tags that apply to this parameter set.
        self._tags = set() # TODO: implement

        self.set(p)

    def __index__(self, s):
        return getattr(self, s)

    def map(self):
        """Return the set of parameters and their default values
        as a python dictionary."""
        return {k: v for k, v in self.__class__.__dict__.items()
                if "__" not in k}

    def tag(self, tags):
        """Add a tag, or set of tags so this set of parameters can be
        searchable for later.

        Args:
            tags (str, or set[str]): The tags that apply to this set of
            parameters.
        """
        if not isinstance(tags, set): tags = {tags}
        self._tags = self._tags.union(tags)

    def set(self, p):
        """Take a dictionary of values and set the corresponding
        attributes of this object."""
        for k, v in p.items():
            setattr(self, k, v)

    def write(self):
        """Store parameters to file in a human readable format."""
        with open (self.filename, "w") as f:
            json.dump(self.map(), f, indent=4)

    def read(self):
        """Read in parameters from json file."""
        with open (self.filename, "r") as f:
            d = json.load(f)

    def pretty(self, a):
        """Optional pretty print mapping for each param."""
        pass

    def set(self, p):
        """Take a dictionary of values and set the corresponding
        attributes of this object."""
        for k, v in p.items():
            setattr(self, k, v)

    def __repr__(self):
        s = pd.Series(self.map()).__repr__()
        s = "\n".join(s.split("\n")[:-1])
        return s

class JobManager(object):
    pass

#: SLURM parameters
slurm_options = {
    # The HPC user account
    "account": None, # required
    "job-name": None, # required
    "ntasks-per-node": None, # required, number of cores in each compute node
    "qos": None, # Quality of service
    "reservation": None, # Request particular resources
    "time": 60, # job minutes
    "array": None, # option for multi-task submission.
    "bb": None, "bbf": None, # burst buffer
    "begin": None, # scheduled runtime
    "chdir": None, # working directory of cluster process
    "clusters": None, # comma separated string of clusters
    "comment": None, # slurm script comment
    "constraint": None, # more constraints
    "deadline": None,
    "error": "job.err",
    "output": "job.out",
    "mail-user": None,
    "mail-type": None,
    # name / cpu / task / node allocation left to Manager
}

class Calculator(object):
    """Interface for any kind of calculation that is run-able
    and set-able can be compatible with multiprocessing utilities like
    SlurmManager and DistributedPool."""

    def set_(self, **state_options):
        """Update the internal state of the object being run.

        Args:
            **state_options: Keywords arguments corresponding to attributes of the object
                being updated.
        """
        raise NotImplementedError("Calculator must implement set_(self, **state_options) function.")

    def run(self, **run_options):
        """Run the calculation with the current settings.

        Args:
            **run_options: Keywords arguments that modify the nature of the
                way the program runs.
        """
        raise NotImplementedError("Calculator must implement set_(self, **run_options) function.")

    def get_directory(self):
        """Return the directory in which the calculation is occurring.

        Returns
            (str): The path of the directory in which the program is being run.
        """
        raise NotImplementedError("Calculator must implement get_directory(self) function.")

    def extract(self, query, process):
        """Extract data from the calculation."""

    def to_pickleable(self):
        """Returns a pickle-able portion of the object sufficient to run
        the calculations."""
        raise NotImplementedError("Calculator must implement to_picklable(self) function.")

class DistributedPool(object):
    """A multiprocessing Pool context for running
    calculations among cores with different settings.

    Args:
        runner (Calculator): The calculation runner.
        processes (int): The number of cores to divide up the work.
    """

    def __init__(self, runner: Calculator, processes=None):
        # Always use the fork context
        mpc = mp.get_context("fork")
        self.runner = runner
        self.pool = mpc.Pool(processes=processes)

    def submit(self, run_args={}, **set_args):
        """Submit a single job with updated key words to the pool.

        Args:
            run_args (dict): Keyword arguments to be passed to
                :meth:`~.hipc.job.Calculator.run`.
        **set_args: Keyword arguments passed to
            :meth:`~.hipc.job.Calculator.set_`
            before calling :meth:`~.hipc.job.Calculator.run`.
        """
        # Copy the state of the runner (this ensures that
        # the parameter state does not get overwritten while
        # the processors are all busy)
        self.runner_child = copy.deepcopy(self.runner)
        # Keyword args will be sent to the set function
        self.runner_child.set_(**set_args)
        # run_args are sent separately with the caller
        self.pool.apply_async(
            self.runner_child.run, (), run_args,
            error_callback=self.err_callback)

    def __enter__(self):
        """Pipe the context input back to caller."""
        self.pool.__enter__()
        return self

    def err_callback(self, err):
        """Print out errors that subprocesses encounter."""
        path = self.runner.get_directory()
        warnings.warn(f"Error in process: PID={os.getpid()} "
                      f"path={path}\n\n{str(err)}", RuntimeWarning)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Safely wait for all processes to finish and exit the pool."""
        # Stop accepting jobs
        self.pool.close()
        # Wait for all jobs to finish
        self.pool.join()
        # Terminate multiprocessing pool
        self.pool.__exit__(exc_type, exc_val, exc_tb)

class SlurmManager(object):
    """A python context interface for the common Slurm HPC job manager
    to run more several intensive calculations on large clusters.
    See https://slurm.schedmd.com/sbatch.html.

    Args:
        runner (Calculator): The calculation runner.
        directory (str or None) The simulation directory. Default is
            the current working directory.
        modules (list[str]): A list of modules to be loaded by the
            HPC module system.
        mock (bool): Option to test scripts without calling a slurm
            manager.
        **options: Additional keyword arguments will be interpreted as
            SLURM parameters.

    Note:
        This job manager currently only works for clusters that either
        already have the gcc and python requirements installed on each
        compute node, or clusters that use the
        `Module System <https://hpc-wiki.info/hpc/Modules>`_ to load
        functionality.
 
        The default behavior is to accommodate the module system as it
        is common on most HPC machines. If you wish to avoid writing
        ``module load`` commands in the SLURM script, simply specify
        ``modules=[]`` in the constructor.
    """
    _pckl_file = "job.pckl"
    def __init__(self, runner: Calculator, directory=None, modules=["python", "gcc"],
            mock=False, **options):
        if directory is None:
            directory = os.getcwd()
        # Make group directory absolute
        if not os.path.isabs(directory):
            directory = str(Path(directory).resolve())
        #: The simulation directory
        self.directory = directory
        #: The list of modules to be loaded by the HPC module system.
        self.modules = modules
        #: The :class:`~.hipc.job.Calculator` object.
        self.runner = runner
        # Option to test the scripts without calling a slurm manager
        self.mock = mock
        # These will hold all the updates to both slurm and the runner
        self.input_sets = []
        #: Store references to the slurm job numbers after jobs are submitted
        self.job_ids = []
        #: The SLURM sbatch options
        self.options = slurm_options.copy()
        self.set_(**options)
        # Make sure cores are specified
        msg = (f"{self.__class__.__name__} requires "
                "the number of cores available at each node "
                "to be passed as ntasks-per-node.")
        if not "ntasks-per-node" in self.options:
            raise RuntimeError(msg)
        if not self.options["ntasks-per-node"]:
            raise RuntimeError(msg)

        # Assume fixed number of cores, store value
        self.ncores = self.options["ntasks-per-node"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit and run sbatch for all the inputs"""
        ntasks = len(self.input_sets)
        nodes_required = int(np.ceil(ntasks / self.ncores))
        for start in range(nodes_required):
            # Isolate the inputs for this node
            inputs = self.input_sets[
                int(start*self.ncores):int(min((start+1)*self.ncores, ntasks))
            ]
            # Take any slurm updates from first input
            self.set_(**inputs[0])
            # Create a directory for slurm files of this node
            node_dir = pjoin(self.directory, f"NODE_{start+1}")
            os.makedirs(node_dir)
            with visit(node_dir):
                # Write pickle of input at the directory level
                with open(self._pckl_file, "wb") as f:
                    pickle.dump((inputs, self.runner), f)
                # Write the slurm script
                self.write_slurm_script()
                # Execute slurm call
                self.sbatch()

    def submit(self, run_args={}, **settings):
        """Add a set of parameter updates to the job queue.
        Slurm is not invoked until the context is exited.

        Args:
            run_args (dict): Keyword arguments to be passed to
                :meth:`~.hipc.job.Calculator.run`.
            **settings: Keyword arguments passed to the
                :meth:`~.hipc.job.Calculator.set_`.
                before calling :meth:`~.hipc.job.Calculator.run`.
        """
        # Resolve relative paths
        if not os.path.isabs(settings["directory"]):
            settings["directory"] = str(Path(settings["directory"]).resolve())

        combined_settings = {"run_args": run_args}
        combined_settings.update(**settings)
        self.input_sets.append(combined_settings.copy())

    def sbatch(self):
        """Call slurm with current settings."""
        if self.mock:
            # Just call the script and block
            self.mock_run()
            return
        # Otherwise, submit to slurm
        cmds = ["date | tee -a jobnum", "sbatch job_script.sh | tee -a jobnum"]
        subprocess.run(cmds[0], shell=True)
        sub_string = subprocess.check_output(cmds[1], shell=True).decode()
        self.job_ids.append(int(sub_string.split()[-1]))

    def set_(self, **options):
        """Update slurm manager options.

        Args:
            **options: SLURM settings.
        """
        self.options.update({k:v
            for k, v in options.items()
            if k in slurm_options})

    def write_slurm_script(self, path=None, script_name=None):
        """Write the SLURM batch script."""
        if script_name is None:
            script_name = "job_script.sh"
        if path is None:
            path = os.getcwd()
        with open(pjoin(path, script_name), "w") as f:
            f.write("#!/bin/bash\n")
            for k, v in self.options.items():
                if not v:
                    continue
                f.write(f"#SBATCH --{k}={v}\n")

            if not self.mock:
                # Only load modules if this is a real slurm run
                f.write("\n")
                for mod in self.modules:
                    f.write(f"module load {mod}\n")
                f.write("\n\n")

            python_script = self.process_batch_script()
            # Declare pyscript var
            f.write("SCRIPT=$(cat<<END\n")
            f.write(python_script)
            f.write("END\n")
            f.write(")\n\n")
            f.write("python -c \"$SCRIPT\"\n")

    def process_batch_script(self):
        """Inspect the batch script below and process it for use
        in sbatch."""
        source = inspect.getsource(self.batch_script)
        source = "\n".join(source.split("\n")[4:])
        # Inject ncores
        source = source.replace("ncores = None", f"ncores = {self.ncores}")
        # Inject pckl name
        source = source.replace("self._pckl_file", f"\"{self._pckl_file}\"")
        # Remove indents
        source = re.sub("^[^\S\n]{8}", "", source, flags=re.MULTILINE)
        return source

    def batch_script(self):
        """The SLURM job script. This does not get called in the
        parent process, but instead the source code is invoked in the
        sbatch script/command for subprocess startup."""
        import pickle
        from hipc.job import DistributedPool
        from hipc.job import slurm_options
        # number of cores and directory will be injected in sbatch
        ncores = None
        # Load in batch parameters
        with open(self._pckl_file, "rb") as f:
            updates, runner = pickle.load(f)
        # Run settings through distruted processing interface
        with DistributedPool(runner, processes=ncores) as pool:
            for update in updates:
                # Separate submit args
                submit_args = {k: v for k, v in update.items()
                    if k not in slurm_options}
                pool.submit(**submit_args)

    def mock_run(self):
        """Act as a compute node and test the job scripts sequentially."""
        os.system(f"chmod +x job_script.sh")
        os.system(f"./job_script.sh")

    def has_active(self):
        """Check whether any submitted jobs are still pending or running.

        Returns:
            (bool): ``True`` if there are still jobs that are pending or
                running. ``False`` otherwise.
        """
        has_active = False
        for job_id in self.job_ids:
            is_active = False
            try:
                cmd = f"scontrol show job {job_id}"
                sub_string = subprocess.check_output(
                    shlex.split(cmd)).decode()
                is_active = "PENDING" in sub_string or "RUNNING" in sub_string
            except subprocess.CalledProcessError as e:
                is_active = False
            has_active = has_active or is_active
        return has_active

    def has_pending(self):
        """Check whether any submitted jobs are still pending.

        Returns:
            (bool): ``True`` if there are still jobs that are pending.
                ``False`` otherwise.
        """
        has_pending = False
        for job_id in self.job_ids:
            is_active = False
            try:
                cmd = f"scontrol show job {job_id}"
                sub_string = subprocess.check_output(
                    shlex.split(cmd)).decode()
                is_pending = "PENDING" in sub_string
            except subprocess.CalledProcessError as e:
                is_pending = False
            has_pending = has_pending or is_pending
        return has_pending

    def join(self):
        """Wait for all slurm jobs to finish."""
        while self.has_active():
            time.sleep(2)

class visit(object):
    """Directory environment context manager."""
    def __init__(self, path):
        self.original_path = os.getcwd()
        self.path = path

    def __enter__(self):
        os.chdir(self.path)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.original_path)


