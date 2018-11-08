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
    print("p0 = ", p0)
    popt, pcov = curve_fit(cauchy_model, x, y, p0)
    print("popt = ", popt)
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
    print("Center Frequency is : ", popt[1]*1e-6, " MHz")
    print("FWHM is : ", 2*popt[2]*1e-6, " MHz")
    print("Q is : ", popt[1]/(2*popt[2]))
    # print(popt)
    if plotting is True:
        data.plot(x='f', y='nrm', ax=ax)
        ax.plot(data['f'].values, cauchy_model(data['f'].values, *popt))
        ax.plot(data['f'].values,
                data['nrm'].values - cauchy_model(data['f'].values, *popt))
    return data, popt


# ==========
# Frequency Scans
# ==========


def dye_qs_lim(fname, lo_win, hi_win, ax=None, window=9):
    import pandas as pd
    if ax is None:
        import matplotlib.pyplot
        fig, ax = plt.subplots()
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data.sort_values(by='f', inplace=True)
    data['s_rm'] = data['s'].rolling(window=window, center=True).mean()
    data.plot(x='f', y='s_rm', ax=ax)
    lo = data['s_rm'][(data['f'] > lo_win[0]) & (data['f'] < lo_win[1])].mean()
    hi = data['s_rm'][(data['f'] > hi_win[0]) & (data['f'] < hi_win[1])].mean()
    ax.axhline(lo, c='k')
    ax.axhline(hi, c='k')
    ax.axhline((lo + hi)/2, c='k')
    ax.legend().remove()
    return


def mw_res(fname, marker, label, mwf, ax):
    import numpy as np
    import pandas as pd
    # fname = "7_mwres.txt"
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data.sort_values(by='f', inplace=True)
    data['s_rm'] = data['s'].rolling(window=9, center=True).mean()
    data.plot(x='f', y='s_rm', ax=ax, label=label)
    for freq in (np.array([-2, -1, 0, 1, 2])*mwf + marker):
        ax.axvline(freq, c='grey', ls='dashed')
    ax.set_ylabel("Signal")
    ax.set_xlabel("Frequency (GHz)")
    return


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
    data, popt, pcov = fit_delay(data, 'nsig')
    return data, popt, pcov


def wlen_to_step(wlen, mwf):
    m = 2.539e-7  # delay stage calibration, m/step
    n = 1.00029  # index of refraction in air
    c = 299792458.0  # Speed of Light, meters/second
    dist = wlen*c/(mwf*n)
    step = dist/(2*m)
    return step


def step_to_wlen(step, mwf):
    m = 2.539e-7  # delay stage calibration, m/step
    n = 1.00029  # index of refraction in air
    c = 299792458.0  # Speed of Light, meters/second
    dist = step*m*2
    wlen = dist*mwf*n/c
    return wlen


def fit_model(x, a0, a1, phi1, a2, phi2, a3, phi3, a4, phi4):
    val = (a0 +
           a1*np.cos(1*2*np.pi*(x - phi1)) +
           a2*np.cos(2*2*np.pi*(x - phi2)) +
           a3*np.cos(3*2*np.pi*(x - phi3)) +
           a4*np.cos(4*2*np.pi*(x - phi4)))
    return val


def fit_delay(data, ykey):
    p0 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    popt, pcov = curve_fit(fit_model, data['wlen'].values, data[ykey].values,
                           p0)
    fit = fit_model(data['wlen'].values, *popt)
    data['fit'] = fit
    return data, popt, pcov


def fit_report(fname, label, popt):
    print("\n" + fname + "    " + label)
    names = ["a0", "a1", "phi1", "a2", "phi2", "a3", "phi3", "a4", "phi4"]
    for i, name in enumerate(names):
        print(name + " = " + str(popt[i]))
    return


def delay_plot(fname, xkey, ykey, ykey2, mwf, nave, ax, label, fold=1,
               blink=False):
    """Plot a delay scan by loading, transforming, and plotting it."""
    data = delay_load(fname)
    data, popt, pcov = transform_delay(data, mwf, nave, xkey, fold, blink)
    fit_report(fname, label, popt)
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
    data[mask].plot(x=xkey, y='fit', label='fit', ax=ax, lw=2)
    return data, popt, pcov


def delay_short(fname, mwf, ax, window=4):
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = window
    fold = 1
    blink = False
    data, popt, pcov = delay_plot(fname, xkey, ykey, ykey2, mwf, nave, ax,
                                  label="", fold=fold, blink=blink)
    stepmin = wlen_to_step(popt[2]+6, mwf)
    stepmax = wlen_to_step(popt[2]+6.5, mwf)
    # ax.axvline(step_to_wlen(stepmin, mwf)%1, c='grey', ls='dashed')
    # ax.axvline(step_to_wlen(stepmax, mwf)%1, c='grey', ls='dashed')
    print("step_min = ", stepmin)
    print("step_max = ", stepmax)
    return data, stepmin, stepmax



# ==========
# Phase Modulation Tool
# ==========


def gba_target(x, value, order):
    import scipy.special as sp
    return (sp.jv(order, x)**2 - value)**2


def get_bessel_arg(amp_off, amp_on, amp_0, guess=1.0, quiet=False, order=0):
    import scipy.optimize as opt
    import scipy.special as sp
    value = (amp_on - amp_0)/(amp_off - amp_0)
    args = (value, order)
    fit = opt.minimize(gba_target, guess, args=args, bounds=[(0, 100)])
    if quiet is False:
        print(fit)
    fit = fit['x'][0]
    if quiet is False:
        print("fit = ", fit)
        print("result = ", gba_target(fit, value, order))
        print("value = ", value)
        print("jv({0}, fit) = ".format(order), sp.jv(order, fit)**2)
    return fit

def gba_01(aoff, a0, a1, zero, quiet=False):
    fit0 = get_bessel_arg(aoff, a0, zero, order=0, quiet=quiet)
    fit1 = get_bessel_arg(aoff, a1, zero, order=1, quiet=quiet)
    return fit0, fit1
