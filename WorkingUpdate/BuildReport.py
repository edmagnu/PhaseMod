# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 19:44:04 2018

@author: labuser
"""

# Report of progress on phase modulation experiment.

import os
import sys
import matplotlib.pyplot as plt
sys.path.append("..")
import utilities as pmu


def n27_and_sidebands():
    """Plot Rydberg states around n=27 and the MW sidebands.
    Produces 'n27_and_sidebands.pdf'"""
    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=False)
    # n=26 through n=29
    folder = os.path.join("..", "..", "2018-09-06")
    fname = "1_dye_fscan.txt"
    fname = os.path.join(folder, fname)
    data = pmu.fscan_import(fname)
    data.plot(x='fpoly', y='sig', label="MW Off", ax=ax)
    # sidebands
    folder = os.path.join("..", "..", "2018-09-09")
    fname = "1_freq_dye.txt"
    fname = os.path.join(folder, fname)
    data = pmu.fscan_import(fname)
    data['asig'] = data['sig'] - 0.3
    data.plot(x='fpoly', y='asig', label="MW On", ax=ax)
    # pretty figure
    ax.legend().remove()
    ax.set_ylabel(r"$e^-$ Signal")
    ax.set_yticks([])
    ax.set_xlabel("Frequency (GHz from Limit)")
    ax.text(-4400, -0.15, "MW On")
    ax.text(-4400, 0.3, "MW Off")
    # save
    fig.tight_layout()
    fig.savefig("n27_and_sidebands.pdf")
    return

def n27_and_stark():
    
    return


if __name__ == "__main__":
    n27_and_sidebands()
