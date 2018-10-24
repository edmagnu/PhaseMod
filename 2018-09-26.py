# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 17:27:01 2018

@author: labuser
"""
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
    data['dif'] = data['sig'] - data['nrm']
    data.sort_values(by='i', inplace=True)
    # fig, ax = plt.subplots()
    data.plot(x='fpoly', y='sig', ax=ax)
    data.plot(x='fpoly', y='nrm', ax=ax)
    data.plot(x='fpoly', y='dif', ax=ax)
    # ax.set_xlabel("Frequency (GHz)")
    ax.set_xlabel("")
    # ax.set_ylabel("Signal (arb. u.)")
    ax.set_ylabel("")
    # fig.tight_layout()
    return


def shift_plots():
    # files
    files = pd.DataFrame()
    obs = {'f': "6_freq_diode_d.txt", "n": "18.5 GHz, 39.15 mm",
           'g': 3, 'mw': 0}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "7_freq_diode_d.txt", "n": "19.6 GHz, 39.15 mm",
           'g': 3, 'mw': 1}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "8_freq_diode_d.txt", "n": "19.6 GHz, 38.15 mm",
           'g': 4, 'mw': 1}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "9_freq_diode_d.txt", "n": "18.5 GHz, 38.15 mm",
           'g': 4, 'mw': 0}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "10_freq_diode_d.txt", "n": "18.5 GHz, 37.15 mm",
           'g': 5, 'mw': 0}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "11_freq_diode_d.txt", "n": "19.6 GHz, 37.15 mm",
           'g': 5, 'mw': 1}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "12_freq_diode_d.txt", "n": "19.6 GHz, 36.15 mm",
           'g': 6, 'mw': 1}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "13_freq_diode_d.txt", "n": "18.5 GHz, 36.15 mm",
           'g': 6, 'mw': 0}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "14_freq_diode_d.txt", "n": "18.5 GHz, 40.15 mm",
           'g': 2, 'mw': 0}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "15_freq_diode_d.txt", "n": "19.6 GHz, 40.15 mm",
           'g': 2, 'mw': 1}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "16_freq_diode_d.txt", "n": "19.6 GHz, 41.15 mm",
           'g': 1, 'mw': 1}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "17_freq_diode_d.txt", "n": "18.5 GHz, 41.15 mm",
           'g': 1, 'mw': 0}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "18_freq_diode_d.txt", "n": "18.5 GHz, 42.15 mm",
           'g': 0, 'mw': 0}
    files = files.append(obs, ignore_index=True)
    obs = {'f': "19_freq_diode_d.txt", "n": "19.6 GHz, 42.15 mm",
           'g': 0, 'mw': 1}
    files = files.append(obs, ignore_index=True)
    # figure
    fig, axes = plt.subplots(nrows=int(files['g'].max()) + 1,
                             ncols=int(files['mw'].max()) + 1,
                             sharex=True,
                             figsize=(6, 1.5*len(files)))
    for i in files.index:
        obs = files.loc[i]
        folder = os.path.join("..", "2018-09-26")
        print(obs)
        iax = int(obs['g'])
        jax = int(obs['mw'])
        ax = axes[iax, jax]
        fname = os.path.join(folder, obs['f'])
        diode_double(fname, fig, ax)
        ax.set_title(obs['n'])
        ax.legend().remove()
    fig.tight_layout()
    return


if __name__ == "__main__":
    # files
    # fname = "1_fscan.txt"
    # fname = "2_fscan.txt"
    # fname = "3_freq_diode_d.txt"
    # fname = "4_freq_diode_d.txt"
    # folder = os.path.join("..", "2018-09-26")
    # fname = os.path.join(folder, fname)
    # analysis
    # limit_scan(fname)
    # mw_fscan(fname, 1)
    # diode_scan(fname, fig, ax)
    # fig, ax = plt.subplots()
    # diode_double(fname, fig, ax)
    shift_plots()

