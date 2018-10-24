# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 18:28:11 2018

@author: labuser
"""

# Eric Magnuson, University of Virginia
# Toolkit

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import cauchy
import pandas as pd

# ==========
# MW Cavity Resonance
# ==========

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


def mw_fscan(fname, d, ax, plotting=True, norm=True):
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False,
                       header=None, names=['f', 'b', 's', 'r'])
    data.sort_values(by='f', inplace=True)
    data['sig'] = data['s'] - data['b']
    data['ref'] = data['r'] - data['b']
    if norm is True:
        data['nrm'] = data['sig'] / data['ref']  # norm by signal / reference
    else:
        data['nrm'] = data['sig']
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


# ==========
# Frequency Scans
# ==========


def dye_scan(fname):
    data = pd.read_csv(fname, sep='\t', comment="#", index_col=False)
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='f', inplace=True)
    return data


def dye_plot(data, label, ax):
    data.plot(x='f', y='sig', label=label, ax=ax)
    ax.set_xlabel("Frequency - IL (GHz)")
    ax.set_ylabel("Signal (arb. u.)")
    return


def step_freq_fit(o, i, f):
    p = np.polyfit(i, f, o)
    fpoly = np.polyval(p, i)
    return fpoly


def diode_scan(fname):
    """Display diode scan with polynomial fitted laser frequency."""
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['fpoly'] = step_freq_fit(5, data['i'], data['f'])
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='i', inplace=True)
    return data


def diode_plot(data, ax, label):
    data.plot(x='fpoly', y='sig', ax=ax, label=label)
    ax.set_ylabel("Signal (arb. u.)")
    ax.set_xlabel("Frequency - IL (GHz)")
    return


def diode_blink_scan(fname):
    """Display diode scan with polynomial fitted laser frequency."""
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['fpoly'] = step_freq_fit(5, data['i'], data['f'])
    data['sig'] = data['s'] - data['b']
    data['ref'] = data['r'] - data['b']
    data.sort_values(by='i', inplace=True)
    return data


def diode_blink_plot(data, axs, axr, label):
    data.plot(x='fpoly', y='sig', ax=axs, label=(label + " sig"))
    data.plot(x='fpoly', y='ref', ax=axr, label=(label + " ref"))
    for ax in [axs, axr]:
        ax.set_ylabel("Signal (arb. u.)")
        ax.set_xlabel("Frequency - IL (GHz)")
    return


# ==========
# Delay Scans
# ==========


def steps_wvlg(mwf):
    # physical values
    m = 2.539e-7  # delay stage calibration, m/step
    c = 299792458.0  # Speed of Light, meters/second
    n = 1.00029  # Index of Refraction in Air
    wln = c/(mwf*n)
    print("Wavelength = ", wln, " M")
    spw = wln/(2*m)
    print("Steps per Wavelength = ", spw)
    return


def delay_load(fname):
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    return data


def blink_transform(data):
    """Translate the MWBlink columns ['i', 'd', 'b', 's', 'r'] to the columns
    expected in a delay scan ['i', 'd', 'n', 'nb', 's', 'sb']"""
    data['sb'] = data['b']
    data['nb'] = data['b']
    data['n'] = data['r']
    return data


def transform_delay(data, mwf, nave, sortkey, fold=1, blink=False):
    """Take the delay data from LabView and produce normalized signal and
    distance, wavelength, and time delay info. Sort then rolling mean. Fold,
    resort, then rolling mean again. Return DataFrame sorted by ['d']."""
    # physical values
    m = 2.539e-7  # delay stage calibration, m/step
    n = 1.00029  # index of refraction in air
    c = 299792458.0  # Speed of Light, meters/second
    # transform
    if blink is True:
        data = blink_transform(data)
    data['norm'] = data['n'] - data['nb']
    data['sign'] = data['s'] - data['sb']
    data['nsig'] = data['sign'] / data['norm']
    data['dist'] = data['d']*m*2
    data['wlen'] = data['dist']*mwf*n/c
    data['time'] = data['dist']/c
    # sort
    data.sort_values(by = 'd', inplace=True)
    # rolling mean
    data['nsig_rm'] = data['nsig'].rolling(window=nave, center=True).mean()
    data.sort_values(by='d', inplace=True)
    # fold
    data['wlen_fold'] = data['wlen']%fold
    data.sort_values(by='wlen_fold', inplace=True)
    data['nsig_fold'] = data['nsig'].rolling(window=nave, center=True).mean()
    # sort
    data.sort_values(by=sortkey, inplace=True)
    return data


def delay_plot(fname, xkey, ykey, ykey2, mwf, nave, ax, label, fold=1,
               blink=False):
    """Plot a delay scan by loading, transforming, and plotting it."""
    data = delay_load(fname)
    data = transform_delay(data, mwf, nave, xkey, fold, blink)
    if ykey not in ['nsig_fold', 'nsig_rm']:
        data[ykey + "_rm"] = data.rolling(window=nave, center=True).mean()
        ykey = ykey + "_rm"
    # print(data)
    mask = np.logical_not(np.isnan(data[ykey]))
    mask = mask & np.logical_not(np.isinf(data[ykey]))
    # print(mask)
    data[mask].plot(x=xkey, y=ykey2, label="raw", ax=ax, ls="", marker=".",
                    c="lightgrey")
    data[mask].plot(x=xkey, y=ykey, label=label, ax=ax, lw=2)
    return data
