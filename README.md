Storing large files in memcached
===

### Pre-requisites

- A working `python2.7` and `virtualenv` installation.

### Getting started

```
./scripts/setup.sh ~/.venv/chunker  # Install dependencies
source ~/.venv/chunker/bin/activate # Activate venv
python test.py                     # Run a test script to see if everything works well
```

Expected output:

```
Setting key - foo:  True
Retrieved value of foo:  bar
Max memory:  1048576000
```

You're all set!

### The task

Storing big files in Memcached

Running the tests:

`python -m unittest chunker.tests`
