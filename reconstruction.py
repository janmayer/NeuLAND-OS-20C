import os
import sys
import subprocess
import ROOT
from helpers import filename_for


def reconstruction_impl(distance, doubleplane, energy, erel, neutron, physics, overwrite):
    inpfile = filename_for(distance, doubleplane, energy, erel, neutron, physics, ".digi.root")
    simfile = filename_for(distance, doubleplane, energy, erel, neutron, physics, ".simu.root")
    parfile = filename_for(distance, doubleplane, energy, erel, neutron, physics, ".para.root")
#     cutfile = f"output/{physics}/{doubleplane}dp_{energy}AMeV_{neutron}n.ncut.root"
    outfile = filename_for(distance, doubleplane, energy, erel, neutron, physics, ".reco.root")

    if not os.path.isfile(inpfile):
        print(f"Input {inpfile} does not exist")
        return

    if os.path.isfile(outfile):
        if overwrite:
            os.remove(outfile)
        else:
            print(f"Output {outfile} exists and overwriting is disabled")
            return

    ROOT.ROOT.EnableThreadSafety()
    ROOT.FairLogger.GetLogger().SetLogVerbosityLevel("LOW")
    ROOT.FairLogger.GetLogger().SetLogScreenLevel("INFO")

    run = ROOT.FairRunAna()
    ffs = ROOT.FairFileSource(inpfile)
    ffs.AddFriend(simfile)
    run.SetSource(ffs)
    run.SetSink(ROOT.FairRootFileSink(outfile))

    # Connect Runtime Database and Calorimetric Par file
    rtdb = run.GetRuntimeDb()
    pario = ROOT.FairParRootFileIo(False)
    pario.open(parfile)
    rtdb.setFirstInput(pario)
#     pario2 = ROOT.FairParRootFileIo(False)
#     pario2.open(cutfile)
#     rtdb.setSecondInput(pario2)

    # Fixed Multiplicty
    run.AddTask(ROOT.R3BNeulandMultiplicityFixed(neutron, "NeulandMultiplicityFixed"))
    
    # Fixed Multiplicity + RValue Neutron Reco
    run.AddTask(ROOT.R3BNeulandNeutronsRValue(energy, "NeulandMultiplicityFixed", "NeulandClusters", "NeulandNeutronsFixedRValue"))
    run.AddTask(ROOT.R3BNeulandNeutronReconstructionMon("NeulandNeutronsFixedRValue", "NeulandRecoFixedRValue"))

    # Perfect Reco
    run.AddTask(ROOT.R3BNeulandMultiplicityCheat("NeulandPrimaryHits", "NeulandMultiplicityCheat"))
    run.AddTask(ROOT.R3BNeulandNeutronsCheat("NeulandMultiplicityCheat", "NeulandPrimaryHits", "NeulandNeutronsCheat"))
    run.AddTask(ROOT.R3BNeulandNeutronReconstructionMon("NeulandNeutronsCheat", "NeulandRecoCheat"))

    run.Init()
    run.Run(0, 0)
    run.TerminateRun()


# Ugly hack, as FairRun (FairRunSim, FairRunAna) has some undeleteable, not-quite-singleton behavior.
# As a result, the same process can't be reused after the first run.
# Here, create a fully standalone process that is fully destroyed afterwards.
# TODO: Once/If this is fixed, remove this and rename the impl function
def reconstruction(distance, doubleplane, energy, erel, neutron, physics):
    logfile = filename_for(distance, doubleplane, energy, erel, neutron, physics, ".reco.log")
    d = [
        "python",
        "reconstruction.py",
        str(distance),
        str(doubleplane),
        str(energy),
        str(erel),
        str(neutron),
        str(physics),
    ]
    with open(logfile, "w") as log:
        subprocess.run(d, stdout=log, stderr=log)


if __name__ == "__main__":
    distance = int(sys.argv[1])
    doubleplane = int(sys.argv[2])
    energy = int(sys.argv[3])
    erel = int(sys.argv[4])
    neutron = int(sys.argv[5])
    physics = sys.argv[6]
    reconstruction_impl(distance, doubleplane, energy, erel, neutron, physics, overwrite=True)
