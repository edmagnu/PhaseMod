# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 21:37:07 2018

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


def diode(date):
    """ Load diode scan and plot"""
    instrs = [["4_freq_diode.txt", "0 V/cm", 0],
              ["5_freq_diode.txt", "6.6 V/cm (40 V)", 1]]
    fig, axes = plt.subplots(nrows=len(instrs), sharex=True, sharey=True,
                             figsize=(8,8))
    for instr in instrs:
        [fname, label, ax] = instr
        ax = axes[ax]
        fname = os.path.join("..", date, fname)
        data = tk.diode_scan(fname)
        tk.diode_plot(data, ax, label)
        ax.axhline(0, c='k')
        ax.axvline(-4509.83, c='grey', ls='dashed')
    axes[0].set_title(r"$n=27$, $l\geq d$ Manifold at 0 and 6.6 V/cm")
    fig.tight_layout()
    fig.savefig("Stark_40V-2018-10-10.pdf")
    return


def diode_blink(date):
    fig, axes = plt.subplots(nrows=2, sharex=False, sharey=True, figsize=(8,8))
    instrs = [["6_freq_blink_diode.txt", "-5 dB, Red", axes[0]],
              ["11_freq_blink_diode.txt", "-11 dB, Blue", axes[1]]]
    for instr in instrs:
        [fname, label, ax] = instr
        fname = os.path.join("..", date, fname)
        data = tk.diode_blink_scan(fname)
        tk.diode_blink_plot(data, ax, ax, label)
    return


def delay(date):
    """Load, average and fold data, see what it yeilds."""
    # MW Field
    mwf = 18.5102e9*2
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = 5
    fold = 1
    instrs = [["2_delay.txt", "0 V, -5 dB", 0],
              ["8_delay.txt", "40 V, -5 dB, Red", 1],
              ["9_delay.txt", "40 V, -11 dB, Red", 2],
              ["10_delay.txt", "40 V, -17 dB, Red", 3]]
    fig, axes = plt.subplots(nrows=len(instrs), sharex=True, sharey=False,
                             figsize=(8, 8))
    for instr in instrs:
        [fname, label, i] = instr
        fname = os.path.join("..", date, fname)
        ax = axes[i]
        tk.delay_plot(fname, xkey, ykey, ykey2, mwf, nave, ax, label, fold,
                      False)
        ax.set_xlabel(r"Delay (MW $\lambda$)")
        ax.set_ylabel("Signal (arb. u.)")
    axes[0].set_title("Modulation of Red Stark State at Different MW Power")
    fig.tight_layout()
    fig.savefig("Red_at_diff_MW-2018-10-10.pdf")
    instrs = [["12_delay.txt", "40 V, -11 dB, Blue", 0],
              ["13_delay.txt", "40 V, -11 dB, Middle", 1],
              ["9_delay.txt", "40 V, -11 dB, Red", 2]]
    fig, axes = plt.subplots(nrows=len(instrs), sharex=True, sharey=False,
                             figsize=(8, 8))
    for instr in instrs:
        [fname, label, i] = instr
        fname = os.path.join("..", date, fname)
        ax = axes[i]
        tk.delay_plot(fname, xkey, ykey, ykey2, mwf, nave, ax, label, fold,
                      False)
        ax.set_xlabel(r"Delay (MW $\lambda$)")
        ax.set_ylabel("Signal (arb. u.)")
    axes[0].set_title("Red, Middle, and Blue Stark State Modulation")
    fig.tight_layout()
    fig.savefig("Red_Middle_Blue-2018-10-10.pdf")
    return


def main():
    date = "2018-10-10"
    # cavity_resonances(date)
    diode(date)
    # diode_blink(date)
    delay(date)
    return


if __name__ == "__main__":
    main()
