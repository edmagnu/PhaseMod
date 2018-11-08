# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 01:01:17 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-11-02


def dye_qs_lim(date):
    import os
    import pandas as pd
    fname = "1_lim.txt"
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


def mw_res(date):
    import os
    import numpy as np
    import pandas as pd
    fname = "4_mwres.txt"
    fname = os.path.join("..", date, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data.sort_values(by='f', inplace=True)
    data['s_rm'] = data['s'].rolling(window=9, center=True).mean()
    ax = data.plot(x='f', y='s_rm')
    center = -12
    for freq in (np.array([-2, -1, 0, 1, 2])*18.5*2 + center):
        ax.axvline(freq, c='grey', ls='dashed')
    return


def cavity_resonances(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    folder = os.path.join("..", date)
    norm = False
    instrs = [
              ["2_fscan.txt", -1],
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


def delays(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    instrs = [
              ["5_delay.txt", "19 dB MW, 32.5 dB PM", 1],
              ["6_delay.txt", "19 dB MW, 30 dB PM", 0],
              ["7_delay.txt", "19 dB MW, 40 dB PM", 2]
             ]
    # fname = "6_delay.txt"
    # label = "0 V/cm Static, 19 dB MW"
    mwf = 18.5101e9*2  # Hz after doubler
    fig, axes = plt.subplots(nrows=len(instrs))
    for instr in instrs:
        [fname, label, i] = instr
        ax = axes[i]
        fname = os.path.join("..", date, fname)
        tk.delay_short(fname, mwf, ax)
        ax.set_title(label)
    fig.tight_layout()
    return


def bessels(date):
    import toolkit as tk
    aoff = 480
    zero = 0
    a0 = 432
    a1 = 22.8
    fit1, fit2 = tk.gba_01(aoff, a0, a1, zero, quiet=True)
    print(fit1, fit2, (fit1 + fit2)/2)
    return


def scratch(date):
    import toolkit as tk
    mwf = 18.5101e9*2
    print(tk.wlen_to_step(0.26 + 6, mwf))
    print(tk.wlen_to_step(0.00824283455081 + 6.5, mwf))
    print(tk.wlen_to_step(0.00824283455081 + 6, mwf))
    return


def main():
    date = "2018-11-02"
    # dye_qs_lim(date)
    # cavity_resonances(date)
    # mw_res(date)
    delays(date)
    # bessels(date)
    # scratch(date)
    return


if __name__ == "__main__":
    main()
