# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 19:32:17 2018

@author: edmag
"""

# Analyze saved Stark Maps of Li7 n=28 from ARC

# import os
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.stats import norm
import pandas as pd


def progress(source, i, total):
    """print an updating report of 'source: i/total'"""
    # start on fresh line
    if i == 0:
        print()
    # progress
    print("\r{0}: {1} / {2}".format(source, i+1, total), end="\r")
    # newline if we've reached the end.
    if i+1 == total:
        print()
    return


def line_model(x, loc, amp):
    return


def read_highlight():
    fname = "Lithium7StarkMap_highlight.csv"
    data = pd.read_csv(fname, comment="#", index_col=False, header=None)
    return data


def read_elevels():
    fname = "Lithium7StarkMap_energyLevels.csv"
    data = pd.read_csv(fname, comment="#", index_col=False, header=None)
    return data


def read_efield():
    fname = "Lithium7StarkMap_eField.csv"
    data = pd.read_csv(fname, comment="#", index_col=False, header=None)
    data.rename(index=str, columns={0: "efield"}, inplace=True)
    return data


def build_spectroscopy(e, fmin, fmax, ax, label="", lw=0.1, sbds=False,
                       fstruct=False):
    """Build expected spectroscopy based on field and f-character."""
    # fig, ax = plt.subplots()
    mwf = 18.5*2
    # import eFields data, and find the right index for the specified field 'e'
    efld = read_efield()
    i_ef = (efld['efield'] - e).abs().argsort()[0]
    print(efld.iloc[i_ef]*1e-2, " V/cm")
    # extract the set of levels and highlighting that corresponds to 'e'
    elvl = read_elevels().iloc[i_ef]
    hglt = read_highlight().iloc[i_ef]
    # build an expected spectrum from the line model, levels, and highlighting.
    # array of frequencies separated by 1 MHz, with 10% padding.
    pad = np.round((fmax - fmin)/10, 2)
    if pad < 1:
        pad = 1
    df = 0.001  # 1 MHz
    spectrum = pd.DataFrame({'freq': np.arange(fmin - pad, fmax + pad, df)})
    spectrum['freq_m1'] = spectrum['freq'] - mwf
    spectrum['freq_p1'] = spectrum['freq'] + mwf
    spectrum['signal'] = 0
    # start adding gaussian lines with 100 MHz width, centers based on elvl,
    #   and amplitudes based on hglt
    mask = (elvl > (fmin - pad)) & (elvl < (fmax + pad))
    t = len(elvl[mask])
    for i, lvl in enumerate(elvl[mask]):
        progress('build_spectroscopy()', i, t)
        # FWHM = 2.3548 * sigma
        scale = lw/2.3548  # 100 MHz, Dye Amplified Diode Laser
        # scale = 12/2.3548  # 12 GHz, Dye Laser
        amp = hglt[mask].iloc[i]
        # line 0
        line = amp*norm.pdf(spectrum['freq'], lvl, scale)
        spectrum['signal'] = spectrum['signal'] + line
        # line 1
    # plot
    for i in [-1, -0.5, 0, 0.5, 1]:
        # 0 field f state and sidebands
        ax.axvline(-4512.46 + i*mwf, c='lightgrey', ls='dashed')
    spectrum_shifted = spectrum.copy()
    new_sig = spectrum_shifted['signal'].values[1050:]
    new_sig = np.append(new_sig, np.zeros(1050))
    spectrum_shifted['signal'] = new_sig
    if fstruct is True:
        spectrum['comb'] = spectrum['signal'].add(
                0.3*spectrum_shifted['signal'], fill_value=0)
        if label is "":
            label = "Fundamental w/ 3D FS Splitting"
    else:
        spectrum['comb'] = spectrum['signal']
        if label is "":
            label = "Fundamental"
    spectrum.plot(x='freq', y='comb', ax=ax, c='C0', label=label)
    if sbds is True:
        spectrum['comb_mw'] = spectrum['comb']*0.5
        spectrum.plot(x='freq_m1', y='comb_mw', ax=ax, c='C1',
                      label=r"-1 $f_{MW}$")
        spectrum.plot(x='freq_p1', y='comb_mw', ax=ax, c='C2',
                      label=r"+1 $f_{MW}$")
    # ax.set_ylabel("Amplitude (arb. u.)")
    ax.set_xlabel("Binding Energy (GHz)")
    # ax.set_title("Spectrum with " + str(lw) + r" GHz FWHM and $E_s = $"
    #              + str(e*1e-2) + " V/cm")
    return spectrum


def build_SM(color=True):
    """Build the Stark Map with Highlighting"""
    mwf = 18.5
    efld = read_efield()
    elvl = read_elevels()
    hglt = read_highlight()
    # print(efld['efield'])
    # elvl['efield'] = efld['efield'].values
    # hglt['efield'] = efld['efield'].values
    # for i in range(100, 154):
    # for i in range(103, 104):
    plt.figure(figsize=(10, 10))
    for i in range(80, 180):
        # plt.scatter(efld['efield']/100, elvl[i].values, c=hglt[i].values,
        #             cmap='Reds', vmin=0, vmax=0.1, s=0.1)
        if color is True:
            args = {'c': hglt[i].values, 'cmap': 'Reds', 'vmin': 0,
                    'vmax': 0.1, 's': 2}
            plt.scatter(efld['efield']/100, elvl[i].values, **args)
        else:
            args = {'c': 'k', 'lw': 0.5}
            plt.plot(efld['efield']/100, elvl[i].values, **args)
    e0 = elvl.loc[0, 127]
    print(e0)
    for i in [-2, -1, 0, 1, 2]:
        # spread of +/- sideband
        plt.axhline(e0 + i*mwf, c='grey', linestyle='dashed')
    plt.xlabel("Field (V/cm)")
    plt.ylabel("Binding Energy (GHz)")
    if color is True:
        plt.colorbar()
        ax = plt.gca()
        ax.patch.set_facecolor('lightblue')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("StarkMap_fchar.png")
    return hglt


def colortest():
    x = np.linspace(0, 300, 301)
    plt.scatter(x, x, c=x, cmap='Reds', s=1)
    return


def get_from_arc():
    efld = read_efield()
    elvl = read_elevels()
    hglt = read_highlight()
    return efld, elvl, hglt


def scratch():
    efld, elvl, hglt = get_from_arc()
    # for i in range(110, 150):
    # i = 127
    # plt.plot(efld['efield'].values, elvl[i].values)
    # plt.axhline(elvl.iloc[0, i])
    # print(elvl.loc[i].iloc[0])
    # lines = [-4523.10, -4519.60, -4516.18, -4512.74, -4509.34, -4505.95,
    #          -4502.54]
    # print(np.diff(lines))
    # print(np.mean(np.diff(lines)))
    # print(abs(lines[0] - lines[-1]))
    slope, intercept, rvalue, pvalue, stderr = \
        linregress([20, 40, 200], [3.25, 6.64, 32.7])
    print(slope, intercept)
    return


def spect_cal_fig():
    fig, axes = plt.subplots(nrows=4, sharex=True)
    instrs = [[0.3e2, "0.3 V/cm", axes[0]],
              [3.25e2, "3.3 V/cm", axes[1]],
              [6.64e2, "6.4 V/cm", axes[2]],
              [32.7e2, "32.7 V/cm", axes[3]]]
    fmin = -4530
    fmax = -4490
    lw = 0.05  # 50 MHz
    for instr in instrs:
        [e, label, ax] = instr
        build_spectroscopy(e, fmin, fmax, ax, label=label, lw=lw, sbds=False,
                           fstruct=True)
    axes[3].set_ylabel("Signal (arb. u.)")
    axes[3].set_xlim(fmin, fmax)
    fig.tight_layout()
    fig.savefig("ARC_Stark.pdf")
    return


def test_spectroscopy():
    e = 9e2  # 15 V/cm, 1500 V/m
    fmin = -4511 - 18.5*6
    fmax = -4511 + 18.5*6
    fig, ax = plt.subplots()
    lw = 9  # 50 MHz
    spectrum = build_spectroscopy(e, fmin, fmax, ax, label="", lw=lw,
                                  sbds=True, fstruct=True)
    return spectrum


if __name__ == "__main__":
    # hglt = read_highlight()
    # elvl = read_elevels()
    # efld = read_efield()
    # ax = spectrum.plot(x='freq', y='signal')
    # ax.set_xlim(-4535, -4505)
    build_SM(color=False)
    # scratch()
    # colortest()
    # spect_cal_fig()
    # spectrum = test_spectroscopy()
