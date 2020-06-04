import os
import sys
import subprocess
import ROOT
from helpers import filename_for


def digitization_impl(distance, doubleplane, energy, erel, neutron, physics, overwrite):
    inpfile = filename_for(distance, doubleplane, energy, erel, neutron, physics, ".simu.root")
    parfile = filename_for(distance, doubleplane, energy, erel, neutron, physics, ".para.root")
    outfile = filename_for(distance, doubleplane, energy, erel, neutron, physics, ".digi.root")

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
    ROOT.FairLogger.GetLogger().SetLogScreenLevel("WARNING")

    run = ROOT.FairRunAna()
    run.SetSource(ROOT.FairFileSource(inpfile))
    run.SetSink(ROOT.FairRootFileSink(outfile))

    # Connect Runtime Database
    rtdb = run.GetRuntimeDb()
    pario = ROOT.FairParRootFileIo(False)
    pario.open(parfile)
    rtdb.setFirstInput(pario)

    # Digitize data to hit level and create respective histograms
    run.AddTask(ROOT.R3BNeulandDigitizer())

    # Build clusters and create respective histograms
    run.AddTask(ROOT.R3BNeulandClusterFinder())

    # Find the actual primary interaction points and their clusters
    run.AddTask(ROOT.R3BNeulandPrimaryInteractionFinder())
    run.AddTask(ROOT.R3BNeulandPrimaryClusterFinder())

    run.Init()
    run.Run(0, 0)


# Ugly hack, as FairRun (FairRunSim, FairRunAna) has some undeleteable, not-quite-singleton behavior.
# As a result, the same process can't be reused after the first run.
# Here, create a fully standalone process that is fully destroyed afterwards.
# TODO: Once/If this is fixed, remove this and rename the impl function
def digitization(distance, doubleplane, energy, erel, neutron, physics):
    logfile = filename_for(distance, doubleplane, energy, erel, neutron, physics, ".digi.log")
    d = [
        "python",
        "digitization.py",
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
    digitization_impl(distance, doubleplane, energy, erel, neutron, physics, overwrite=True)
