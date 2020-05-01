# clam

clam is a **c**luster/**l**ocal **a**ctivity **m**onitor

Currently it can display CPU usage for CPUs on the local machine.

Tested with Python 3.7.6

## Setup

Install with system-wide Python:

```bash
pip3 install -r requirements.txt
```

Install within a virtual environment (requires `virtualenv` Python package):

```bash
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Run

**Cluster**

```bash
python3 clam.py --nodes host1 [host2 host3 ... ]
```

This will show overall CPU activity for each node provided.

**Local**

```bash
python3 clam.py --local
```

This will show CPU activity of all logical CPUs on the local machine.
