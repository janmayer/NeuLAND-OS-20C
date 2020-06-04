import pathlib
import os
import ROOT


def filename_for(distance, doubleplane, energy, erel, neutron, physics, what):
    basepath = "output/%s/" % physics.lower()
    pathlib.Path(basepath).mkdir(parents=True, exist_ok=True)
    basename = "%dm_%ddp_%dAMeV_%dkeV_%dn" % (distance, doubleplane, energy, erel, neutron)
    return basepath + basename + what

def processed_events(distance, doubleplane, energy, erel, neutron, physics, what):
    filename = filename_for(distance, doubleplane, energy, erel, neutron, physics, what)
    if os.path.isfile(filename):
        try:
            ROOT.ROOT.EnableThreadSafety()
            tfile = ROOT.TFile.Open(filename)
            ttree = tfile.Get("evt")
            num_events = int(ttree.GetEntries())
            return (filename, num_events)
        except:
            pass
    return (filename, 0)
