# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 02:46:46 2018

@author: labuser
"""

# Analysis of phase modulation delay data

import os
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import pandas as pd


def running_mean(df, xk, yk, n):
    """Moving step function average for n points"""
    cumsum = np.array(df[yk].cumsum(skipna=True))
    y = (cumsum[n:] - cumsum[:-n]) / n
    cumsum = np.array(df[xk].cumsum(skipna=True))
    x = (cumsum[n:] - cumsum[:-n]) / n
    return x, y


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


def fold_delay(data, fold, nave):
    data['wlen_fd'] = data['wlen'] % fold
    data.sort_values(by='wlen_fd', inplace=True)
    data['nsig_fd'] = data['nsig'].rolling(window=nave, center=True).mean()
    return data


def Analyze_2018_07_18():
    """From 2018-07-18, analyze the two delay scans 6 (no static) and 7
    (+200 mV on Top). Import, transform, average, and fold the data.
    I care if there is modulation at 1x and 2x the MW frequency. I will
    investigate both the normalized signal, but also the raw signal and "norm"
    to see if there is any modulation.
    """
    # parameters
    mwf = 18268e6*2  # MW frequency in Hz
    nave = 10  # averaging window size
    # import data
    folder = os.path.join("..", "2018-07-18")
    # No static
    fname = "6_delay.txt"
    fname = os.path.join(folder, fname)
    data000 = pd.read_csv(fname, sep="\t", index_col=False, comment="#")
    # +200 mV on Top
    fname = "7_delay.txt"
    fname = os.path.join(folder, fname)
    data200 = pd.read_csv(fname, sep="\t", index_col=False, comment="#")
    # transform
    data000 = transform_delay(data000, mwf, nave)
    data200 = transform_delay(data200, mwf, nave)
    # plotting
    fig, axes = plt.subplots(nrows=4, ncols=2, sharex=False, sharey=False,
                             figsize=(8, 10))
    # averaged
    i = 0
    data000.plot(x='wlen', y='nsig_rm', label="  0 mV/cm", ax=axes[i, 0])
    data200.plot(x='wlen', y='nsig_rm', label="+14 mV/cm", ax=axes[i, 1])
    # fold by 2
    i = 1
    fold = 2
    data000 = fold_delay(data000, fold, nave)
    data200 = fold_delay(data200, fold, nave)
    data000.plot(x='wlen_fd', y='nsig_fd', label="  0 mV/cm", ax=axes[i, 0])
    data200.plot(x='wlen_fd', y='nsig_fd', label="+14 mV/cm", ax=axes[i, 1])
    # fold by 1
    i = 2
    fold = 1
    data000 = fold_delay(data000, fold, nave)
    data200 = fold_delay(data200, fold, nave)
    data000.plot(x='wlen_fd', y='nsig_fd', label="  0 mV/cm", ax=axes[i, 0])
    data200.plot(x='wlen_fd', y='nsig_fd', label="+14 mV/cm", ax=axes[i, 1])
    # fold by 0.5
    i = 3
    fold = 0.5
    data000 = fold_delay(data000, fold, nave)
    data200 = fold_delay(data200, fold, nave)
    data000.plot(x='wlen_fd', y='nsig_fd', label="  0 mV/cm", ax=axes[i, 0])
    data200.plot(x='wlen_fd', y='nsig_fd', label="+14 mV/cm", ax=axes[i, 1])
    # labels
    for i in [0, 1, 2, 3]:
        axes[i, 0].set(xlabel="", ylabel="")
        axes[i, 1].set(xlabel="", ylabel="")
    axes[0, 0].set(title="0 mV/cm",
                   ylabel=("Averaged" + "\n\n" + "Norm. Signal"))
    axes[0, 1].set(title="+14 mV/cm")
    axes[1, 0].set(ylabel=("Fold by 2" + "\n\n" + "Norm. Signal"))
    axes[2, 0].set(ylabel=("Fold by 1" + "\n\n" + "Norm. Signal"))
    axes[3, 0].set(ylabel=("Fold by 0.5" + "\n\n" + "Norm. Signal"),
                   xlabel=r"Delay ($\lambda$)")
    axes[3, 1].set(xlabel=r"Delay ($\lambda$)")
    # final
    fig.tight_layout()
    plt.savefig("delay_folds.pdf")
    return


def Analyze_2018_07_19():
    """From 2018-07-19, analyze the delay scans taken with and without static
    field."""
    folder = os.path.join("..", "2018-07-19")
    # ==========
    # 0 Field MW Power
    # Sets 10, 12, 13
    # ==========
    fig, axes = plt.subplots(nrows=1, ncols=1)
    nave = 10
    # 17 dB MW, no Static
    fname = "10_delay.txt"
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    mwf = 18268e6*2
    data = transform_delay(data, mwf, nave)
    data.plot(x='wlen', y='nsig_rm', ax=axes, label=r"$P_0$")
    # 23 dB MW, no static
    fname = "12_delay.txt"
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    mwf = 18267e6*2
    data = transform_delay(data, mwf, nave)
    data.plot(x='wlen', y='nsig_rm', ax=axes, label=r"$P_0$ - 6 dB")
    # 11 dB MW, no static
    fname = "13_delay.txt"
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    mwf = 18267e6*2
    data = transform_delay(data, mwf, nave)
    data.plot(x='wlen', y='nsig_rm', ax=axes, label=r"$P_0$ + 6 dB")
    # texts labels
    # props = dict(boxstyle='round', facecolor='white', alpha=1.0)
    axes.text(12.5, 0.6, r"$P_0$ - 17 dB", rotation=-90,
              verticalalignment='center', size=12)
    axes.text(12.5, 0.25, r"$P_0$ - 11 dB", rotation=-90,
              verticalalignment='center', size=12)
    axes.text(12.5, 0.9, r"$P_0$ - 23 dB", rotation=-90,
              verticalalignment='center', size=12)
    # pretty
    axes.legend().remove()
    axes.xaxis.label.set_size(14)
    axes.yaxis.label.set_size(14)
    axes.title.set_size(18)
    axes.set(xlabel=r"Delay (MW $\lambda$)",
             ylabel="Norm. Signal",
             ylim=(0, 1.0),
             title="Centered at -12 GHz, Modulation Index = 1.4")
    fig.tight_layout(rect=[0, 0, 0.95, 1])
    fig.savefig("NoStatic_Power.pdf")
    # ==========
    # No Field vs Static Field
    # Sets 10, 11, 15
    # ==========
    fig, axes = plt.subplots(nrows=1, ncols=1)
    nave = 10
    # 17 dB MW, no Static
    fname = "10_delay.txt"
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    mwf = 18268e6*2
    data = transform_delay(data, mwf, nave)
    data.plot(x='wlen', y='nsig_rm', ax=axes, label=r"0 mV/cm")
    # 17 dB MW, +200 mV static
    fname = "11_delay.txt"
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    mwf = 18268e6*2
    data = transform_delay(data, mwf, nave)
    data.plot(x='wlen', y='nsig_rm', ax=axes, label=r"+14.4 mV/cm")
    # 17 dB MW, -200 mV static
    fname = "15_delay.txt"
    fname = os.path.join(folder, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    mwf = 18268e6*2
    data = transform_delay(data, mwf, nave)
    mask = (data['i'] < 751)  # Vacuum shutdown in the middle of collection.
    data = data[mask]
    data.plot(x='wlen', y='nsig_rm', ls='dashed', ax=axes,
              label=r"-14.4 mV/cm")
    # text labels
    axes.text(12.5, 0.6, "0 mV/cm", rotation=-90,
              verticalalignment='center', size=12)
    axes.text(12.5, 0.25, "+ 14 mV/cm\n(-14 mV/cm Dashed)", rotation=-90,
              verticalalignment='center', size=12)
    # pretty
    axes.legend().remove()
    axes.xaxis.label.set_size(14)
    axes.yaxis.label.set_size(14)
    axes.title.set_size(18)
    axes.set(xlabel=r"Delay (MW $\lambda$)",
            ylabel="Norm. Signal",
            ylim=(0, 1.0),
            title="Centered at -12 GHz, Modulation Index = 1.4")
    fig.tight_layout(rect=[0, 0, 0.95, 1])
    fig.savefig("WithStatic.pdf")
    return


def model_func(x, y0, a, phi):
    """Sinusoidal plus offset model for delay scan phase dependence.
    "x" is the delay in wavelengths
    "y" is the normalized Rydberg signal.
    Returns model dataframe and fit parameters.
    """
    return y0 + a*np.sin(2*2*np.pi*x + phi)


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


def model_func_4(x, y0, a, phi, a2, phi2, a3, phi3, a4, phi4):
    """1st, 2nd, 3rd harmonic sinusoidal + offset model."""
    return y0 + a*np.sin(1*2*np.pi*x + phi) + a2*np.sin(2*2*np.pi*x + phi2) + \
        a3*np.sin(3*2*np.pi*x + phi3) + a4*np.sin(4*2*np.pi*x + phi4)
        

def model_p0_4(x, y):
    """Adds zeros for a2, phi2, a3, phi3"""
    return model_p0(x, y) + [0, 0, 0, 0, 0, 0]


def fitting(fname, mwf, plotting=False, printing=False):
    """Fit delay scan data, and plot and print results if asked to."""
    data = delay_load(fname)
    nave = 10
    data = transform_delay(data, mwf, nave)
    # plot
    # fit
    p0 = model_p0(data['wlen'], data['nsig'])
    # data['guess'] = model_func(data['wlen'], *p0)
    # data.plot(x='wlen', y='guess', ax=axes, label="Guess")
    popt, pcov = scipy.optimize.curve_fit(
                model_func, data['wlen'].astype(float),
                data['nsig'].astype(float), p0)
    data['fit'] = model_func(data['wlen'], *popt)
    if printing is True:
        print("\n{0}:\nMean:\t{1}\nAmp:\t{2}\nPhase:\t{3}\n".format(
                fname, *popt))
    # pretty
    if plotting is True:
        fig, axes = plt.subplots(nrows=1, ncols=1)
        data.plot(x='wlen', y='nsig', color='grey', lw=0.5, ax=axes,
                  label="Data")
        data.plot(x='wlen', y='nsig_rm', lw=5, color='C0', ax=axes,
                  label="Averaged")
        data.plot(x='wlen', y='fit', color='k', ax=axes, label="Fit")
        axes.set(title=fname, xlabel=r"Delay (MW $\lambda$)",
                 ylabel="Norm. Signal")
    return popt


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

def amp_v_mw():
    """Compare how the phase dependence changes with MW field at MI = 1.4"""
    mwf = 18268e6*2  # GHz after doubler
    attns = [17, 19, 15, 18, 16, 17.5]
    flist = np.array(["1", "2", "3", "4", "5", "6"], dtype=object)
    folder = os.path.join("..", "2018-07-20")
    for i in range(len(flist)):
        flist[i] = flist[i] + "_delay.txt"
        flist[i] = os.path.join(folder, flist[i])
    # print(flist)
    record = pd.DataFrame({'fname': flist})
    record['attn'] = attns
    record['mean'] = np.ones(len(record))*np.NaN
    record['amp'] = np.ones(len(record))*np.NaN
    record['phase'] = np.ones(len(record))*np.NaN
    for i in record.index:
        popt = fitting(record.loc[i, 'fname'], mwf)
        record.loc[i, ['mean', 'amp', 'phase']] = (*popt,)
    record['phase'] = record['phase'] % (np.pi)
    print(record)
    record.sort_values(by='attn', inplace=True)
    # plot
    fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col',
                             figsize=(8, 10.5))
    record.plot(x='attn', y='amp', marker='o', ax=axes[1])
    record.plot(x='attn', y='mean', marker='o', ax=axes[0])
    record.plot(x='attn', y='phase', marker='o', ax=axes[2])
    axes[2].set(ylim=(0, np.pi), yticks=[0, np.pi/2, np.pi],
                yticklabels=["0", r"$\pi$/2", r"$\pi$"])
    return record


def amp_v_mod():
    """Compare MI = 1.4 and 2.4 (where 0th line has no power)."""
    folder = os.path.join("..", "2018-07-20")
    mwf = 18268e6*2  # GHz after doubler
    # List for Amp vs MW with ModIndex = 1.4
    attns = [-17, -19, -15, -18, -16, -17.5]
    fnames = np.array(["1", "2", "3", "4", "5", "6"], dtype=object)
    # list for comparing MW amplitude with Mod Index = 1.6
    # attns = [-17.5, -16, -14, -15, -17, -15.5, -23, -11]
    # fnames = np.array(["8", "9", "10", "11", "12", "13", "14", "15"],
    #                   dtype=object)
    # list for comparing Phase Modulation
    # attns = [-35, -30, -32, -33, -31, -38]
    # fnames = np.array(
    #         ["7", "8", "16", "17", "18", "19"],
    #         dtype=object)
    record = pd.DataFrame({'fname': fnames})
    record['attn'] = attns
    fitkeys = ['mean', 'amp', 'phase', 'amp2', 'phase2', 'amp3', 'phase3',
               'amp4', 'phase4']
    for key in fitkeys:
        record[key] = np.ones(len(record))*np.NaN
    for i in record.index:
        fname = record.loc[i, 'fname']
        fname = fname + "_delay.txt"
        fname = os.path.join(folder, fname)
        record.loc[i, 'fname'] = fname
        popt = fitting_4(fname, mwf, plotting=True, printing=True)
        record.loc[i, fitkeys] = (*popt,)
    for key in ['phase', 'phase2', 'phase3', 'phase4']:
        record[key] = record[key] % np.pi
    record.sort_values(by='attn', inplace=True)
    fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col',
                             figsize=(8, 10.5))
    record.plot(x='attn', y='mean', marker='o', ax=axes[0], c='C3')
    record.plot(x='attn', y='amp2', marker='o', ax=axes[1],
                label=r"Amp @ $2 \cdot f_{MW}$")
    record.plot(x='attn', y='phase2', marker='o', ax=axes[2],
                label=r"Phase @ $2 \cdot f_{MW}$")
    record.plot(x='attn', y='amp4', marker='o', ax=axes[1],
                label=r"Amp @ $4 \cdot f_{MW}$")
    record.plot(x='attn', y='phase4', marker='o', ax=axes[2],
                label=r"Phase @ $4 \cdot f_{MW}$")
    axes[2].set(ylim=(0, np.pi), yticks=[0, np.pi/2, np.pi],
                yticklabels=["0", r"$\pi$/2", r"$\pi$"])
    axes[2].set(xlabel="MW Attn (dB)", ylabel="Phase")
    axes[1].set(ylabel="Amplitude")
    axes[0].set(ylabel="Mean", title="Mod Index = 1.4")
    fig.tight_layout()
    fig.savefig("AmpvMW.pdf")
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


def Analyze_2018_08_03():
    folder = os.path.join("..", "2018-08-03")
    fnames = np.array(["3", "4", "5", "6"], dtype=object)
    mwf = 18258e6*2  # Hz after doubler
    for i, name in enumerate(fnames):
        fname = name + "_delay.txt"
        fname = os.path.join(folder, fname)
        fitting_4(fname, mwf, plotting=True, printing=True)
        fourier(fname, mwf)
    return


def Analyze_2018_08_04():
    folder = os.path.join("..", "2018-08-04")
    fnames = np.array(["1", "2", "3", "4"], dtype=object)
    mwf = 18258e6*2  # Hz after doubler
    for i, name in enumerate(fnames):
        fig, ax = plt.subplots(nrows=1, ncols=2)
        fname = name + "_delay.txt"
        fname = os.path.join(folder, fname)
        fitting_4(fname, mwf, plotting=True, printing=True, ax=ax[0])
        fourier(fname, mwf, ax[1])
    return


def n47_modulation():
    folder = os.path.join("..", "2018-08-06")
    fnames = ["8_delay_blue.txt", "9_delay_red.txt", "10_delay.txt"]
    mwf = 18268e6*2
    for i, name in enumerate(fnames):
        fig, ax = plt.subplots(nrows=1, ncols=2)
        fname = os.path.join(folder, name)
        fitting_4(fname, mwf, plotting=True, printing=True, ax=ax[0])
        fourier(fname, mwf, ax[1])
    return


# ==========
# main script
# Analyze_2018_07_18()
Analyze_2018_07_19()
# amp_v_mw()
# amp_v_mod()
# fourier()
# Analyze_2018_08_03()
# n47_modulation()
