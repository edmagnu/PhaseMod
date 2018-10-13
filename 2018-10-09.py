# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 18:27:26 2018

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
    instrs = [["1_fscan.txt", axes]]
    for instr in instrs:
        [fname, ax] = instr
        print("\n", fname)
        fname = os.path.join(folder, fname)
        data, popt = tk.mw_fscan(fname, -1, ax)
    fig.tight_layout()
    return


def delay(date):
    """Load, average and fold data, see what it yeilds."""
    # MW Field
    fig, axes = plt.subplots(nrows=6, sharex=True, sharey=False,
                             figsize=(8, 10))
    instrs = [["5_delay.txt", "-0.1 dB", axes[0]],
              ["4_delay.txt", "-1 dB", axes[1]],
              ["6_delay.txt", "-2 dB", axes[2]],
              ["2_delay.txt", "-5 dB", axes[3]],
              ["6_delay.txt", "-7 dB", axes[4]],
              ["3_delay.txt", "-10 dB", axes[5]]]
    for instr in instrs:
        [fname, label, ax] = instr
        fname = os.path.join("..", date, fname)
        data = tk.delay_load(fname)
        mwf = 18511.9e6*2
        nave = 5
        fold = 1
        data = tk.transform_delay(data, mwf, nave, fold)
        ykey = 'nsig_rm'
        mask = np.logical_not(np.isnan(data[ykey]))
        mask = mask & np.logical_not(np.isinf(data[ykey]))
        data[mask].plot(x='wlen_fold', y=ykey, label=label, ax=ax)
    axes[-1].set_xlabel("Delay (MW Wavelength)")
    axes[0].set_title("PM = 1.4 (Equal 0 and +/- 1)")
    fig.tight_layout()
    fig.savefig("MW in zero field 2018-10-09.pdf")
    # Modulation
    fig, axes = plt.subplots(nrows=5, sharex=True, sharey=False,
                             figsize=(8, 10))
    instrs = [["11_delay.txt", "-28 dB", axes[0]],
              ["9_delay.txt", "-31 dB", axes[1]],
              ["4_delay.txt", "-35 dB", axes[2]],
              ["8_delay.txt", "-38 dB", axes[3]],
              ["10_delay.txt", "-41.5 dB", axes[4]]]
    for instr in instrs:
        [fname, label, ax] = instr
        fname = os.path.join("..", date, fname)
        data = tk.delay_load(fname)
        mwf = 18511.9e6*2
        nave = 5
        fold = 1
        data = tk.transform_delay(data, mwf, nave, 'wlen_fold')
        ykey = 'nsig_rm'
        mask = np.logical_not(np.isnan(data[ykey]))
        mask = mask & np.logical_not(np.isinf(data[ykey]))
        data[mask].plot(x='wlen_fold', y=ykey, label=label, ax=ax)
    axes[-1].set_xlabel("Delay (MW Wavelength)")
    axes[0].set_title("Attn = -1 dB")
    fig.tight_layout()
    fig.savefig("PM in zero field 2018-10-09.pdf")
    return


def main():
    date = "2018-10-09"
    # cavity_resonances(date)
    delay(date)
    plt.show()
    return


if __name__ == "__main__":
    main()
