# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 19:44:04 2018

@author: labuser
"""

# Import and plot frequency scans from the dye laser.

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def step_freq_fit(o, i, f):
    p = np.polyfit(i, f, o)
    fpoly = np.polyval(p, i)
    return fpoly


def dye_scan():
    """Display a long frequency scan of the dye laser, showing n=40 -> Cont"""
    fname = os.path.join("..", "2018-08-06", "4_dye_160VDC.txt")
    data = pd.read_csv(fname, sep='\t', comment="#", index_col=False)
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='f', inplace=True)
    fig, ax = plt.subplots()
    ax.axvline(0, c='k')
    ax.axhline(0, c='k')
    e45 = -1623.43
    e50 = -1314.77
    e60 = -912.7
    print(max(data['sig']))
    ntext = ["45", "50", "60"]
    for i, line in enumerate([e45, e50, e60]):
        ax.plot([line]*2, [0, 1.2*max(data['sig'])], '--', c='grey')
        ax.text(line, ax.get_ylim()[1], ntext[i],
                horizontalalignment='center', verticalalignment='top')
    data.plot(x='f', y='sig', ax=ax)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Signal (arb. u.)")
    fig.tight_layout()
    fig.savefig("DyeScan.pdf")
    return


def narrow_red():
    """Display a close-up of n=60 with the diode laser"""
    folder = os.path.join("..", "2018-08-06")
    # 1
    fname = "1_diode_n60.txt"
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['fpoly'] = step_freq_fit(3, data['i'], data['f'])
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='i', inplace=True)
    fig, ax = plt.subplots(nrows=2, sharex=True)
    data.plot(x='fpoly', y='sig', ax=ax[0], label="Broad 670-nm")
    # 3
    fname = "3_diode_n60.txt"
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['fpoly'] = step_freq_fit(3, data['i'], data['f'])
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='i', inplace=True)
    data.plot(x='fpoly', y='sig', ax=ax[1], label="Narrow 670-nm")
    ax[1].set_xlabel("Frequency (GHz)")
    ax[0].set_ylabel("Signal (arb. u.)")
    ax[1].set_ylabel("Signal (arb. u.)")
    ax[1].set_xlim((-918, -908))
    fig.tight_layout()
    fig.savefig("NarrowRed.pdf")
    return


def diode_scan():
    """Display a close-up of n=47 with the diode laser"""
    folder = os.path.join("..", "2018-08-06")
    # 1
    fname = "5_diode_n47.txt"
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['fpoly'] = step_freq_fit(3, data['i'], data['f'])
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='i', inplace=True)
    fig, ax = plt.subplots()
    data.plot(x='fpoly', y='sig', ax=ax, label="n=47")
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Signal (arb. u.)")
    fig.tight_layout()
    fig.savefig("DiodeScan.pdf")
    return


def starks():
    """Display effect of Stark Broadening"""
    folder = os.path.join("..", "2018-08-06")
    fnames = ["5_diode_n47.txt", "7_diode_7V.txt", "6_diode_15V.txt"]
    fig, ax = plt.subplots(nrows=len(fnames), sharex='col')
    for i, name in enumerate(fnames):
        fname = os.path.join(folder, name)
        data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
        data['fpoly'] = step_freq_fit(5, data['i'], data['f'])
        data['sig'] = data['s'] - data['sb']
        data.sort_values(by="i", inplace=True)
        data.plot(x='fpoly', y='sig', ax=ax[i], label=name)
    ax[-1].set_xlabel("Frequency (GHz)")
    ax[-1].set_ylabel("Signal (arb. u.)")
    ax[-1].set_xlim(-1505, -1470)
    fig.tight_layout()
    return

# main
# dye_scan()
# diode_scan()
starks()
