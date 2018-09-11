# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 19:44:04 2018

@author: labuser
"""

# Import and plot frequency scans from the dye laser.

import os
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import pandas as pd


def dye_scan():
    fname = os.path.join("..", "2018-09-09", "1_freq_dye.txt")
    data = pd.read_csv(fname, sep='\t', comment="#", index_col=False)
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='f', inplace=True)
    fig, ax = plt.subplots()
    # ax.axvline(0, c='k')
    ax.axhline(0, c='k')
    # e29 = -3910.510993878823
    # e26 = -4865.269534632156
    # print(max(data['sig']))
    # ax.plot([e26]*2, [0, 1.2*max(data['sig'])], '--', c='grey')
    # ax.text(e26, ax.get_ylim()[1], "26",
    #         horizontalalignment='center', verticalalignment='top')
    # ax.plot([e29]*2, [0, 1.2*max(data['sig'])], '--', c='grey')
    # ax.text(e29, ax.get_ylim()[1], "29",
    #         horizontalalignment='center', verticalalignment='top')
    e27 = -4511.5
    for i in [-2, -1, 0, 1, 2]:
        ax.axvline(e27 + 2*i*19.6354, color='grey', linestyle='dashed')
    data.plot(x='f', y='sig', ax=ax)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Signal (arb. u.)")
    ax.set_xlim(-4800, -4200)
    fig.tight_layout()
    fig.savefig("DyeScan.pdf")
    return


def step_freq_fit(o, i, f):
    p = np.polyfit(i, f, o)
    fpoly = np.polyval(p, i)
    return fpoly


def diode_scan():
    """Display a close-up of n=47 with the diode laser"""
    folder = os.path.join("..", "2018-09-09")
    # 1
    fnames = ["10", "11"]
    # fname = "10_freq_diode.txt"
    for name in fnames:
        fname = name + "_freq_diode.txt"
        fname = os.path.join(folder, fname)
        data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
        data['fpoly'] = step_freq_fit(3, data['i'], data['f'])
        data['sig'] = data['s'] - data['sb']
        data.sort_values(by='i', inplace=True)
        fig, ax = plt.subplots()
        data.plot(x='fpoly', y='sig', ax=ax, label="n=27")
        ax.set_xlabel("Frequency (GHz)")
        ax.set_ylabel("Signal (arb. u.)")
        fig.tight_layout()
        fig.savefig("DiodeScan.pdf")
    return



def fourier(fname, mwf, ax=None):
    """Test out fourier analysis on the data."""
    # fig, ax = plt.subplots(nrows=1, ncols=1)
    data = delay_load(fname)
    nave = 10
    data = transform_delay(data, mwf, nave)
    t = np.fft.fft(np.array(data['nsig']))
    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1)
    p = np.power(np.abs(t), 2)
    ax.plot(p, '.-')
    ax.set_xlim(1, 5*13)
    ax.set_ylim(0, 1.2*max(p[range(1, 5*13)]))
    ax.set_title(fname)
    return


def delay_load(fname):
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    return data


def transform_delay(data, mwf, nave):
    """Take the delay data from LabView and produce normalized signal and
    distance, wavelength, and time delay info. Sort then rolling mean. Fold,
    resort, then rolling mean again. Return DataFrame sorted by ['d']."""
    # physical values
    m = 2.539e-7  # delay stage calibration, m/step
    c = 299792458.0  # Speed of Light, meters/second
    # transform
    data['norm'] = data['n'] - data['nb']
    data['sign'] = data['s'] - data['sb']
    data['nsig'] = data['sign'] / data['norm']
    # data['nsig'] = data['norm']  # !!!!
    data['dist'] = data['d']*m*2
    data['wlen'] = data['dist']*mwf/c
    data['time'] = data['dist']/c
    # sort
    data.sort_values(by = 'd', inplace=True)
    # rolling mean
    data['nsig_rm'] = data['nsig'].rolling(window=nave, center=True).mean()
    # !!!!
    # data['nsig_rm'] = data['norm'].rolling(window=nave, center=True).mean()
    # folding
    # data['wlen_fd'] = data['wlen'] % 2.0
    # data.sort_values(by = 'wlen_fd', inplace=True)
    # data['nsig_fd'] = data['nsig'].rolling(window=nave, center=True).mean()
    # re-sort
    data.sort_values(by = 'd', inplace=True)
    return data


def model_func_4(x, y0, a, phi, a2, phi2, a3, phi3, a4, phi4):
    """1st, 2nd, 3rd harmonic sinusoidal + offset model."""
    return y0 + a*np.sin(1*2*np.pi*x + phi) + a2*np.sin(2*2*np.pi*x + phi2) + \
        a3*np.sin(3*2*np.pi*x + phi3) + a4*np.sin(4*2*np.pi*x + phi4)
        

def model_p0(x, y):
    """Guesses reasonable starting parameters p0 to pass to model_func().
    x and y are pandas.Series
    Returns p0, array of [y0, a, phi]"""
    # y0 is the mean
    y0 = y.mean()
    # phi from averaged maximum and minimum
    yroll = y.rolling(window=9, center=True).mean()
    imax = yroll.idxmax()
    imin = yroll.idxmin()
    phi = ((x[imax] % 1) + ((x[imin]-0.5) % 1)) / 2
    phi = ((phi-0.25) % 1)*np.pi
    # a is max and min
    mx = yroll.max()
    mn = yroll.min()
    a = (mx-mn)/2
    return [y0, a, phi]


def model_p0_4(x, y):
    """Adds zeros for a2, phi2, a3, phi3"""
    return model_p0(x, y) + [0, 0, 0, 0, 0, 0]


def fitting_4(fname, mwf, plotting=False, printing=False, ax=None):
    data = delay_load(fname)
    nave = 10
    data = transform_delay(data, mwf, nave)
    p0 = model_p0_4(data['wlen'], data['nsig'])
    print(p0)
    popt, pcov = scipy.optimize.curve_fit(
            model_func_4, data['wlen'].astype(float),
            data['nsig'].astype(float), p0)
    data['fit'] = model_func_4(data['wlen'], *popt)
    if printing is True:
        pstring = "\n{0}:\nMean:\t{1}\n"
        pstring = pstring + "Amp:\t{2}\nPhase:\t{3}\n"
        pstring = pstring + "Amp2:\t{4}\nPhase2:\t{5}\n"
        pstring = pstring + "Amp3:\t{6}\nPhase3:\t{7}\n"
        pstring = pstring + "Amp4:\t{8}\nPhase4:\t{9}\n"
        print(pstring.format(fname, *popt))
    if plotting is True:
        if ax is None:
            fig, ax = plt.subplots(nrows=1, ncols=1)
        data.plot(x='wlen', y='nsig', color='grey', lw=0.5, ax=ax,
                  label="Data")
        data.plot(x='wlen', y='nsig_rm', lw=5, color='C0', ax=ax,
                  label="Averaged")
        data.plot(x='wlen', y='fit', color='k', ax=ax, label="Fit")
        ax.set(title=fname, xlabel=r"Delay (MW $\lambda$)",
                 ylabel="Norm. Signal")
    return popt


def delay():
    folder = os.path.join("..", "2018-09-09")
    fnames = ["2", "3", "4", "5", "6", "7"]
    mwf = 19635.4e6*2  # Hz after doubler
    for i, name in enumerate(fnames):
        fig, ax = plt.subplots(nrows=1, ncols=2)
        fname = name + "_delay.txt"
        fname = os.path.join(folder, fname)
        fitting_4(fname, mwf, plotting=True, printing=True, ax=ax[0])
        fourier(fname, mwf, ax[1])
    return

# main
# dye_scan()
# delay()
diode_scan()
