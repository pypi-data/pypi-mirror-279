# hipc

Submission, storage, and extraction on HPC machines.

## Setup Sockets

in $HOME/.ssh/config, add lines of the form.
This will allow remote login through ssh without the need for a password
once an initial shell connection is establish.

```
Host <<host_name>>*
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h:%p
```

## Installation

```bash
$ pip install hipc
```

## Usage

- TODO
