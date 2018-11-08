# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 16:55:49 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-11-02

def dye_qs_lim(date):
    import os
    import pandas as pd
    fname = "11_lim.txt"
    fname = os.path.join("..", date, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data.sort_values(by='f', inplace=True)
    data['s_rm'] = data['s'].rolling(window=9, center=True).mean()
    ax = data.plot(x='f', y='s_rm')
    hi_win = [-100, -50]
    lo_win = [10, 20]
    lo = data['s_rm'][(data['f'] > lo_win[0]) & (data['f'] < lo_win[1])].mean()
    hi = data['s_rm'][(data['f'] > hi_win[0]) & (data['f'] < hi_win[1])].mean()
    ax.axhline(lo, c='k')
    ax.axhline(hi, c='k')
    ax.axhline((lo + hi)/2, c='k')
    ax.legend().remove()
    return


def cavity_resonances(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    folder = os.path.join("..", date)
    norm = False
    instrs = [
              ["7_fscan.txt", -1],
             ]
    fig, axes = plt.subplots(nrows=len(instrs))
    for iax, instr in enumerate(instrs):
        [fname, d] = instr
        if len(instrs) > 1:
            ax = axes[iax]
        else:
            ax = axes
        print("\n", fname)
        fname = os.path.join(folder, fname)
        data, popt = tk.mw_fscan(fname, d , ax, norm=norm)
    fig.tight_layout()
    return


def mw_res(date):
    import os
    import numpy as np
    import  matplotlib.pyplot as plt
    import pandas as pd
    instrs = [
              ["8_mwres.txt", "29 dB", 0],
              ["7_mwres.txt", "20 dB", 1],
              ["9_mwres.txt", "14 dB", 2],
              ["10_mwres.txt", "9 dB", 3]
             ]
    # fname = "7_mwres.txt"
    fig, axes = plt.subplots(nrows=len(instrs), sharex=True, sharey=True,
                             figsize=(6,8))
    for instr in instrs:
        [fname, label, i] = instr
        ax = axes[i]
        fname = os.path.join("..", date, fname)
        data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
        data.sort_values(by='f', inplace=True)
        data['s_rm'] = data['s'].rolling(window=9, center=True).mean()
        data.plot(x='f', y='s_rm', ax=ax, label=label)
        center = -12
        for freq in (np.array([-2, -1, 0, 1, 2])*18.5*2 + center):
            ax.axvline(freq, c='grey', ls='dashed')
    for ax in axes:
        ax.set_ylabel("Signal")
        ax.set_xlabel("Frequency (GHz)")
    fig.tight_layout()
    fig.savefig("2018-11-03-mwres.pdf")
    return


def delay_short(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    fname = "3_delay.txt"
    label = "MW = 19.0 dB, PM = 35.0 dB"
    fig, ax = plt.subplots()
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18.5102e9*2  # Hz after doubler.
    fold = 1
    blink = False
    fname = os.path.join("..", date, fname)
    data, popt, pcov = tk.delay_plot(fname, xkey, ykey, ykey2, mwf, nave, ax,
                                     label, fold=fold, blink=blink)
    obs = {"mw": 9, "pm": 38, "a0": popt[0], "a1": popt[1], "a2": popt[3],
               "a3": popt[5], "a4": popt[7]}
    stepmin = tk.wlen_to_step(popt[2]+6, mwf)
    stepmax = tk.wlen_to_step(popt[2]+6.5, mwf)
    print("step_min = ", stepmin)
    print("step_max = ", stepmax)
    ax.axvline(tk.step_to_wlen(stepmin, mwf)%1, c='grey', ls='dashed')
    ax.axvline(tk.step_to_wlen(stepmax, mwf)%1, c='grey', ls='dashed')
    return


def delays(date, instrs, figsize):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    # instrs = [
              # ["12_delay.txt", "19 dB MW, 32.5 dB PM, 0 mV", 0],
              # ["13_delay.txt", "19 dB MW, 32.5 dB PM, +85 mV", 2],
              # ["14_delay.txt", "19 dB MW, 32.5 dB PM, +46 mV", 1],
              # ["14_delay.txt", "19 dB MW, 32.5 dB PM, +46 mV", 0],
              # ["16_delay.txt", "19 dB MW, 36 dB PM, +46 mV", 1],
              # ["15_delay.txt", "19 dB MW, 39 dB PM, +46 mV", 2],
              # ["16_delay.txt", "19 dB MW, 36 dB PM, +46 mV", 1],
              # ["17_delay.txt", "19 dB MW, 36 dB PM, +92 mV", 3],
              # ["18_delay.txt", "19 dB MW, 36 dB PM, +69 mV", 2],
              # ["19_delay.txt", "19 dB MW, 36 dB PM, 0 mV", 0]
               # ["12_delay.txt", "19 dB MW, 1.4 PM, 0 mV", 0],
               # ["13_delay.txt", "19 dB MW, 1.4 PM, +85 mV", 2],
               # ["14_delay.txt", "19 dB MW, 1.4 PM, +46 mV", 1],
               # ["20_delay.txt", "19 dB MW, 32.5 dB PM, +80 mV", 3],
               # ["21_delay.txt", "19 dB MW, 32.5 dB PM, +120 mV", 4],
               # ["22_delay.txt", "19 dB MW, 1.4 PM, 0 mV, +1", 1],
               # ["12_delay.txt", "19 dB MW, 1,4 PM, 0 mV, 0", 0],
               # ["23_delay.txt", "19 dB MW, 1.4 PM, 40 mV, +1", 2],
               # ["24_delay.txt", "19 dB MW, 1.4 pm, 80 mV, +1", 2],
               # ["25_delay.txt", "19 dB MW, 1.4 pm, 40 mV, +1", 5],
               # ["26_delay.txt", "19 dB MW, 2.4 pm, 40 mV, +1", 3],
               # ["27_delay.txt", "19 dB MW, 2.4 pm, 0 mV, +1", 4]
               # ["25_delay.txt", "19 dB MW, 1.4 pm, 40 mV, +1", 1],
               # ["26_delay.txt", "19 dB MW, 2.4 pm, 40 mV, +1", 2],
               # ["28_delay.txt", "19 dB MW, 1.0 pm, 40 mV, +1", 0]
               # ["12_delay.txt", "19 dB MW, 1,4 PM, 0 mV, 0", 1],
               # ["29_delay.txt", "19 dB MW, 1.4 pm, 0 mV, -1", 0],
               # ["29_delay.txt", "19 dB MW, 1.4 PM, 0 mV, -1", 0],
               # ["30_delay.txt", "19 dB MW, 1.4 PM, 40 mV, -1", 2],
               # ["32_delay.txt", "19 dB MW, 1.0 PM, 40 mV, -1", 1],
               # ["33_delay.txt", "19 dB MW< 2.4 PM, 40 mV, -1", 3]
               # ["31_delay.txt", "19 dB MW, 1.4 PM, 120 mV, -1", 2],
             # ]
    mwf = 18.5106e9*2  # Hz after doubler
    axlen = len(instrs)
    if axlen == 1: axlen = 2
    fig, axes = plt.subplots(nrows=axlen, sharex=True, sharey=False,
                             figsize=figsize)
    for instr in instrs:
        [fname, label, i] = instr
        ax = axes[i]
        fname = os.path.join("..", date, fname)
        tk.delay_short(fname, mwf, ax)
        ax.legend([label])
    fig.tight_layout()
    return fig, axes


def delay_instrs(date):
    instrs = [
              ["29_delay.txt", "19 dB MW, 1.4 PM, 0 mV, -1", 0],
              ["30_delay.txt", "19 dB MW, 1.4 PM, 40 mV, -1", 2],
              ["32_delay.txt", "19 dB MW, 1.0 PM, 40 mV, -1", 1],
              ["33_delay.txt", "19 dB MW< 2.4 PM, 40 mV, -1", 3]
             ]
    fig, axes = delays(date, instrs, figsize=(6, 8))
    axes[0].set_title("-1 Sideband, Changing PM")
    fig.savefig("2018-11-03-m1sbnd.pdf")
    instrs = [
              ["22_delay.txt", "19 dB MW, 1.4 PM, 0 mV, +1", 0],
              ["23_delay.txt", "19 dB MW, 1.4 PM, 40 mV, +1", 2],
              ["26_delay.txt", "19 dB MW, 2.4 pm, 40 mV, +1", 3],
              ["28_delay.txt", "19 dB MW, 1.0 pm, 40 mV, +1", 1]
             ]
    fig, axes = delays(date, instrs, figsize=(6,8))
    axes[0].set_title("+1 Sidenabnd, Chaginging PM")
    fig.savefig("2018-11-03-0sbnd.pdf")
    instrs = [
              ["12_delay.txt", "19 dB MW, 1.4 pm, 0 mV", 0],
              ["14_delay.txt", "19 dB MW, 1.4 pm, +46 mV", 1],
              ["15_delay.txt", "19 dB MW, 1.0 dB PM, +46 mV", 2],
             ]
    fig, axes = delays(date, instrs, figsize=(6,8))
    axes[0].set_title("0th Sidenabnd, Chaginging PM")
    fig.savefig("2018-11-03-p1sbnd.pdf")
    return


def bessels(date):
    import toolkit as tk
    aoff = 880
    zero = 0
    a0 = 560
    a1 = 152
    fit1, fit2 = tk.gba_01(aoff, a0, a1, zero, quiet=True)
    print(fit1, fit2, (fit1 + fit2)/2)
    return


def scratch(date):
    from scipy.special import jv
    import toolkit as tk
    phase = 0.2
    mwf = 18.5106e9*2
    print(tk.wlen_to_step(phase + 6, mwf))
    print(tk.wlen_to_step(phase + 6.5, mwf))
    print(jv(0, 1)**2*944)
    return


def main():
    date = "2018-11-03"
    mw_res(date)
    # delay_short(date)
    # dye_qs_lim(date)
    # cavity_resonances(date)
    # delay_instrs(date)
    # bessels(date)
    # scratch(date)
    return

if __name__ == "__main__":
    main()
