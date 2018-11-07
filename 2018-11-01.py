# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 17:22:57 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-11-01

def cavity_resonances(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    folder = os.path.join("..", date)
    norm = False
    instrs = [
              ["1_fscan.txt"],
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


def minmax_step(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    fname = "11_delay_diode.txt"
    fname = os.path.join("..", date, fname)
    mwf = 18.5119e9*2  # Hz after doubler.
    fig, ax = plt.subplots()
    tk.delay_short(fname, mwf, ax)
    return


def delays(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    instrs = [
              ["12_delay_diode.txt", "27f + 0, PM=0.5", 0, 0],
              ["11_delay_diode.txt", "27f + 0, PM=1.1", 1, 0],
              ["9_delay_diode.txt", "27f + 1, PM=0.5", 0, 1],
              ["10_delay_diode.txt", "27f + 1, PM=1.1", 1, 1]
             ]
    mwf = 18.5110e9*2  # Hz after doubler
    fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
    for instr in instrs:
        [fname, label, i, j] = instr
        ax = axes[i, j]
        fname = os.path.join("..", date, fname)
        tk.delay_short(fname, mwf, ax)
        ax.set_title(label)
    fig.tight_layout()
    fig.savefig("2018-11-01-sideband.pdf")
    return


def quickscan_import(fname):
    import pandas as pd
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['t'] = data.index.values
    data['t'] = data['t'].max() - data['t']
    data.sort_values(by='t', inplace=True)
    data['d'] = data['s'] - data['r']
    for key in ['d', 's', 'r']:
        data[key] = -data[key]
    return data


def quickscan_plot(data, axes):
    data.plot(x='t', y='d', ax=axes[0])
    data.plot(x='t', y='s', ax=axes[1])
    data.plot(x='t', y='r', ax=axes[2])
    axes[0].set_ylabel("On - Off")
    axes[1].set_ylabel("PM On")
    axes[2].set_ylabel("PM Off")
    return


def quickscan(date):
    import os
    import matplotlib.pyplot as plt
    import pandas as pd
    # Phase = 0
    fname = os.path.join("..", date, "4_freq_diode_PMBlink.txt")
    data = quickscan_import(fname)
    data1 = data.copy()
    fig, axes = plt.subplots(nrows=6, sharex=True,  figsize=(4, 6))
    quickscan_plot(data, axes[[0, 1, 2]])
    # Phase = pi
    fname = os.path.join("..", date, "5_freq_diode_PMBlink.txt")
    data = quickscan_import(fname)
    data2 = data.copy()
    quickscan_plot(data, axes[[3, 4, 5]])
    for ax in axes:
        ax.legend().remove()
    axes[0].set_title(r"Phase = 0")
    axes[3].set_title(r"Phase = $\pi$")
    axes[-1].set_xlabel(r"Laser Frequency (Blue $\rightarrow$)")
    fig.tight_layout()
    # fig.savefig("2018-11-01-SlopeDiff37dB_Individual.pdf")
    # Master Diff
    fig, axes = plt.subplots(nrows=3, sharex=True, figsize=(4, 6))
    datam = pd.DataFrame()
    datam['t'] = data1['t']
    datam['s'] = data1['s']
    datam['r'] = data2['s']
    datam['d'] = datam['s'] - datam['r']
    quickscan_plot(datam, axes)
    for ax in axes:
        ax.legend().remove()
    axes[1].set_ylabel(r"Phase = 0")
    axes[2].set_ylabel(r"Phase = $\pi$")
    axes[0].set_ylabel(r"$0 - \pi$")
    axes[-1].set_xlabel(r"Laser Frequency (Blue $\rightarrow$)")
    fig.tight_layout()
    # fig.savefig("2018-11-01-SlopeDiff37dB_Both.pdf")
    return


def bessels(date):
    import toolkit as tk
    aoff = 80.8
    zero = 0
    a0 = 68.0
    a1 = 5.4
    fit1, fit2 = tk.gba_01(aoff, a0, a1, zero, quiet=True)
    print(fit1, fit2, (fit1 + fit2)/2)
    return


def main():
    date = "2018-11-01"
    # cavity_resonances(date)
    # minmax_step(date)
    # quickscan(date)
    delays(date)
    # bessels(date)
    return


if __name__ == "__main__":
    main()

