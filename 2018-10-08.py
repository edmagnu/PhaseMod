# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-10-08


import os
import numpy as np
from scipy.stats import cauchy
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd


def dye_plot(fname, mwf, label, ax):
    data = pd.read_csv(fname, sep='\t', comment="#", index_col=False)
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='f', inplace=True)
    data.plot(x='f', y='sig', label=label, ax=ax)
    return


def mw_sideband_scan(date):
    mwf = 18.5122  # GHz
    e27f = -4511.5
    e27p = -4526.9
    fig, axes = plt.subplots(nrows=3, ncols=2, sharex='row')
    instrs = [["4_freq_dye.txt", "-1 dB", axes[0, 0]],
              ["5_freq_dye.txt", "-10 dB", axes[1, 0]],
              ["6_freq_dye.txt", "MAX", axes[2, 0]],
              ["7_freq_dye.txt", "-1 dB", axes[0, 1]],
              ["8_freq_dye.txt", "-10 dB", axes[1, 1]],
              ["9_freq_dye.txt", "MAX", axes[2, 1]]]
    for instr in instrs:
        [fname, label, ax] = instr
        fname = os.path.join("..", date, fname)
        dye_plot(fname, mwf, label, ax)
        ax.axvline(e27p, color='grey', linestyle='dashed')
        for i in [-2, -1, 0, 1, 2]:
            ax.axvline(e27f + 2*i*mwf, color='grey', linestyle='dashed')
        ax.axhline(0, c='k')
        ax.set_xlabel("Frequency (GHz)")
        ax.set_ylabel("Signal (arb. u.)")
    axes[0, 0].set_title("0 V/cm")
    axes[0, 1].set_title("6.6 V/cm")
    fig.tight_layout()
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


def cavity_resonances(date):
    """Using the dye laser at -180 GHz, the MW f is scanned over the
    cavity resonances, finding center, FWHM, and Q values."""
    fig, axes = plt.subplots(nrows=2, sharex=True)
    folder = os.path.join("..", date)
    instrs = [["1_fscan.txt", axes[0]],
              ["10_fscan.txt", axes[1]]]
    for instr in instrs:
        [fname, ax] = instr
        print("\n", fname)
        fname = os.path.join(folder, fname)
        data, popt = mw_fscan(fname, -1, ax)
    fig.tight_layout()
    return


def step_freq_fit(o, i, f):
    p = np.polyfit(i, f, o)
    fpoly = np.polyval(p, i)
    return fpoly


def diode_scan(fname, ax, label):
    """Display diode scan with polynomial fitted laser frequency."""
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['fpoly'] = step_freq_fit(5, data['i'], data['f'])
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='i', inplace=True)
    data.plot(x='fpoly', y='sig', ax=ax, label=label)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Signal (arb. u.)")
    # fig.savefig("DiodeScan.pdf")
    return


def stark_spectroscopy(date):
    """Plot Diode Laser scans of the stark manifold at different applied (Top -> Bot) Voltages"""
    fig, axes = plt.subplots(nrows=2, sharex=True)
    todolist = [["2_stark_0V.txt", "0 V/cm", axes[0]],
	            ["3_stark_40V.txt", "6.6 V/cm", axes[1]]]
    for todo in todolist:
	    [fname, label, ax] = todo
	    fname = os.path.join("..", date, fname)
	    diode_scan(fname, ax, label)
    fig.tight_layout()
    return


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


def delay_blink(date):
    fname = "14_delay.txt"
    fname = os.path.join("..", date, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    sol = 299792458  # m/s
    n = 1.00029  # Index of refraction of Air
    m = 2.539e-7  # meter / step
    mwf = 18.5096e9*2  # GHz
    wlng = sol/(mwf*n)
    print(wlng)
    data['wlng'] = data['d']*2*m/wlng
    data['wlng'] = data['wlng'] % 1.0
    data.sort_values(by='wlng', inplace=True)
    data = data.rolling(window=5, center=True).mean()
    data['sig'] = data['s'] - data['b']
    data['ref'] = data['r'] - data['b']
    data['nrm'] = data['sig'] / data['ref']
    mask = np.logical_not(np.isnan(data['r']))
    mask = mask & np.logical_not(np.isinf(data['r']))
    data[mask].plot(x='wlng', y='r')
    return


if __name__ == "__main__":
    date = "2018-10-08"
    # limit(date)
    # cavity_resonances(date)
    # mwion_scan(date)
    # svf_from_cav_res(date)
    # node_scan()
    # dye_mwion(date)
    # stark_spectroscopy(date)
    # steps_wvlg(18512.2e6*2)  # Hz
    # mw_sideband_scan(date)
    delay_blink(date)
    plt.show()
