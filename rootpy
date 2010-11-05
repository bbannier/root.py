#!/bin/env ipython
import ROOT as r
import sys

r.gROOT.ProcessLine('.x ~/.root_logon.C')

_f = []
args = sys.argv[1:]
for a in args:
  if a.endswith('.C'):
    print "Processing %s" %(a)
    r.gROOT.ProcessLine('.x %s' %(a))
  if a.endswith('.root'):
    print "Loading %s as _f[%s]" %(a, len(_f))
    _f.append(r.TFile(a))

# vi:filetype=python
