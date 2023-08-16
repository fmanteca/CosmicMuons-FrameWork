import sys
import os
import ROOT as r
import numpy as np
import library
import argparse
from datetime import datetime
from Plot import Plot

# import library
cutslib = library.cuts
variableslib = library.variables
sampleslib = library.samples
legendlib = library.legendNames

colors = {'dsa': r.kRed+2, 'dmu_dsa': r.kRed, 'dgl': r.kBlue+2, 'dmu_dgl': r.kBlue}

# Input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--eff',           required=False, action='store_true', dest='efficiency')
parser.add_argument('--muon',          required=False, type=str, dest='muon', nargs='*', default=['dmu_dsa'])
parser.add_argument('--var',           required=False, type=str, dest='var', default='dz')
parser.add_argument('--sample',        required=False, type=str, dest='sample', default='Cosmics2022C')
parser.add_argument('--file',          required=False, type=str, dest='filename', default=None)
parser.add_argument('--cuts',          required=False, type=str, dest='cuts', nargs='*', default=['HLT','passTagID'])
parser.add_argument('--maxEntries',    required=False, type=int, dest='maxEntries', default=-1)
parser.add_argument('--outdir',        required=False, type=str, dest='outdir', default='./plots')
args = parser.parse_args()

if __name__=='__main__':
    r.gROOT.ProcessLine('.L ./include/tdrstyle.C')
    r.setTDRStyle()
    r.gROOT.SetBatch(1)

    for muon in args.muon:
        if muon not in ['dsa','dgl','dmu_dsa','dmu_dgl']: 
            print("Error: incorrect muon type. Use one of these: dsa dgl dmu_dsa dmu_dgl")
            sys.exit()
    if args.var not in variableslib: 
            print("Error: unsupported variable.")
            sys.exit()
    if args.sample not in sampleslib: 
            print("Error: unsupported sample.")
            sys.exit()

    mtypes = args.muon
    outdir = args.outdir
    if not os.path.exists(outdir): os.makedirs(outdir)

    # read tChain
    if args.filename:
        tChain = r.TChain("Events")
        tChain.Add(args.filename)
    else:
        _sample = sampleslib[args.sample]
        tChain = _sample.getTChain("Events")

    if args.filename:
        canvasName = "_".join(['var', "file", '-'.join(mtypes), args.var, datetime.now().strftime("%d%m%Y_%H%M%S")])
    else:
        canvasName = "_".join(['var', args.sample, '-'.join(mtypes), args.var, datetime.now().strftime("%d%m%Y_%H%M%S")])
    plot = Plot(canvasName, args.outdir)
    if args.efficiency:
        plot.initLegend()
    else:
        plot.initLegend(x0=.65, y0=.80, x1=.90, y1=.87)

    for mtype in mtypes:
        # read varexp
        var = variableslib[args.var]
        varexp = var.getStr(mtype)

        # buid selection string
        weightParts = []
        selectionParts = []
        if args.cuts:
            for cut in args.cuts:
                _cut = cutslib[cut]
                cutStr = _cut.getStr(mtype)
                if _cut.perEvent: weightParts.append(f'({cutStr})')
                else: selectionParts.append(f'({cutStr})')
            weightStr = "&&".join(weightParts)
            selectionStr = "&&".join(selectionParts)
            selection = f"({weightStr})*({selectionStr})"

        print(f"----------------------------------------------")
        print(f">> Drawing histogram:")
        print(f"    varexp:              {varexp}")
        print(f"    selection:           {selection}")

        if var.vbins is not None: h = r.TH1F(f"h{mtype}", ";"+var.title()+";N events", var.nbins, var.vbins)
        else:                     h = r.TH1F(f"h{mtype}", ";"+var.title()+";N events", var.nbins, var.xmin, var.xmax)
        
        if args.maxEntries==-1:
            tChain.Draw(varexp+f">>h{mtype}", selection, "goff")
        else:
            tChain.Draw(varexp+f">>h{mtype}", selection, "goff", args.maxEntries)
        print(f"    N of entries in hist: {h.GetEntries()}")
        plot.addHist(h, legend=legendlib[mtype], color=colors[mtype])
    
    plot.makeVarPlot(ylog=True)
    plot.save()
