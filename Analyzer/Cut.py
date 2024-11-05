import os
import ROOT as r

class Cut:

    def __init__(self, string, latex='-', perEvent=False):
        self.string = string
        self.latex = latex
        self.perEvent = perEvent

    def getStr(self, *args):
        return self.string.format(*args)

    def getInverted(self):
        " Returns inverted version of the cut "
        return Cut(f"!({self.string})", latex=f"fails {self.latex}", perEvent=self.perEvent)

    def __add__(self, other):
        if self.perEvent != other.perEvent: 
            print('Error: cannot add a per-event cut and a per-muon cut')
            return
        return Cut(f'({self.getStr()})&&({other.getStr()})', latex=f'{self.latex} and {other.latex}', perEvent=self.perEvent)
