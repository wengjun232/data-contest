# Convert ROOT file to HDF5 file

import numpy as np
import ROOT
import sys, itertools as it
import os, argparse
import tables

windowSize = 1029

# Define the database columns
class WaveformData(tables.IsDescription):
    EventID    = tables.Int64Col(pos=0)
    ChannelID  = tables.Int16Col(pos=1)
    Waveform   = tables.Col.from_type('int16', shape=windowSize, pos=2)

class ParticleTruthData(tables.IsDescription):
    EventID    = tables.Int64Col(pos=0)
    x          = tables.Float32Col(pos=1)
    y          = tables.Float32Col(pos=2)
    z          = tables.Float32Col(pos=3)
    E          = tables.Float32Col(pos=4)
    Alpha       = tables.Int16Col(pos=5)
    px = tables.Float32Col(pos=6)
    py = tables.Float32Col(pos=7)
    pz = tables.Float32Col(pos=8)

ROOT.PyConfig.IgnoreCommandLineOptions = True

psr = argparse.ArgumentParser()                                                                          
psr.add_argument("-o", dest='opt', help="output")
psr.add_argument('--alpha', nargs='+', help="alpha input")
psr.add_argument('--beta', nargs='+', help="beta input")
args = psr.parse_args()

class PETruthData(tables.IsDescription):
    EventID    = tables.Int64Col(pos=0)
    ChannelID  = tables.Int16Col(pos=1)
    PETime     = tables.Int16Col(pos=2)
    PEType     = tables.Int8Col(pos=3)

# Create the output file and the group
h5file = tables.open_file(args.opt, mode="w", title="OneTonDetector",                                    
                           filters = tables.Filters(complevel=9))
group = "/"

# Create tables
ParticleTruthTable = h5file.create_table(group, "ParticleTruth", ParticleTruthData, "Particle information")
triggerinfo = ParticleTruthTable.row

WaveformTable = h5file.create_table(group, "Waveform", WaveformData, "Waveform")
waveform = WaveformTable.row

PETruthTable = h5file.create_table(group, "PETruth", PETruthData, "PE information")
groundtruth = PETruthTable.row

t = ROOT.TChain("Readout")
tTruth = ROOT.TChain("SimTriggerInfo")

for filename in it.chain(args.alpha, args.beta):
    t.Add(filename)
    tTruth.Add(filename)

# Loop for event
nEntries = t.GetEntries()
print(nEntries)

entry_list = np.arange(nEntries, dtype=int)
np.random.shuffle(entry_list)

n = 0
for i in entry_list:
    print(n)
    n += 1
    t.GetEntry(i)
    event = t
    nChannel = event.ChannelId.size()
    wavSize = event.Waveform.size()
    for j in range(nChannel):
        waveform['EventID'] = n
        waveform['ChannelID'] = event.ChannelId[j]
        waveform['Waveform'] = event.Waveform[j*windowSize:(j+1)*windowSize]
        waveform.append()

    tTruth.GetEntry(i)
    event = tTruth
    triggerinfo['EventID'] = n
    triggerinfo['x'] = event.truthList[0].x
    triggerinfo['y'] = event.truthList[0].y
    triggerinfo['z'] = event.truthList[0].z
    triggerinfo['E'] = event.truthList[0].EkMerged

    particle = event.truthList[0].PrimaryParticleList[0]
    triggerinfo['Alpha'] = int(particle.PdgId!=11)
    triggerinfo['px'] = particle.px
    triggerinfo['py'] = particle.py
    triggerinfo['pz'] = particle.pz

    triggerinfo.append()

    for PE in event.PEList:
        groundtruth['EventID'] = n
        groundtruth['ChannelID'] = PE.PMTId
        groundtruth['PETime'] = PE.HitPosInWindow+10   # Add a 10ns offset. The PE time now is more closer to the waveform.
        groundtruth['PEType'] = PE.PEType
        groundtruth.append()

# Flush into the output file
ParticleTruthTable.flush()
WaveformTable.flush()
PETruthTable.flush()
h5file.close()
