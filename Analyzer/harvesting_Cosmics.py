import ROOT as r
import os, json
from math import pi
import numpy as np
from argparse import ArgumentParser
import include.drawUtils as draw
from include.Launcher import Launcher
from include.DTree import DTree

#r.gStyle.SetLabelFont(42)
################################# GLOBAL VARIABLES DEFINITION ####################################

runningfile = os.path.abspath(__file__)
WORKPATH = ''
for level in runningfile.split('/')[:-1]:
    WORKPATH += level
    WORKPATH += '/'
EOSPATH = '/eos/user/r/rlopezru/www/DisplacedMuons_Studies/'
www = '/eos/user/r/rlopezru/www'

# Read dat file
datFile = WORKPATH + 'dat/Samples_Summer23_Cosmics.json'
dat = json.load(open(datFile,'r'))

def makeEfficiencyPlot(hfile, dtree, hname, tag, collection, names, color=r.kBlue+1, texts=[]):
    sample = dtree.short_name
    h_track = hfile.Get(hname+"_"+collection)
    h_muon = hfile.Get(hname+"_dmu_"+collection)
    c = r.TCanvas(hname+'_'+collection, hname+'_'+collection)
    c.cd()
    xaxis = h_track.GetTotalHistogram().GetXaxis()
    xmin = xaxis.GetBinLowEdge(xaxis.GetFirst())
    xmax = xaxis.GetBinUpEdge(xaxis.GetLast())
    h_track.Draw("PA")
    h_muon.Draw("P,SAME")
    c.Update()
    #### Styling track plot
    h_track.SetLineWidth(1)
    h_track.SetLineColor(color[0])
    h_track.SetMarkerColor(color[0])
    h_track.SetMarkerStyle(20)
    _g = h_track.GetPaintedGraph()
    _g.SetMinimum(0)
    _g.SetMaximum(1.2)
    _g.GetXaxis().SetLimits(xmin,xmax)
    #### Styling muon plot
    h_muon.SetLineWidth(1)
    h_muon.SetLineColor(color[1])
    h_muon.SetMarkerColor(color[1])
    h_muon.SetMarkerStyle(20)
    l = r.TLegend(.60,.83,.85,.88)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    l.AddEntry(h_track, names[0], "P")
    l.AddEntry(h_muon, names[1], "P")
    l.SetBorderSize(0)
    l.Draw()
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.15, 0.93, "#bf{CMS} #it{Internal}")
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.03);
    for n,t in enumerate(texts):
        latex.DrawLatex(0.17, 0.86-0.03*n, t)
    c.SaveAs(EOSPATH+'Plots/{0}/{1}/{2}.png'.format(tag,dtree.short_name,c.GetName()))
    c.SaveAs(EOSPATH+'Plots/{0}/{1}/{2}.pdf'.format(tag,dtree.short_name,c.GetName()))
    c.SaveAs(EOSPATH+'Plots/{0}/{1}/{2}.C'.format(tag,dtree.short_name,c.GetName()))


def makeVarPlot(hfile, dtree, hname, tag, collection, names, color=r.kRed, texts=[], ylog=True):
    # Get hists
    sample = dtree.short_name
    h_track = hfile.Get(hname+"_"+collection) # track hist
    h_muon = hfile.Get(hname+"_dmu_"+collection) # muon hist
    maxVal = max([h_track.GetMaximum(), h_muon.GetMaximum()])
    #### Styling track plot
    h_track.SetLineWidth(1)
    if ylog:
        h_track.SetMaximum(100*maxVal)
        h_track.SetMinimum(1)
    else: h_track.SetMaximum(1.2*maxVal)
    h_track.SetLineColor(color[0])
    h_track.SetLineWidth(2)
    h_track.GetXaxis().SetLabelSize(0)
    h_track.GetYaxis().SetLabelSize(0.05)
    h_track.GetYaxis().SetTitleSize(0.05)
    #### Styling muon plot
    h_muon.SetLineWidth(1)
    if ylog: h_muon.SetMaximum(10*maxVal)
    else: h_muon.SetMaximum(1.2*maxVal)
    h_muon.SetLineColor(color[1])
    h_muon.SetLineWidth(2)

    c = r.TCanvas(hname+'_'+collection, hname+'_'+collection)
    c.SetFillStyle(4000)
    c.cd()
    ## Create tha pads
    # PAD1
    pad1 = r.TPad("pad1", "pad1", 0, 0.3, 1, 1.0) # for the plot
    pad1.SetBottomMargin(0.015)
    pad1.SetTopMargin(0.1)
    pad1.Draw()
    # PAD2
    pad2 = r.TPad("pad2", "pad2", 0, 0.01, 1, 0.3) # for the difference
    pad2.SetTopMargin(0.05);
    pad2.SetBottomMargin(0.4);
    pad2.Draw();

    pad1.cd()
    if ylog: pad1.SetLogy(1)
    else: pad1.SetLogy(0)
    h_track.Draw("HIST")
    h_muon.Draw("HIST,SAME")
    pad1.Update()
    pad1.RedrawAxis()
    aux_frame = r.TLine()
    aux_frame.SetLineWidth(2) 
    aux_frame.DrawLine(pad1.GetUxmax(), pad1.GetUymin(), pad1.GetUxmax(), pad1.GetUymax());

    ## Compute difference hist
    h_diff = r.TH1F(h_track)
    h_diff.Add(h_muon, -1)
    pad2.cd()
    # Style h_diff plot
    h_diff.SetLineColor(r.kBlack)
    h_diff.SetLineWidth(2)
    h_diff.GetYaxis().SetTitle("Tracks - Muons");
    h_diff.GetYaxis().CenterTitle();
    h_diff.GetYaxis().SetLabelSize(0.11);
    h_diff.GetYaxis().SetNdivisions(6);
    h_diff.GetYaxis().SetTitleSize(0.11);
    h_diff.GetXaxis().SetLabelSize(0.11);
    h_diff.GetXaxis().SetTitleSize(0.12);
    h_diff.GetXaxis().SetLabelOffset(0.03);
    h_diff.GetXaxis().SetTitleOffset(1.5);
    # Set max and min
    h_diff.SetMaximum(1.1*h_diff.GetMaximum() if h_diff.GetMaximum() >= 1 else 1)
    h_diff.SetMinimum(1.1*h_diff.GetMinimum() if h_diff.GetMinimum() <= -1 else -1)
    h_diff.Draw('HIST')
    xmin = h_diff.GetBinLowEdge(1)
    xmax = h_diff.GetBinLowEdge(h_diff.GetNbinsX()+1)
    line = r.TLine(xmin, 0, xmax, 0)
    line.SetLineColor(r.kGray+2);
    line.SetLineWidth(2);
    line.Draw('');
    pad2.Update()
    pad2.RedrawAxis()
    aux_frame2 = r.TLine()
    aux_frame2.SetLineWidth(2) 
    aux_frame2.DrawLine(pad2.GetUxmax(), pad2.GetUymin(), pad2.GetUxmax(), pad2.GetUymax());

    c.cd()
    l = r.TLegend(.60,.80,.85,.88)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    l.AddEntry(h_track, names[0], "L")
    l.AddEntry(h_muon, names[1], "L")
    l.SetBorderSize(0)
    l.Draw()
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.15, 0.94, "#bf{CMS} #it{Internal}")
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.03);
    for n,t in enumerate(texts):
        latex.DrawLatex(0.17, 0.86-0.03*n, t)
    c.SaveAs(EOSPATH+'Plots/{0}/{1}/{2}.png'.format(tag,dtree.short_name,c.GetName()))
    c.SaveAs(EOSPATH+'Plots/{0}/{1}/{2}.pdf'.format(tag,dtree.short_name,c.GetName()))
    c.SaveAs(EOSPATH+'Plots/{0}/{1}/{2}.C'.format(tag,dtree.short_name,c.GetName()))

def make2DEfficiencyPlot(hfile, dtree, hname, tag, collection, zlog=False):

    h = hfile.Get(hname+'_'+collection)

    c = r.TCanvas(hname+'_'+collection,hname+'_'+collection,ww=700,wh=600)
    c.SetLeftMargin(0.13)
    c.SetRightMargin(0.16)
    c.cd()
    if zlog: c.SetLogy(1)
    else: c.SetLogy(0)
 
    h.SetStatisticOption(r.TEfficiency.kFNormal)
    h.Draw("COLZ,TEXT")
    #h.GetPaintedHistogram().GetZaxis().SetRangeUser(0,1)

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.16, 0.93, "#bf{CMS} #it{Internal}")

    r.gStyle.SetPaintTextFormat("4.2f")

    c.SaveAs(EOSPATH+'Plots/{0}/{1}/{2}.png'.format(tag,dtree.short_name,c.GetName()))
    c.SaveAs(EOSPATH+'Plots/{0}/{1}/{2}.pdf'.format(tag,dtree.short_name,c.GetName()))
    c.SaveAs(EOSPATH+'Plots/{0}/{1}/{2}.C'.format(tag,dtree.short_name,c.GetName()))


if __name__ == '__main__':

    r.gROOT.ProcessLine('.L ./include/tdrstyle.C')
    r.gROOT.SetBatch(1)
    print('WORKPATH: ' + WORKPATH)

    r.gStyle.SetPaintTextFormat("3.2f")
    parser = ArgumentParser()
    parser.add_argument('-t', '--tag',   dest='tag')
    parser.add_argument('-a', '--aod',   dest='aod',      action='store_true')
    parser.add_argument('-f', '--force', dest='force_rm', action='store_true')
    args = parser.parse_args()
    gTag = args.tag   
 
    data = 'MiniAOD'
    if args.aod: data = 'AOD'
    
    r.setTDRStyle()    
    collections = ['dsa','dgl']

    # Trees
    trees_originalFilter = []
    '''trees_originalFilter.append(DTree('Cosmics_2022B_MiniAOD_ReReco',         'Cosmics Run2022B MiniAOD (ReReco)',      dat['Cosmics_2022B']['MiniAOD_ReReco'],              gTag, isData = True))
    trees_originalFilter.append(DTree('Cosmics_2022C_MiniAOD_ReReco',         'Cosmics Run2022C MiniAOD (ReReco)',      dat['Cosmics_2022C']['MiniAOD_ReReco'],              gTag, isData = True))
    trees_originalFilter.append(DTree('Cosmics_2022D_MiniAOD_ReReco',         'Cosmics Run2022D MiniAOD (ReReco)',      dat['Cosmics_2022D']['MiniAOD_ReReco'],              gTag, isData = True))
    trees_originalFilter.append(DTree('Cosmics_2022E_MiniAOD_ReReco',         'Cosmics Run2022E MiniAOD (ReReco)',      dat['Cosmics_2022E']['MiniAOD_ReReco'],              gTag, isData = True))
    trees_originalFilter.append(DTree('Cosmics_2022F_MiniAOD',         'Cosmics Run2022F MiniAOD (PromptReco)',      dat['Cosmics_2022F']['MiniAOD-Ntuples'],              gTag, isData = True))
    trees_originalFilter.append(DTree('Cosmics_2022G_MiniAOD',         'Cosmics Run2022G MiniAOD (PromptReco)',      dat['Cosmics_2022G']['MiniAOD-Ntuples'],              gTag, isData = True))'''
    trees_originalFilter.append(DTree(['Cosmics_2022B_MiniAOD_ReReco', 'Cosmics_2022C_MiniAOD_ReReco', 'Cosmics_2022D_MiniAOD_ReReco', 'Cosmics_2022E_MiniAOD_ReReco'],              
                                       'Cosmics 2022 (ReReco BCDE)', 
                                       [dat['Cosmics_2022B']['MiniAOD_ReReco'],dat['Cosmics_2022C']['MiniAOD_ReReco'], dat['Cosmics_2022D']['MiniAOD_ReReco'], dat['Cosmics_2022E']['MiniAOD_ReReco']],
                                       gTag, 
                                       short_name = 'Cosmics_2022BCDE',
                                       isData = True))
    trees_originalFilter.append(DTree(['Cosmics_2022F_MiniAOD', 'Cosmics_2022G_MiniAOD'],              
                                       'Cosmics 2022 (PromptReco FG)', 
                                       [dat['Cosmics_2022F']['MiniAOD-Ntuples'], dat['Cosmics_2022G']['MiniAOD-Ntuples']],
                                       gTag, 
                                       short_name = 'Cosmics_2022FG',
                                       isData = True))
    
    trees_nsegmentsFilter = []

    if not os.path.exists(EOSPATH+'Plots/'+args.tag):
        os.makedirs(EOSPATH+'Plots/'+args.tag)
        os.system('cp {0}/index.php {0}/DisplacedMuons_Studies/Plots/{1}'.format(www,gTag))

    for dtree in trees_originalFilter + trees_nsegmentsFilter:
        dtree.merge(args.force_rm)

        if not os.path.exists(EOSPATH+'Plots/'+args.tag+'/'+dtree.short_name):
            os.makedirs(EOSPATH+'Plots/'+args.tag+'/'+dtree.short_name)
            os.system('cp {0}/index.php {0}/DisplacedMuons_Studies/Plots/{1}/{2}'.format(www,gTag,dtree.short_name))

        hfile = r.TFile(dtree.targetFile)

        #hists =     ["h_pt", "h_eta", "h_phi", "h_normalizedChi2", "h_dxy", "h_dz"]
        hists =     []
        hists_log = ["h_pt_100", "h_pt_100_probe", "h_normalizedChi2_probe", "h_dxy", "h_dz", "h_dxy_probe", "h_dz_probe", "h_NDThits_probe", "h_NCSChits_probe", "h_eta"]
        hists_eff = ["h_eff_pt", "h_eff_eta", "h_eff_dxy", "h_eff_dz"]
        colors_1 = [[r.kRed+4, r.kRed-4], [r.kBlue+4, r.kBlue]]
        colors = [r.kRed+1, r.kBlue+1]
        
        print('>> Plotting {0}'.format(dtree.short_name))
       
        #####           Elaborate texts that will go in Var and Eff plots          ##### 
        #------------------------------------------------------------------------------#
        texts = []
        texts.append(dtree.label)
        #------------------------------------------------------------------------------#
        
        for n,collection in enumerate(collections):
            for h in hists:
                makeVarPlot(hfile, dtree, h, args.tag, collection, names=['reco::Track({0})'.format(collection),'pat::Muon({0})'.format(collection)], color=colors_1[n], texts=texts, ylog=False) 
            for h in hists_log:
                makeVarPlot(hfile, dtree, h, args.tag, collection, names=['reco::Track({0})'.format(collection),'pat::Muon({0})'.format(collection)], color=colors_1[n], texts=texts, ylog=True)
            for h in hists_eff:
                makeEfficiencyPlot(hfile, dtree, h, args.tag, collection, names=['reco::Track({0})'.format(collection),'pat::Muon({0})'.format(collection)], color=colors_1[n], texts=texts)
        make2DEfficiencyPlot(hfile, dtree, "h_eff_2D", args.tag, collection, zlog=False)
        make2DEfficiencyPlot(hfile, dtree, "h_eff_2D_dmu", args.tag, collection, zlog=False)
        print('>> DONE') 
