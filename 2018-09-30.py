# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 17:06:17 2018

@author: labuser
"""

# 2018-09-29

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
    # fname = "1_lim_dye.txt"
    fname = "4_lim_dye.txt"
    folder = os.path.join("..", "2018-09-30")
    fname = os.path.join(folder, fname)
    limit_scan(fname, ax)
    return


def cauchy_model(x, a, loc, scale, y0):
    return a*cauchy.pdf(x, loc, scale) + y0


def cauchy_fit(x, y, d):
    if d is -1:
        a0 = -(max(y) - min(y))*(max(x) - min(x))/10
        loc0 = x[np.argmin(y)]
        scale0 = (max(x) - min(x))/10
        y00 = max(y)
    elif d is 1:
        a0 = (max(y) - min(y))*(max(x) - min(x))/10
        loc0 = x[np.argmax(y)]
        scale0 = (max(x) - min(x))/10
        y00 = min(y)
    else:
        a0 = 1
        loc0 = np.mean(x)
        scale0 = (max(x) - min(x))/10
        y00 = 1
    p0 = [a0, loc0, scale0, y00]
    print(p0)
    popt, pcov = curve_fit(cauchy_model, x, y, p0)
    print("Center Frequency is : ", popt[1]*1e-6, " MHz")
    print("FWHM is : ", 2*popt[2]*1e-6, " MHz")
    print("Q is : ", popt[1]/(2*popt[2]))
    return popt


def mw_fscan(fname, d, ax, plotting=True):
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False,
                       header=None, names=['f', 'b', 's', 'r'])
    data.sort_values(by='f', inplace=True)
    data['sig'] = data['s'] - data['b']
    data['ref'] = data['r'] - data['b']
    data['nrm'] = data['sig'] / data['ref']  # norm by signal / reference
    data['nrm'] = data['nrm']
    popt = cauchy_fit(data['f'].values, data['nrm'].values, d)
    # print(popt)
    if plotting is True:
        data.plot(x='f', y='nrm', ax=ax)
        ax.plot(data['f'].values, cauchy_model(data['f'].values, *popt))
        ax.plot(data['f'].values,
                data['nrm'].values - cauchy_model(data['f'].values, *popt))
        ax.axhline(0.9, c='k')
        ax.axhline(0.5, c='k')
    return data, popt


def cavity_resonances():
    """Using the dye laser at -180 GHz, the MW f is scanned over the
    cavity resonances, finding center, FWHM, and Q values."""
    fig, axes = plt.subplots()
    folder = os.path.join("..", "2018-09-30")
    fname = "5_fscan.txt"
    fname = os.path.join(folder, fname)
    data, popt = mw_fscan(fname, -1, axes)
    fig.tight_layout()
    return


def db_feq(a):
    """Get a number proportional to field from an attenuation value"""
    return np.power(10, a/20)


def feq_db(f):
    return 20*np.log10(f)


def mwion_scan():
    """Take ratios of MW on / MW off to get ionization rate at different values
    of the Variable Attenuator"""
    fig, ax = plt.subplots()
    # Data from 2018-09-27, using the SFIP
    fname = "6_mwion_blnk.txt"  # -180 GHz
    folder = os.path.join("..", "2018-09-30")
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#")
    data['r'] = data['s1']/data['s2']
    data['f'] = db_feq(data['d'].values)
    data.sort_values(by='f', inplace=True)
    data.plot(x='f', y='r', marker='v', ax=ax, label="-180 GHz")
    return


def svf_from_cav_res():
    """Using a scan of the cavity resonance, produce Survival vs. Field"""
    fig, axes = plt.subplots(nrows=2, sharex=False)
    fname = "5_fscan.txt"
    attn = -16  # Var Attn value
    fmax = db_feq(attn)
    folder = os.path.join("..", "2018-09-30")
    fname = os.path.join(folder, fname)
    data, popt = mw_fscan(fname, -1, axes[0])
    fwhm = popt[2]*2
    loc = popt[1]
    field = fmax*cauchy.pdf((data['f'].values-loc)/fwhm*2)/cauchy.pdf(0)
    survival_fit = cauchy_model(data['f'].values, *popt)/popt[3]
    survival_data = data['nrm']/popt[3]
    axes[1].plot(field, survival_data, '.', label="data")
    axes[1].plot(field, survival_fit, '-', lw=3, label="Fit")
    axes[1].plot(field, survival_data-survival_fit, '.', label="error")
    axes[1].axvline(0, c='k')
    for val in [1, 0.9, 0.5, 0]:
        axes[1].axhline(val, c='k')
    axes[1].legend()
    fig.tight_layout()
    return


def node_scan():
    """Using the dye laser at n=27 _ 1 f_MW, and moving the 610-nm lense, the
    nodes and anti-nodes of each cavity resonance are scanned."""
    fig, axes = plt.subplots(nrows=2, sharex=True)
    fname = "3_sbnd_blnk.txt"
    folder = os.path.join("..", "2018-09-30")
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=0)
    data['r12'] = data['s1']/data['s2']
    data['r21'] = data['s2']/data['s1']
    data.plot.scatter(x='d', y='s1', c='C0', ax=axes[0])
    data.plot.scatter(x='d', y='s2', c='C1', ax=axes[0])
    data.plot.scatter(x='d', y='r12', c='C2', ax=axes[1])
    data.plot.scatter(x='d', y='r21', c='C3', ax=axes[1])
    return data


if __name__ == "__main__":
    # limit()
    # cavity_resonances()
    mwion_scan()
    # svf_from_cav_res()
    # node_scan()
