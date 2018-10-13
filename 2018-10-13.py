# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 14:37:26 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-10-09


import os
import numpy as np
from scipy.stats import cauchy
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
import toolkit as tk


def cavity_resonances(date):
    """Using the dye laser at -180 GHz, the MW f is scanned over the
    cavity resonances, finding center, FWHM, and Q values."""
    fig, axes = plt.subplots(nrows=1, sharex=True)
    folder = os.path.join("..", date)
    norm = False
    instrs = [["1_fscan.txt", axes]]
    for instr in instrs:
        [fname, ax] = instr
        print("\n", fname)
        fname = os.path.join(folder, fname)
        data, popt = tk.mw_fscan(fname, 1, ax, norm=norm)
    fig.tight_layout()
    return


def mw_sideband_scans(date):
    """Scan the dye laser from n=27 -3 f_MW to +3 f_MW in static and MW field.
    Looking for sideband strength change with applied MW field."""
    fig, axes = plt.subplots(nrows=5, ncols=2, sharex=True, sharey=True,
                             figsize=(8, 10))
    folder = os.path.join("..", date)
    instrs = [["10_freq_dye.txt", "0 V,  NO MW", axes[0, 0]],
              ["11_freq_dye.txt", "50 V, NO MW", axes[0, 1]],
              ["8_freq_dye.txt", "0 V, -26 dB", axes[1, 0]],
              ["9_freq_dye.txt", "50 V, -26 dB", axes[1, 1]],
              ["2_freq_dye.txt", "0 V, -20 dB", axes[2, 0]],
              ["3_freq_dye.txt", "50 V, -20 dB", axes[2, 1]],
              ["4_freq_dye.txt", "0 V, -14 dB", axes[3, 0]],
              ["5_freq_dye.txt", "50 V, -14 dB", axes[3, 1]],
              ["6_freq_dye.txt", "0 V, -8 dB", axes[4, 0]],
              ["7_freq_dye.txt", "50 V, -8 dB", axes[4, 1]]]
    axes[0, 0].set_xlim(-4640, 4380)
    for instr in instrs:
        [fname, label, ax] = instr
        fname = os.path.join(folder, fname)
        data = tk.dye_scan(fname)
        tk.dye_plot(data, label, ax)
    fig.tight_layout()
    return


def main():
    date = "2018-10-13"
    # cavity_resonances(date)
    mw_sideband_scans(date)
    # diode(date)
    # diode_blink(date)
    # delay(date)
    return


if __name__ == "__main__":
    main()
