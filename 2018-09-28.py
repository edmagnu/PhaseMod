# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 21:49:20 2018

@author: labuser
"""

# 2018-09-28

import os
import numpy as np
from scipy.stats import cauchy
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd


def limit_scan(fname, ax):
    data = pd.read_csv(fname, sep='\t', comment="#", index_col=False)
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='f', inplace=True)
    data.plot(x='f', y='sig', ax=ax)
    return


def limit():
    """Using the HP 214B, see what the DIL is."""
    fig, ax = plt.subplots()
    fname = "1_lim_dye.txt"
    folder = os.path.join("..", "2018-09-28")
    fname = os.path.join(folder, fname)
    limit_scan(fname, ax)
    return


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
    """Using the dye laser at -180 GHz, the MW f is scanned over the
    cavity resonances, finding center, FWHM, and Q values."""
    fig, axes = plt.subplots()
    folder = os.path.join("..", "2018-09-28")
    fname = "2_fscan.txt"
    fname = os.path.join(folder, fname)
    mw_fscan(fname, 1, axes)
    fig.tight_layout()
    return


def mwion_scan():
    """Take ratios of MW on / MW off to get ionization rate at different values
    of the Variable Attenuator"""
    fig, ax = plt.subplots()
    # Data from 2018-09-27, using the SFIP
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
    # data from 2018-09-28
    fname = "3_mwion_blnk.txt"
    folder = os.path.join("..", "2018-09-28")
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#")
    data['r'] = data['s1']/data['s2']
    data['f'] = np.power(10, data['d']/20)  # field equivalent
    data.sort_values(by='f', inplace=True)
    data.plot(x='f', y='r', marker='o', ax=ax, label="-180 GHz")
    return



if __name__ == "__main__":
    # limit()
    # cavity_resonances()
    mwion_scan()
