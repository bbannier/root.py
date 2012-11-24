#!/bin/env ipython

"""
Copyright 2010-2012 Benjamin Bannier

This program is free software. It comes without any warranty, to the extent
permitted by applicable law. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2, as
published by Sam Hocevar. See http://sam.zoy.org/wtfl/COPYING for more details.
"""

import ROOT as r
import sys
import IPython.ipapi

try:
    from matplotlib import pyplot
    import numpy as np
    pyplot.ion()

    def set_axis_labels(h):
        pyplot.xlabel(h.GetXaxis().GetTitle())
        pyplot.ylabel(h.GetYaxis().GetTitle())

    def set_axis_ranges(h):
        pyplot.xlim(h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax())
        if h.GetDimension() > 1:
            pyplot.ylim(h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax())

    def extractData(data):
        if data.InheritsFrom('TH1'):
            dimension = data.GetDimension()
            nx = data.GetXaxis().GetNbins()
            x = [data.GetBinCenter(i) for i in xrange(nx)]
            if dimension == 1:
                y = [data.GetBinContent(i) for i in xrange(nx)]
                xe = [data.GetBinWidth(i) for i in xrange(nx)]
                ye = [data.GetBinError(i) for i in xrange(nx)]
                return x, y, xe, ye
            elif dimension == 2:
                ny = data.GetYaxis().GetNbins()
                y = [data.GetYaxis().GetBinCenter(i) for i in xrange(ny)]
                z = [data.GetBinContent(ix, iy)
                    for ix in xrange(nx) for iy in xrange(ny)]
                z = np.array(z).reshape((nx, ny))
                return x, y, z
        elif data.InheritsFrom('TF1'):
            x = np.linspace(\
                data.GetXaxis().GetXmin(), data.GetXaxis().GetXmax(), 100)
            y = [data.Eval(X) for X in x]
            return x, y, None, None

    def errorbar(h):
        try:
            if h.GetDimension() == 1:
                x, y, xe, ye = extractData(h)
                pyplot.errorbar(x, y, ye, xe, fmt='.')
                for f in h.GetListOfFunctions():
                    fx, fy, _, _ = extractData(f)
                    pyplot.plot(fx, fy, '-')
                set_axis_labels(h)
                set_axis_ranges(h)
                pyplot.show()

        except AttributeError:
            pyplot.errorbar(h)

    def plot(h):
        try:
            if h.GetDimension() == 1:
                x, y, _, _ = extractData(h)
                pyplot.plot(x, y, 'h')
                for f in h.GetListOfFunctions():
                    fx, fy, _, _ = extractData(f)
                    pyplot.plot(fx, fy, '-')
            elif h.GetDimension() == 2:
                x, y, z = extractData(h)
                pyplot.contour(y, x, z.tolist(), colors='k')
            set_axis_labels(h)
            set_axis_ranges(h)
            pyplot.show()

        except AttributeError:
            pyplot.plot(h)

except ImportError:
    pass

##################################################

def set_color(hist, color):
  hist.SetMarkerColor(color)
  hist.SetLineColor(color)

##################################################

_ip = IPython.ipapi.get()

r.gROOT.ProcessLine('.x ~/.root_logon.C')

_f = []
args = sys.argv[1:]
for a in args:
    if a.endswith('.C'):
        print "Processing %s" % (a)
        r.gROOT.ProcessLine('.x %s' % (a))
    elif a.endswith('.py'):
        print "Processing %s" % (a)
        _ip.magic('run -i %s' % (a))
    elif a.endswith('.root'):
        print "Loading %s as _f[%s]" % (a, len(_f))
        _f.append(r.TFile(a))
    elif a.endswith('.hbk'):
        print "Loading %s as _f[%s]" % (a, len(_f))
        _f.append(r.THbookFile(a))

# vi:filetype=python tabstop=4 foldmethod=indent
