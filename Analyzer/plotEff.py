import os
import ROOT as r
import numpy as np
import library
import argparse
from datetime import datetime

# Input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--muon',          required=False, type=str, dest='muon', default='dmu_dsa')
parser.add_argument('--var',           required=False, type=str, dest='var', default='dz')
parser.add_argument('--sample',        required=False, type=str, dest='sample', default='Cosmics2022C')
parser.add_argument('--file',          required=False, type=str, dest='filename', default=None)
parser.add_argument('--cuts',          required=False, type=str, dest='cuts', nargs='*', default=['HLT','passTagID'])
parser.add_argument('--maxEntries',    required=False, type=int, dest='maxEntries', default=-1)
parser.add_argument('--outdir',        required=False, type=str, dest='outdir', default='./plots')
args = parser.parse_args()

if __name__=='__main__':
    r.gROOT.LoadMacro('./include/tdrstyle.C')
    r.setTDRStyle()
    r.gROOT.SetBatch(1)

    cutslib = library.cuts
    variableslib = library.variables
    sampleslib = library.samples

    if args.muon not in ['dsa','dgl','dmu_dsa','dmu_dgl']: print("Error: incorrect muon type. Use one of these: dsa dgl dmu_dsa dmu_dgl")
    if args.var not in variableslib: print("Error: unsupported variable.")
    if args.sample not in sampleslib: print("Error: unsupported sample.")

    mtype = args.muon   
    outdir = args.outdir
    if not os.path.exists(outdir): os.makedirs(outdir)

    # read tChain
    if args.filename:
        tChain = r.TChain("Events")
        tChain.Add(args.filename)
    else:
        _sample = sampleslib[args.sample]
        tChain = _sample.getTChain("Events")

    # read varexp
    variable = variableslib[args.var]
    varexp = variable.getStr(mtype)

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
        selectionStr = "&&".join(selectionParts+[f'({mtype}_passTagID)'])
        selection_total = f"({weightStr})*({selectionStr})"
        selectionStr = "&&".join(selectionParts+[f'({mtype}_passTagID)',f'({mtype}_hasProbe)'])
        selection_passed = f"({weightStr})*({selectionStr})"

    print(f"Args to tChain.Draw():")
    print(f"    varexp:           {varexp}")
    print(f"    selection total:  {selection_total}")
    print(f"    selection passed: {selection_passed}")
    print(f"    n of entries:     {tChain.GetEntries()}")

    if variable.vbins is not None:
        h_total  = r.TH1F("h_total",  f"Efficiency cosmic muons;tag {variable.title};Efficiency", variable.nbins, variable.vbins)
        h_passed = r.TH1F("h_passed", f"Efficiency cosmic muons;tag {variable.title};Efficiency", variable.nbins, variable.vbins)
    else:
        h_total  = r.TH1F("h_total",  f"Efficiency cosmic muons;tag {variable.title};Efficiency", variable.nbins, variable.xmin, variable.xmax)
        h_passed = r.TH1F("h_passed", f"Efficiency cosmic muons;tag {variable.title};Efficiency", variable.nbins, variable.xmin, variable.xmax)
    h_total.Sumw2()
    h_passed.Sumw2()
    if args.maxEntries==-1:
        tChain.Draw(varexp+">>h_total", selection_total, "goff")
        tChain.Draw(varexp+">>h_passed", selection_passed, "goff")
    else:
        tChain.Draw(varexp+">>h_total", selection_total, "goff", args.maxEntries)
        tChain.Draw(varexp+">>h_passed", selection_passed, "goff", args.maxEntries)

    print(f"Global efficiency (passed/total) = {h_passed.GetEntries()}/{h_total.GetEntries()} = {h_passed.GetEntries()/h_total.GetEntries()*100}%")
    h_eff = r.TEfficiency(h_passed, h_total)

    if args.filename:
        canvasName = "_".join(['eff', args.sample, mtype, args.var, datetime.now().strftime("%d%m%Y_%H%M%S")])
    else:
        canvasName = "_".join(['eff', "file", mtype, args.var, datetime.now().strftime("%d%m%Y_%H%M%S")])
    c = r.TCanvas(canvasName, canvasName)
    c.SetFillStyle(4000)
    c.cd()
    xaxis = h_eff.GetTotalHistogram().GetXaxis()
    xmin = xaxis.GetBinLowEdge(xaxis.GetFirst())
    xmax = xaxis.GetBinUpEdge(xaxis.GetLast())
    h_eff.Draw("PA");
    c.Update()
    #### Styling eff plot
    h_eff.SetLineWidth(1)
    h_eff.SetLineColor(r.kBlue)
    h_eff.SetMarkerColor(r.kBlue)
    h_eff.SetMarkerStyle(20)
    _g = h_eff.GetPaintedGraph()
    _g.SetMinimum(0)
    _g.SetMaximum(1.2)
    _g.GetXaxis().SetLimits(xmin,xmax)

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.20, 0.93, "#bf{CMS} #it{Internal}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.03);
    if not args.filename:
        latex.DrawLatex(0.88, 0.93, _sample.name)
    else:
        latex.DrawLatex(0.88, 0.93, args.filename)

    c.SaveAs(f"{outdir}/{canvasName}.png")
    c.SaveAs(f"{outdir}/{canvasName}.pdf")
    c.SaveAs(f"{outdir}/{canvasName}.C")
