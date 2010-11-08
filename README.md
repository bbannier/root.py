root.py
=======

`root.py` is a simple wrapper to replace the interactive ROOT plot with
ipython.

All it does is import the ROOT namespace as `r` and do some argument
processing:

* ROOT files are loaded into an array `_f`.
* CINT macros are processed.

Usually command line arguments will be handed to ipython first. Use `--` to
clearly separate ipython and root.py arguments.
