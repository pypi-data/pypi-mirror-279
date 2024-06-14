# Time-X EuroHPC project: Dynamic Resource Manager

This repo contains a Python-based dynamic resource manager to be used with the [Time-X dynamic MPI Extensions](https://gitlab.inria.fr/dynres/dyn-procs/ompi).

The resource manager connects as PMIx Tool to the PMIx server of Dyn_PRRTE and can then control PSet operations and spawn new jobs. 

At the moment it only supports very basic management, but it can be extended with more sophisticated scheduling policies (see corresponding class in my_system.py)

## Installation

### Installation using `pip`
We provide regular releases of this package.
Dynamic Resources require changes in the whole system software stack.
Thus, changes in our 
[dynamic MPI Extensions](https://gitlab.inria.fr/dynres/dyn-procs/ompi),
[dynamic PMIx Extensions](https://gitlab.inria.fr/dynres/dyn-procs/openpmix) and
[dynamic PRRTE Extensions](https://gitlab.inria.fr/dynres/dyn-procs/prrte)
might break compatibility with the dynamic resource manager.
We give our best to provide up to date releases and version information.
However, to be on the save site we recommend to manually install the package (see below)
and run it with the most recent versions of our dynamic extensions.

If you want to use pip for the installation run:

```
pip install dyn_rm
```
### (Recommended) Manual Installation
To ensure compatibility with our dynamic MPI, PMIx and PRRTE Extensions it is recommended 
to use a manual installation. This version is tested with the corresponding most recent versions
of the dynamic extensions.

* Clone this repository:
```
git clone https://gitlab.inria.fr/dynres/dyn-procs/dyn_rm
```
* Then, from this directory run:
```
python3 setup.py install --user
```

### Installation with Spack
coming soon ...

## Running the resource manager

The command to run jobs with the dynamic resource manager is:

```
dyn_rm [ARGS]

Args:
    --jobs=[path_to_job_mix_file] (Required):
        A job-mix files is a text file, where each line represents a job to be scheduled.
        The format of each line is:
        {"name": <job_name>, "cmd": <mpirun_cmd>, "start_time": <time of job submission (sec)>}
    
    --host=[host1:slots,...,hostN:slots] (Required):
        Specifies the hosts of the system managed by the resource manager.
        The syntax is similar to the mpirun's 'host' option
    
    --policy=[policy_name] (Optional):
        The policy to be used by the resource manager
        Options: {'default', 'dmr'}
        Default: 'default' 
    
    --verbosity=[0,4] (Optional):
        The verbosity level: higher = more output
        Default: 0

    --sched_interval=[float] (Optional):
        The interval of scheduling decisions in seconds
        Default: 1

    --server_pid=[int] (Optional):
        The PID of the PMIx server to connect to. 
        If no PID is given, a persitent PRRTE instance will be started on the specified nodes
    
    --output=[path_to_outputfile.csv] (Optional)
        If an output file is specified, the resource manager will write output regarding the node occupatin to this file.
```


There are example job mix files provided in the examples subdirectory.
The basic command to run the resource manager on a system with 4 nodes á 8 slots and the job mix file "job_mix_alternate.txt" looks as like this:

```
dyn_rm --jobs=examples/job_mix_alternate.txt --host=n01:8,n02:8,n03:8,n04:8
```

