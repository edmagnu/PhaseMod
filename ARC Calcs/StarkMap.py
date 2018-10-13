# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 13:05:26 2018

@author: edmag
"""

# Use ARC to build a Stark Map of Li7, n=27

import sys
import os
import numpy as np
# import ARC library
# rootDir = os.path.join("C:", "Users", "edmag", "Documents", "Work", "ARC")
rootDir = "C:\\Users\\edmag\\Documents\\Work\\" + \
    "ARC-Alkali-Rydberg-Calculator-1.4.5"
sys.path.append(rootDir)
os.chdir(rootDir)
import arc


# main
calc = arc.StarkMap(arc.Lithium7())
# parameters: n, l, j, mj, nmin, nmax, lmax
calc.defineBasis(27, 3, 3.5, 0.5, 25, 30, 30)
calc.diagonalise(np.linspace(0e2, 150e2, 1501))
#                  drivingFromState=[3, 2, 1.5, 0.5, 0])
rootFileName = "Lithium7StarkMap"
rootFileName = os.path.join("..", "PhaseMod", "Arc Calcs", rootFileName)
calc.exportData(rootFileName, exportFormat="csv")
arc.saveCalculation(calc, "MyCalc.pki")
calc.plotLevelDiagram()
calc.showPlot()
