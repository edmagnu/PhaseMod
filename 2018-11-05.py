# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 19:36:55 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-11-05

import os
from scipy.special import jv
import matplotlib.pyplot as plt
import pandas as pd
import toolkit as tk


def lims(date):
    """Dye scan shows full extent of the IP from the HP242B, including the
    DIL"""
    fname = "1_freq_dye.txt"
    fname = os.path.join("..", date, fname)
    lo_win = [-550, -450]
    hi_win = [-100, -50]
    fig, ax = plt.subplots()
    tk.dye_qs_lim(fname, lo_win, hi_win, ax, 10)
    return


def cavity_resonances(date):
    """Use a cauchy fit to get the MW Resonance from an atom signal. In this
    case, with the dye laser at 100 GHz, looking at MW Ionization"""
    folder = os.path.join("..", date)
    norm = False
    fname = "52_fscan.txt"
    d = -1
    norm = False
    fig, ax = plt.subplots()
    fname = os.path.join(folder, fname)
    data, popt = tk.mw_fscan(fname, d, ax, norm=norm)
    fig.tight_layout()
    return


def mwres(date):
    """Can clearly see 0 and +/-1 resonances, and a long tail above the
    limit."""
    fname = "3_mwres.txt"
    fname = os.path.join("..", date, fname)
    fig, ax = plt.subplots()
    marker = -15
    label = ""
    mwf = 18.5119*2  # GHz
    tk.mw_res(fname, marker, label, mwf, ax)
    return


def delay_qs_plot(fname, mwf, ax, label=""):
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    m = 2.539e-7  # delay stage calibration, m/step
    n = 1.00029  # index of refraction in air
    c = 299792458.0  # Speed of Light, meters/second
    nave = 30
    fold = 1
    # transform
    data['sig'] = data['s'] - data['b']
    data['nsig'] = data['sig']
    data['dist'] = data['d']*m*2
    data['wlen'] = data['dist']*mwf*n/c
    data['time'] = data['dist']/c
    data.sort_values(by='dist', inplace=True)
    data['nsig_rm'] = data['nsig'].rolling(window=nave, center=True).mean()
    data['wlen_fold'] = data['wlen']%fold
    data.sort_values(by='wlen_fold', inplace=True)
    data['nsig_fold'] = data['nsig'].rolling(window=nave, center=True).mean()
    data.plot(x='wlen_fold', y='nsig_fold', ax=ax, label=label)
    return data


def delay_qs_zfsbnds(date):
    mwf = 18511.0e6*2
    instrs = [
              ["5_delay.txt", "-15 GHz, Resonant", 2],
              ["6_delay.txt", "+33 GHz, Resonant", 0],
              ["13_delay.txt", "+3 GHz, Off-Resonant", 1],
              ["14_delay.txt", "-37 GHz, Off-Resonant", 3],
              ["7_delay.txt", "-49 GHz, Resonant", 4]
             ]
    fig, ax = plt.subplots(nrows=len(instrs), sharex=True, sharey=False,
                           figsize=(6, 8))
    for instr in instrs:
        [fname, label, ia] = instr
        fname = os.path.join("..", date, fname)
        delay_qs_plot(fname, mwf, ax[ia], label)
    ax[-1].set_xlabel(r"Delay ($T_{MW}$)")
    ax[0].set_title("PM Index = 1.4, MW Field = 15 V/cm, 0 V/cm Static.")
    fig.tight_layout()
    fig.savefig("2018-11-05-inversion.pdf")
    return


def delay_qs_0resfig(date):
    mwf = 18511.0e6*2
    instrs = [
              ["5_delay.txt", "PM = 1.4, St = 0 mV", 1, 0],
              ["8_delay.txt", "PM = 1.4, St = 40 mV", 1, 1],
              ["9_delay.txt", "PM = 1.0, St = 40 mV", 0, 1],
              ["10_delay.txt", "PM = 1.0, St = 0 mV", 0, 0],
              ["11_delay.txt", "PM = 2.4, St = 0 mV", 2, 0],
              ["12_delay.txt", "PM = 2.4, St = 40 mV", 2, 1]
             ]
    fig, ax = plt.subplots(nrows=3, ncols=2, sharex=True, sharey=True,
                           figsize=(6, 6))
    for instr in instrs:
        [fname, label, ia, ja] = instr
        fname = os.path.join("..", date, fname)
        delay_qs_plot(fname, mwf, ax[ia, ja], label)
    ax[-1, 0].set_xlabel(r"Delay ($T_{MW}$)")
    ax[-1, 1].set_xlabel(r"Delay ($T_{MW}$)")
    fig.tight_layout()
    return


def scratch(date):
    mwf = 18511.0e6*2
    steps = tk.wlen_to_step(1, mwf)
    print(steps)
    print(100e3-2*steps, 100e3+2*steps)
    coeff = 1.0
    print("j_0({0})^2 = ".format(coeff), jv(0, coeff)**2)
    return


def main():
    date = "2018-11-05"
    # lims(date)
    cavity_resonances(date)
    # mwres(date)
    # scratch(date)
    # delay_qs_zfsbnds(date)
    # delay_qs_0resfig(date)
    return


if __name__ == "__main__":
    main()
