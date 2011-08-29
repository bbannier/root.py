#!/bin/env ipython
import ROOT as r
import sys
import IPython.ipapi

try:
  from matplotlib import pyplot
  import numpy as np
  pyplot.ion()

  def extractData(h):
    dimension = h.GetDimension()
    if dimension==1:
      x  = [h.GetBinCenter(i)  for i in xrange(h.GetXaxis().GetNbins())]
      y  = [h.GetBinContent(i) for i in xrange(h.GetXaxis().GetNbins())]
      xe = [h.GetBinWidth(i)   for i in xrange(h.GetXaxis().GetNbins())]
      ye = [h.GetBinError(i)   for i in xrange(h.GetXaxis().GetNbins())]
      return x, y, xe, ye
    elif dimension==2:
      nx = h.GetXaxis().GetNbins()
      ny = h.GetYaxis().GetNbins()
      x  = [h.GetXaxis().GetBinCenter(i) for i in xrange(nx)]
      y  = [h.GetYaxis().GetBinCenter(i) for i in xrange(ny)]
      z  = [h.GetBinContent(ix, iy) for ix in xrange(nx) for iy in xrange(ny)]
      z  = np.array(z).reshape((nx, ny))

      return x, y, z

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
      elif h.GetDimension()==2:
        x, y, z = extractData(h)
        pyplot.contour(y, x, z.tolist(), colors='k')
      pyplot.show()

    except AttributeError:
      pyplot.plot(h)

except ImportError:
  pass
##################################################

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

# vi:filetype=python
