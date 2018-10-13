# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 11:35:17 2018

@author: labuser
"""

# 2018-09-27

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import cauchy
from scipy.optimize import curve_fit
import pandas as pd


def cauchy_model(x, a, loc, scale, y0):
    return a*cauchy.pdf(x, loc, scale) + y0


def cauchy_fit(x, y):
    p0 = [(max(y) - min(y))*(max(x) - min(x))/10,
          x[np.argmax(y)],
          (max(x) - min(x))/10, min(y)]
    popt, pcov = curve_fit(cauchy_model, x, y, p0)
    print("Center Frequency is : ", popt[1]*1e-6, " MHz")
    print("FWHM is : ", 2*popt[2]*1e-6, " MHz")
    print("Q is : ", popt[1]/(2*popt[2]))
    return popt


def mw_fscan(fname, d, ax, plotting=True):
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False,
                       header=None, names=['f', 's'])
    data.sort_values(by='f', inplace=True)
    data['s'] = data['s']*d
    popt = cauchy_fit(data['f'].values, data['s'].values)
    # print(popt)
    if plotting is True:
        data.plot(x='f', y='s', ax=ax)
        ax.plot(data['f'].values, cauchy_model(data['f'].values, *popt))
        ax.plot(data['f'].values,
                data['s'].values - cauchy_model(data['f'].values, *popt))
    return data


def cavity_resonances():
    """Using the dye laser at n=27 + 1 f_MW, the MW f is scanned over the
    cavity resonances, finding center, FWHM, and Q values."""
    fig, axes = plt.subplots(ncols=3)
    folder = os.path.join("..", "2018-09-27")
    fname = "2_fscan.txt"  # n=27 + 1 f_MW sideband.
    fname = os.path.join(folder, fname)
    mw_fscan(fname, -1, axes[0])
    fname = "1_fscan.txt"  # n=27 + 1 f_MW sideband.
    fname = os.path.join(folder, fname)
    mw_fscan(fname, -1, axes[1])
    fname = "7_fscan.txt"  # MW ionization at n=46
    fname = os.path.join(folder, fname)
    mw_fscan(fname, 1, axes[2])
    fig.tight_layout()
    return


def node_scan():
    """Using the dye laser at n=27 _ 1 f_MW, and moving the 610-nm lense, the
    nodes and anti-nodes of each cavity resonance are scanned."""
    fig, axes = plt.subplots(nrows=2, sharex=True)
    fname = "3_sbnd_blnk.txt"
    folder = os.path.join("..", "2018-09-27")
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=0)
    data['r12'] = data['s1']/data['s2']
    data['r21'] = data['s2']/data['s1']
    data.plot.scatter(x='d', y='s1', c='C0', ax=axes[0])
    data.plot.scatter(x='d', y='s2', c='C1', ax=axes[0])
    data.plot.scatter(x='d', y='r12', c='C2', ax=axes[1])
    data.plot.scatter(x='d', y='r21', c='C3', ax=axes[1])
    return data


def limit_scan(fname, ax):
    data = pd.read_csv(fname, sep='\t', comment="#", index_col=False)
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='f', inplace=True)
    data.plot(x='f', y='sig', ax=ax)
    return


def limit():
    fig, ax = plt.subplots()
    fname = "5_lim_dye.txt"
    folder = os.path.join("..", "2018-09-27")
    fname = os.path.join(folder, fname)
    limit_scan(fname, ax)
    fname = "6_lim_dye.txt"
    fname = os.path.join(folder, fname)
    limit_scan(fname, ax)
    return


def mwion_scan():
    fig, ax = plt.subplots()
    fname = "8_mwion_blnk.txt"
    folder = os.path.join("..", "2018-09-27")
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#")
    data['r'] = data['s1']/data['s2']
    data['f'] = np.power(10, data['d']/20)  # field equivalent
    data.sort_values(by='f', inplace=True)
    data.plot(x='f', y='r', marker='v', ax=ax, label="-1580 GHz")
    fname = "9_mwion_blnk.txt"
    folder = os.path.join("..", "2018-09-27")
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#")
    data['r'] = data['s1']/data['s2']
    data['f'] = np.power(10, data['d']/20)  # field equivalent
    data.sort_values(by='f', inplace=True)
    data.plot(x='f', y='r', marker='^', ax=ax, label="-780 GHz")
    fname = "10_mwion_blnk.txt"
    folder = os.path.join("..", "2018-09-27")
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#")
    data['r'] = data['s1']/data['s2']
    data['f'] = np.power(10, data['d']/20)  # field equivalent
    data.sort_values(by='f', inplace=True)
    data.plot(x='f', y='r', marker='s', ax=ax, label="-380 GHz")
    fname = "11_mwion_blnk.txt"
    folder = os.path.join("..", "2018-09-27")
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#")
    data['r'] = data['s1']/data['s2']
    data['f'] = np.power(10, data['d']/20)  # field equivalent
    data.sort_values(by='f', inplace=True)
    data.plot(x='f', y='r', marker='o', ax=ax, label="-180 GHz")
    return


if __name__ == "__main__":
    # cavity_resonances()
    node_scan()
    # limit()
    # mwion_scan()
