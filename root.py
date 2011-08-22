#!/bin/env ipython
import ROOT as r
import sys
import IPython.ipapi

_ip = IPython.ipapi.get()

r.gROOT.ProcessLine('.x ~/.root_logon.C')

_f = []
args = sys.argv[1:]
for a in args:
  if a.endswith('.C'):
    print "Processing %s" %(a)
    r.gROOT.ProcessLine('.x %s' %(a))
  elif a.endswith('.py'):
    print "Processing %s" %(a)
    _ip.magic('run -i %s' %(a))
  elif a.endswith('.root'):
    print "Loading %s as _f[%s]" %(a, len(_f))
    _f.append(r.TFile(a))
  elif a.endswith('.hbk'):
    print "Loading %s as _f[%s]" %(a, len(_f))
    _f.append(r.THbookFile(a))

##################################################
try:
  from matplotlib import pyplot
  pyplot.ion()

  def extractData(h):
    x  = [h.GetBinCenter(i)  for i in xrange(h.GetXaxis().GetNbins())]
    y  = [h.GetBinContent(i) for i in xrange(h.GetXaxis().GetNbins())]
    xe = [h.GetBinWidth(i)   for i in xrange(h.GetXaxis().GetNbins())]
    ye = [h.GetBinError(i)   for i in xrange(h.GetXaxis().GetNbins())]
    return x, y, xe, ye

  def errorbar(h):
    try:
      if h.GetDimension()==1:
        x, y, xe, ye = extractData(h)
        pyplot.errorbar(x, y, ye, xe, fmt='.')
        pyplot.show()

    except AttributeError:
      pyplot.errorbar(h)

  def plot(h):
    try:
      if h.GetDimension()==1:
        x, y, _, _ = extractData(h)
        pyplot.plot(x, y, 'h')
        pyplot.show()

    except AttributeError:
      pyplot.plot(h)

except ImportError:
  pass

# vi:filetype=python
