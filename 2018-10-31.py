# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 12:06:30 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-10-31


def cavity_resonances(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    folder = os.path.join("..", date)
    norm = False
    instrs = [
              ["1_fscan.txt"],
              ["3_fscan.txt"]
             ]
    fig, axes = plt.subplots(nrows=len(instrs))
    for iax, instr in enumerate(instrs):
        [fname] = instr
        if len(instrs) > 1:
            ax = axes[iax]
        else:
            ax = axes
        print("\n", fname)
        fname = os.path.join(folder, fname)
        data, popt = tk.mw_fscan(fname, 1, ax, norm=norm)
    fig.tight_layout()
    return


def delay_short(date):
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import toolkit as tk
    fname = "6_delay_diode.txt"
    label = "MW = 9.0 dB, PM = 38.0 dB"
    fig, ax = plt.subplots()
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18.5119e9*2  # Hz after doubler.
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


def quickscan_cauchy(date, bkgnd):
    import os
    import matplotlib.pyplot as plt
    import pandas as pd
    import toolkit as tk
    fig, ax = plt.subplots()
    fname = os.path.join("..", date, "0_reference.txt")
    data = pd.read_csv(fname, sep="\t", index_col=False, names='s')
    data['sig'] = data['s'] - bkgnd
    trim = [600, 750]
    mask = range(trim[0], trim[1])
    data.iloc[mask].plot(y='sig', ax=ax)
    x = data.iloc[mask].index
    y = data.iloc[x]['sig'].values
    popt = tk.cauchy_fit(x, y, -1)
    data['fit'] = pd.Series(data=tk.cauchy_model(x, *popt), index=x)
    data.iloc[mask].plot(y='fit', ax=ax)
    return popt


def quickscan_background(date):
    import os
    import pandas as pd
    fname = os.path.join("..",date, "0_background.txt")
    data = pd.read_csv(fname, sep="\t", index_col=False, names="s")
    value = data['s'].mean()
    print("background = ", value)
    return value


def quickscan_peak(date):
    import toolkit as tk
    bkgnd = quickscan_background(date)
    popt = quickscan_cauchy(date, bkgnd)
    peak = tk.cauchy_model(popt[1], *popt)
    print("\npeak = ", abs(peak), "\n")
    return


def quickscan_smooth(fname, bkgnd):
    import pandas as pd
    data = pd.read_csv(fname, sep="\t", index_col=False, names="s")
    data['sig'] = data['s'] - bkgnd
    data['rm'] = data['sig'].rolling(window=15, center=True).mean()
    return data


def quickscans(date):
    import os
    bkgnd = quickscan_background(date)
    fname = os.path.join("..", date, "0_signal.txt")
    data = quickscan_smooth(fname, bkgnd)
    ax = data.plot(y='sig', c='C1', marker='.')
    data.plot(y='rm', c='C0', lw=3, ax=ax)
    fname = os.path.join("..", date, "0_reference.txt")
    data = quickscan_smooth(fname, bkgnd)
    ax = data.plot(y='sig', c='C1', marker='.')
    data.plot(y='rm', c='C0', lw=3, ax=ax)
    return


def quickscan_blink(date):
    import os
    import matplotlib.pyplot as plt
    import pandas as pd
    fname = os.path.join("..", date, "4_quickscan_mwblink.txt")
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['sig'] = -(data['s'] - data['b'])
    data['ref'] = -(data['r'] - data['b'])
    data['sig_rm'] = data['sig'].rolling(window=9, center=True).mean()
    data['ref_rm'] = data['ref'].rolling(window=9, center=True).mean()
    data['t'] = data.index.values
    data['frel'] = data['t'].max() - data['t']
    data.sort_values(by='frel', inplace=True)
    fig, axes = plt.subplots(nrows=2, sharex=True, sharey=True)
    data.plot.scatter(x='frel', y='sig', ax=axes[0], marker='.', c='lightgrey')
    data.plot.scatter(x='frel', y='ref', ax=axes[1], marker='.', c='lightgrey')
    data.plot(x='frel', y='sig_rm', ax=axes[0], c='C0', label="MW On")
    data.plot(x='frel', y='ref_rm', ax=axes[1], c='C1', label="MW Off")
    axes[1].set_xlabel("Relative Laser Frequency")
    axes[0].set_ylabel("Signal")
    axes[1].set_ylabel("Signal")
    axes[0].axhline(0, c='k')
    axes[1].axhline(0, c='k')
    return


def MWDel_Blink(date):
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import toolkit as tk
    cal = mwonoff_cal(date)
    fname = os.path.join("..", date, "7_MWDelayBlink.txt")
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['s1nrm'] = (data['son1'] - data['b']) / (data['soff1'] - data['b'])
    data['s2nrm'] = (data['son2'] - data['b']) / (data['soff2'] - data['b'])
    data['s1nrm'] = data['s1nrm']*cal
    data['s2nrm'] = data['s2nrm']*cal
    for i in data.index:
        obs = data.iloc[i]
        fit0, fit1 = tk.gba_01(obs['aoff'], obs['a0'], obs['a1'], obs['zero'],
                               quiet=True)
        data.at[i, 'fit0'] = fit0
        data.at[i, 'fit1'] = fit1
    # Hard code the zero, it doesn't like it
    data.at[0, 'fit0'] = 0
    data.at[0, 'fit1'] = 0
    data['pm'] = (data['fit0'] + data['fit1'])/2
    # Over 2.4, it gets confused, by eye correction
    data.at[11, 'pm'] = 2.5
    data.at[12, 'pm'] = 2.39
    data.sort_values(by='pmatt', inplace=True)
    print(data)
    # Fig of PM vs. Signals
    fig, ax = plt.subplots()
    data.plot(x='pm', y='s1nrm', ax=ax, marker='o', label=r"$\phi = 0$")
    data.plot(x='pm', y='s2nrm', ax=ax, marker='o', label=r"$\phi = \pi$")
    ax.set_xlabel("PM Index")
    ax.set_ylabel("Norm. Signal")
    ax.set_ylim(0, 1.4)
    ax.grid(b=True)
    fig.tight_layout()
    # Fig of PM Attn vs. Signals
    fig, ax = plt.subplots()
    data.plot(x='pmatt', y='s1nrm', ax=ax, marker='o')
    data.plot(x='pmatt', y='s2nrm', ax=ax, marker='o')
    fig.tight_layout()
    # Fig of PM Attn vs. PM
    fig, ax = plt.subplots()
    data.plot(x='pmatt', y='pm', ax=ax, marker='o')
    fig.tight_layout()
    return data


def mwonoff_cal(date):
    import os
    import pandas as pd
    fname = os.path.join("..", date, "8_peak_cal.txt")
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    b = data['b'].mean()
    on = data['on'].mean()
    off = data['off'].mean()
    cal = (on-b)/(off-b)
    return cal


def bessels(date):
    import toolkit as tk
    aoff = 102.0
    zero = 3.2
    a0 = 88.8
    a1 = 8.0
    tk.gba_01(aoff, a0, a1, zero)
    return


def scratch(date):
    import os
    import numpy as np
    import scipy.special as sp
    import matplotlib.pyplot as plt
    import pandas as pd
    fname = os.path.join("..", date, "8_peak_cal.txt")
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    b = data['b'].mean()
    on = data['on'].mean()
    off = data['off'].mean()
    cal = (on-b)/(off-b)
    print(data)
    print(cal)
    return


def main():
    date = "2018-10-31"
    # quickscan_peak(date)
    # cavity_resonances(date)
    # bessels(date)
    # delay_short(date)
    # quickscans(date)
    # quickscan_peak(date)
    # quickscan_blink(date)
    MWDel_Blink(date)
    # scratch(date)
    return
    

if __name__ == "__main__":
    main()
