# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 19:36:49 2018

@author: labuser
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 19:22:41 2018

@author: labuser
"""

# Load and display limit scans from 2018-09-25

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import cauchy
from scipy.optimize import curve_fit
import pandas as pd


def limit_scan(fname):
    data = pd.read_csv(fname, sep='\t', comment="#", index_col=False)
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='f', inplace=True)
    data.plot(x='f', y='sig')
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


def mw_fscan(fname, d=1):
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False,
                       header=None, names=['f', 's'])
    data.sort_values(by='f', inplace=True)
    data['s'] = data['s']*d
    popt = cauchy_fit(data['f'].values, data['s'].values)
    # print(popt)
    ax = data.plot(x='f', y='s')
    ax.plot(data['f'].values, cauchy_model(data['f'].values, *popt))
    ax.plot(data['f'].values,
            data['s'].values - cauchy_model(data['f'].values, *popt))
    return


def step_freq_fit(o, i, f):
    p = np.polyfit(i, f, o)
    fpoly = np.polyval(p, i)
    return fpoly


def diode_scan(fname, fig, ax):
    """Display a close-up of n=47 with the diode laser"""
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['fpoly'] = step_freq_fit(5, data['i'], data['f'])
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='i', inplace=True)
    # fig, ax = plt.subplots()
    data.plot(x='fpoly', y='sig', ax=ax)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Signal (arb. u.)")
    fig.tight_layout()
    return


def diode_double(fname, fig, ax):
    "Display a scan with two plots"""
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['fpoly'] = step_freq_fit(5, data['i'], data['f'])
    data['sig'] = data['s'] - data['b']
    data['nrm'] = data['n'] - data['b']
    data.sort_values(by='i', inplace=True)
    # fig, ax = plt.subplots()
    data.plot(x='fpoly', y='sig', ax=ax)
    data.plot(x='fpoly', y='nrm', ax=ax)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Signal (arb. u.)")
    fig.tight_layout()
    return

    
if __name__ == "__main__":
    # files
    # fname = "1_fscan.txt"
    fname = "2_fscan.txt"
    # fname = "3_freq_diode.txt"
    # fname = "4_freq_diode.txt"
    # fname = "5_freq_diode.txt"
    # fname = "6_freq_diode.txt"
    # fname = "7_freq_diode.txt"
    # fname = "8_freq_diode_d.txt"
    # fig, ax = plt.subplots()
    folder = os.path.join("..", "2018-09-25")
    fname = os.path.join(folder, fname)
    # analysis
    # limit_scan(fname)
    mw_fscan(fname, -1)
    # diode_scan(fname, fig, ax)
    # diode_double(fname, fig, ax)
