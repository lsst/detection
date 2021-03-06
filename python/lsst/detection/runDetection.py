#!/usr/bin/env python
import os
import sys
import optparse

import lsst.daf.data as dafData
import lsst.pex.policy
import lsst.pex.logging
import lsst.afw.image as afwImage
import lsst.afw.detection as afwDet
import lsst.detection as det
import Detection

defInDir = os.environ.get("FWDATA_DIR", "")
moduleDir = os.path.split(__file__)[0]
appDir = os.path.normpath(os.path.join("../../../",moduleDir))

#defDiaPath = os.path.join(defInDir, "871034p_1_MI")
defDiaPath = "/home/tsa/DC2OutputData/704893p_01_diff"
defPolicyPath = "/home/tsa/DMS/detection/trunk/pipeline/examples/DetectionPipeline/policy/DetectionStagePolicy.paf"
defVerbosity = 5 # change to 0 once this all works to hide all messages

usage = """usage: %%prog [options] [diaImage [policyFile]]]
Note:
- image arguments are paths to MaskedImage fits files
- image arguments must NOT include the final _img.fits
- default diaMaskedImage = %s
- default policy = %s
""" % (defDiaPath, defPolicyPath)

parser = optparse.OptionParser(usage)
parser.add_option("-v", "--verbosity",
                  type=int, default=defVerbosity,
                  help="verbosity of diagnostic trace messages; 9 for just warnings, less for less information")
parser.add_option("-d", "--debugIO",
                  action="store_true", default=False,
                  help="write diagnostic intermediate files")
(options, args) = parser.parse_args()

def getArg(ind, defValue):
    if ind < len(args):
        return args[ind]
    return defValue

diaPath = getArg(0, defDiaPath)
policyPath = getArg(1, defPolicyPath)

diaExposure = afwImage.ExposureF()
diaExposure.readFits(diaPath)
diaMaskedImage = diaExposure.getMaskedImage()
diaWCS = diaExposure.getWcs()

policy = lsst.pex.policy.Policy.createPolicy(policyPath)
if options.debugIO:
    policy.set("debugIO", True)

if options.verbosity > 0:
    print "Verbosity =", options.verbosity
    lsst.pex.logging.Trace_setVerbosity("lsst.detection", 9)

diaSources = Detection.detection(diaExposure, policy, 0)

for i in range(len(diaSources)):
    diaSource_i = diaSources[i]
    print diaSource_i.getColc(), " ", diaSource_i.getRowc(), " -> ", diaSource_i.getRa(), " ", diaSource_i.getDec()
