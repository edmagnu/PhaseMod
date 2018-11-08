# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 13:25:09 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-11-06

import os
from scipy.special import jv
import matplotlib.pyplot as plt
import pandas as pd
import toolkit as tk


def delay_qs_plot(fname, mwf, ax, label=""):
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    m = 2.539e-7  # delay stage calibration, m/step
    n = 1.00029  # index of refraction in air
    c = 299792458.0  # Speed of Light, meters/second
    nave = 30
    fold = 1
    # transform
    data['sig'] = data['s'] - data['sb']
    data['nrm'] = -(data['n'] - data['nb'])  # !!! Not an Error, n, nb flipped
    data['nsig'] = data['sig'] / data['nrm']
    data['dist'] = data['d']*m*2
    data['wlen'] = data['dist']*mwf*n/c
    data['time'] = data['dist']/c
    data.sort_values(by='dist', inplace=True)
    data['nsig_rm'] = data['nsig'].rolling(window=nave, center=True).mean()
    data['wlen_fold'] = data['wlen']%fold
    data.sort_values(by='wlen_fold', inplace=True)
    data['nsig_fold'] = data['nsig'].rolling(window=nave, center=True).mean()
    data.sort_values(by='wlen', inplace=True)
    data.plot(x='wlen', y='nsig_fold', ax=ax, label=label)
    return data


def res0_PM_nostatic(date):
    dlist = delay_listing(date)
    files = [9, 10, 11, 12, 13, 14, 15]
    mlist = dlist.iloc[files].copy()
    mwf = 18513.2e6*2
    print()
    print(mlist)
    mlist.sort_values(by='pm', inplace=True)
    fig, axes = plt.subplots(nrows=len(mlist['pm']), sharex=True,
                             figsize=(6, 9))
    print(mlist.index.values)
    for i, index in enumerate(mlist.index.values):
        obs = mlist.loc[[index]]
        label = "PM Coeff = {0}".format(obs['pm'].values[0])
        # print(label)
        fname = str(int(obs['number'].values[0])) + "_delay.txt"
        fname = os.path.join("..", date, fname)
        # print(fname)
        delay_qs_plot(fname, mwf, axes[i], label)
    axes[0].set_title("-10 GHz, 0th Resonance, 15 V/cm MW, No Static")
    axes[-1].set_xlabel(r"Delay ($T_{MW}$)")
    axes[-1].set_ylabel("N. Signal")
    fig.tight_layout()
    fig.savefig("2018-11-06-res0PMNoStat.pdf")
    return


def resp1_PM_nostatic(date):
    dlist = delay_listing(date)
    files = [16, 17, 18, 19, 20, 21, 22]
    mlist = dlist.iloc[files].copy()
    mwf = 18513.2e6*2
    print()
    print(mlist)
    mlist.sort_values(by='pm', inplace=True)
    fig, axes = plt.subplots(nrows=len(mlist['pm']), sharex=True,
                             figsize=(6,9))
    print(mlist.index.values)
    for i, index in enumerate(mlist.index.values):
        obs = mlist.loc[[index]]
        label = "PM Coeff = {0}".format(obs['pm'].values[0])
        # print(label)
        fname = str(int(obs['number'].values[0])) + "_delay.txt"
        fname = os.path.join("..", date, fname)
        # print(fname)
        delay_qs_plot(fname, mwf, axes[i], label)
    axes[0].set_title("+39 GHz, +1st Resonance, 15 V/cm MW, No Static")
    axes[-1].set_xlabel(r"Delay ($T_{MW}$)")
    axes[-1].set_ylabel("N. Signal")
    fig.tight_layout()
    fig.savefig("2018-11-06-resp1PMNoStat.pdf")
    return


def resm1_PM_nostatic(date):
    dlist = delay_listing(date)
    files = [23, 24, 25, 26, 27, 28, 29]
    mlist = dlist.iloc[files].copy()
    mwf = 18512.5e6*2
    print()
    print(mlist)
    mlist.sort_values(by='pm', inplace=True)
    fig, axes = plt.subplots(nrows=len(mlist['pm']), sharex=True,
                             figsize=(6,9))
    print(mlist.index.values)
    for i, index in enumerate(mlist.index.values):
        obs = mlist.loc[[index]]
        label = "PM Coeff = {0}".format(obs['pm'].values[0])
        # print(label)
        fname = str(int(obs['number'].values[0])) + "_delay.txt"
        fname = os.path.join("..", date, fname)
        # print(fname)
        delay_qs_plot(fname, mwf, axes[i], label)
    axes[0].set_title("-50 GHz, -1st Resonance, 15 V/cm MW, No Static")
    axes[-1].set_xlabel(r"Delay ($T_{MW}$)")
    axes[-1].set_ylabel("N. Signal")
    fig.tight_layout()
    fig.savefig("2018-11-06-resm1PMNoStat.pdf")
    return


def res0_PM_scanstatic(date):
    dlist = delay_listing(date)
    files = [30, 31, 32, 33, 34, 35, 37, 39]
    # files = [30, 34, 39, 32, 40, 41]
    mlist = dlist.iloc[files].copy()
    mwf = 18511.7e6*2
    print()
    print(mlist)
    mlist.sort_values(by='static', inplace=True)
    fig, axes = plt.subplots(nrows=len(mlist['pm']), sharex=True,
                             figsize=(6,9))
    print(mlist.index.values)
    for i, index in enumerate(mlist.index.values):
        obs = mlist.loc[[index]]
        label = "Static = {0} mV".format(obs['static'].values[0])
        # print(label)
        fname = str(int(obs['number'].values[0])) + "_delay.txt"
        fname = os.path.join("..", date, fname)
        # print(fname)
        delay_qs_plot(fname, mwf, axes[i], label)
    axes[0].set_title("-10 GHz, 0th Resonance, 15 V/cm MW, PM Coeff = 1.4")
    axes[-1].set_xlabel(r"Delay ($T_{MW}$)")
    axes[-1].set_ylabel("N. Signal")
    fig.tight_layout()
    fig.savefig("2018-11-06-res0PMScanStat.pdf")
    return


def res0_PM_scanstatic_close(date):
    dlist = delay_listing(date)
    # files = [30, 31, 32, 33, 34, 35, 37, 39]
    files = [30, 34, 39, 32, 40, 41]
    mlist = dlist.iloc[files].copy()
    mwf = 18511.2e6*2
    print()
    print(mlist)
    mlist.sort_values(by='static', inplace=True)
    fig, axes = plt.subplots(nrows=len(mlist['pm']), sharex=True,
                             figsize=(6,9))
    print(mlist.index.values)
    for i, index in enumerate(mlist.index.values):
        obs = mlist.loc[[index]]
        label = "Static = {0} mV".format(obs['static'].values[0])
        # print(label)
        fname = str(int(obs['number'].values[0])) + "_delay.txt"
        fname = os.path.join("..", date, fname)
        # print(fname)
        delay_qs_plot(fname, mwf, axes[i], label)
    axes[0].set_title("-10 GHz, 0th Resonance, 15 V/cm MW, PM Coeff = 1.4")
    axes[-1].set_xlabel(r"Delay ($T_{MW}$)")
    axes[-1].set_ylabel("N. Signal")
    fig.tight_layout()
    fig.savefig("2018-11-06-res0PMScanStatClose.pdf")
    return


def res0_PM_160mV(date):
    dlist = delay_listing(date)
    files = [42, 43, 44, 45, 46, 47, 48]
    mlist = dlist.iloc[files].copy()
    mwf = 18511.2e6*2
    print()
    print(mlist)
    mlist.sort_values(by='pm', inplace=True)
    fig, axes = plt.subplots(nrows=len(mlist['pm']), sharex=True,
                             figsize=(6,9))
    print(mlist.index.values)
    for i, index in enumerate(mlist.index.values):
        obs = mlist.loc[[index]]
        label = "PM = {0} mV".format(obs['pm'].values[0])
        # print(label)
        fname = str(int(obs['number'].values[0])) + "_delay.txt"
        fname = os.path.join("..", date, fname)
        # print(fname)
        delay_qs_plot(fname, mwf, axes[i], label)
    axes[0].set_title("-10 GHz, 0th Resonance, 15 V/cm MW, Static = 80 mV")
    axes[-1].set_xlabel(r"Delay ($T_{MW}$)")
    axes[-1].set_ylabel("N. Signal")
    fig.tight_layout()
    fig.savefig("2018-11-06-res0PM80mV.pdf")
    return


def res0_PM_80mV(date):
    dlist = delay_listing(date)
    files = [43, 52, 53, 54, 55, 56]
    mlist = dlist.iloc[files].copy()
    mwf = 18511.2e6*2
    print()
    print(mlist)
    mlist.sort_values(by='pm', inplace=True)
    fig, axes = plt.subplots(nrows=len(mlist['pm']), sharex=True,
                             figsize=(6,9))
    print(mlist.index.values)
    for i, index in enumerate(mlist.index.values):
        obs = mlist.loc[[index]]
        label = "PM = {0}".format(obs['pm'].values[0])
        # print(label)
        fname = str(int(obs['number'].values[0])) + "_delay.txt"
        fname = os.path.join("..", date, fname)
        # print(fname)
        delay_qs_plot(fname, mwf, axes[i], label)
    axes[0].set_title("-10 GHz, 0th Resonance, 15 V/cm MW, Static = 80 mV")
    axes[-1].set_xlabel(r"Delay ($T_{MW}$)")
    axes[-1].set_ylabel("N. Signal")
    fig.tight_layout()
    fig.savefig("2018-11-06-res0PM80mV.pdf")
    return


def resp1_PM_80mV(date):
    dlist = delay_listing(date)
    files = [38, 49, 50, 51, 57, 58]
    mlist = dlist.iloc[files].copy()
    mwf = 18511.2e6*2
    print()
    print(mlist)
    mlist.sort_values(by='pm', inplace=True)
    fig, axes = plt.subplots(nrows=len(mlist['pm']), sharex=True,
                             figsize=(6,9))
    print(mlist.index.values)
    for i, index in enumerate(mlist.index.values):
        obs = mlist.loc[[index]]
        label = "PM = {0}".format(obs['pm'].values[0])
        # print(label)
        fname = str(int(obs['number'].values[0])) + "_delay.txt"
        fname = os.path.join("..", date, fname)
        # print(fname)
        delay_qs_plot(fname, mwf, axes[i], label)
    axes[0].set_title("-10 GHz, 0th Resonance, 15 V/cm MW, Static = 80 mV")
    axes[-1].set_xlabel(r"Delay ($T_{MW}$)")
    axes[-1].set_ylabel("N. Signal")
    fig.tight_layout()
    fig.savefig("2018-11-06-resp1PM80mV.pdf")
    return



def delay_listing(date):
    fname = os.path.join("..", date, "delay_list.txt")
    dlist = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    print(dlist)
    return dlist


def scratch(date):
    mwf = 18511.7e6*2
    steps = tk.wlen_to_step(1, mwf)
    print(steps)
    print(100e3-1.5*steps, 100e3+1.5*steps)
    coeff = 1.0
    print("j_0({0})^2 = ".format(coeff), jv(0, coeff)**2)
    return


def main():
    date = "2018-11-05"  # !!! NOT A TYPO
    # lims(date)
    # cavity_resonances(date)
    # mwres(date)
    # scratch(date)
    # delay_qs_zfsbnds(date)
    # delay_qs_0resfig(date)
    # delay_listing(date)
    # res0_PM_nostatic(date)
    # resp1_PM_nostatic(date)
    # resm1_PM_nostatic(date)
    # res0_PM_scanstatic(date)
    # res0_PM_scanstatic_close(date)
    res0_PM_80mV(date)
    # resp1_PM_80mV(date)
    return


if __name__ == "__main__":
    main()
