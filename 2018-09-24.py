# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 19:22:41 2018

@author: labuser
"""

# Load and display limit scans from 2018-09-24

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
    print("Center Frequency is : ", popt[1]*1e-6, " GHz")
    return popt


def mw_fscan(fname):
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False,
                       header=None, names=['f', 's'])
    data.sort_values(by='f', inplace=True)
    popt = cauchy_fit(data['f'].values, data['s'].values)
    # print(popt)
    ax = data.plot(x='f', y='s')
    ax.plot(data['f'].values, cauchy_model(data['f'].values, *popt))
    return


if __name__ == "__main__":
    # fname = "1_lim_dye.txt"
    fname = "2_fscan.txt"
    folder = os.path.join("..", "2018-09-24")
    fname = os.path.join(folder, fname)
    # limit_scan(fname)
    mw_fscan(fname)