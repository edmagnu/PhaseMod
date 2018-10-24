# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 21:18:27 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-10-23


def cavity_resonances(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    """Using the dye laser at -180 GHz, the MW f is scanned over the
    cavity resonances, finding center, FWHM, and Q values."""
    fig, axes = plt.subplots(nrows=2, sharex=True)
    folder = os.path.join("..", date)
    norm = False
    instrs = [
              ["2_fscan.txt", axes[0]],
              ["17_fscan.txt", axes[1]]
             ]
    for instr in instrs:
        [fname, ax] = instr
        print("\n", fname)
        fname = os.path.join(folder, fname)
        data, popt = tk.mw_fscan(fname, 1, ax, norm=norm)
    fig.tight_layout()
    return


def diode_27f(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    fname = "1_freq_diode.txt"
    fname = os.path.join("..", date, fname)
    data = tk.diode_scan(fname)
    fig, ax = plt.subplots()
    tk.diode_plot(data, ax, None)
    return


def find_delay_mins(date):
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    import toolkit as tk
    instrs = [
              # ["3_delay_diode.txt", "MW = -10 dB", 0],
              [ "4_delay_diode.txt", "MW = - 6 dB", 0],
              [ "6_delay_diode.txt", "MW = - 8 dB", 1],
              [ "7_delay_diode.txt", "MW = -10 dB", 2],
              [ "5_delay_diode.txt", "MW = -12 dB", 3],
              [ "8_delay_diode.txt", "MW = -16 dB", 4],
              [ "9_delay_diode.txt", "MW = -20 dB", 5],
              ["10_delay_diode.txt", "MW = -26 dB", 6],
              ["11_delay_diode.txt", "MW = -32 dB", 7]
              # ["12_delay_diode.txt", "MW = -38 dB", 8]
             ]
    fig, axes = plt.subplots(nrows=len(instrs), sharex=True, sharey=True)
    xkey = 'd'
    ykey = 'nsig_rm'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18.5096e9*2  # Hz after doubler.
    fold = 1
    blink = False
    smins = []
    smaxs = []
    for instr in instrs:
        [fname, label, ax] = instr
        ax = axes[ax]
        fname = os.path.join("..", date, fname)
        data = tk.delay_load(fname)
        data, popt, pconv = tk.transform_delay(data, mwf, nave, xkey, fold,
                                               blink)
        data.plot(x='d', y='nsig', ax=ax, label=label)
        data.plot(x='d', y='fit', ax=ax, label="fit")
        step_min = tk.wlen_to_step(6 + popt[2], mwf)
        smins = smins + [step_min]
        step_max = tk.wlen_to_step(6.5 + popt[2], mwf)
        smaxs = smaxs + [step_max]
        print("\n", fname, "\t", label, "\n", step_min, "\t", step_max, "\n",
              tk.step_to_wlen(step_min, mwf), "\t",
              tk.step_to_wlen(step_max, mwf), "\n", popt[1])
        for step in [step_min, step_max]:
            ax.axvline(step, c='k', ls='solid', lw=2)
    for ax in axes:
        for step in smins:
            ax.axvline(step, c='grey', ls='dashed')
        for step in smaxs:
            ax.axvline(step, c='grey', ls='dashed')
    sm_m = np.mean(smins)
    sm_s = np.std(smins)
    print("\n", "mean min", "\n", sm_m, " +/- ", sm_s, "\n",
          tk.step_to_wlen(sm_m, mwf), " +/- ",
          tk.step_to_wlen(sm_s, mwf))
    return


def turning(date):
    import os
    import matplotlib.pyplot as plt
    import pandas as pd
    import toolkit as tk
    fname = "13_turning.txt"
    fname = os.path.join("..", date, fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['nsig'] = (data['sig'] - data['0'])/(data['norm'] - data['0'])
    for i in data.index:
        coeff = tk.get_bessel_arg(108, data.loc[i, 'val'], 3, quiet=True)
        data.loc[i, 'coeff'] = coeff
    fig, ax = plt.subplots()
    data.plot.scatter(x='mwa', y='pm', ax=ax)
    ax.set_xlim(-35, 0)
    ax.set_xlabel(r"MW Attenuation ($P_{0,MW}$ - x dB)")
    ax.set_ylabel("PM Attenuation ($P_{0,PM}$ - y dB)")
    ax.set_title("PM Turning Point")
    fig.tight_layout()
    fig.savefig("2018-10-23-Turning.pdf")
    return data


def dbs_min(date):
    import os
    import matplotlib.pyplot as plt
    import pandas as pd
    import toolkit as tk
    instrs = [
              ["14_phase_min.txt", "MW = $P_{0,MW}$ - 9 dB", "C0", "o"],
              ["15_phase_min.txt", "MW = $P_{0,MW}$ - 15 dB", "C1", "X"],
              ["16_phase_min.txt", "MW = $P_{0,MW}$ - 21 dB", "C2", "^"]
             ]
    # fname = "14_phase_min.txt"
    fig, ax = plt.subplots()
    for instr in instrs:
        [fname, label, color, marker] = instr
        fname = os.path.join("..", date, fname)
        data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
        data.sort_values(by='pm', inplace=True)
        data['nsig'] = (data['sig'] - data['0'])/(data['norm'] - data['0'])
        data.plot(x='pm', y='nsig', marker=marker, label=label, c=color, ax=ax)
    ax.legend()
    ax.set_xlim(-51, -28)
    ax.set_xlabel(r"PM Attenuation ($P_{0,PM}$ - x dB)")
    ax.set_ylabel("Normalized Signal")
    ax.set_title("Minimum vs. PM")
    fig.tight_layout()
    fig.savefig("2018-10-23-Minimum.pdf")
    return


def main():
    import toolkit as tk
    date = "2018-10-23"
    # cavity_resonances(date)
    # diode_27f(date)
    # find_delay_mins(date)
    turning(date)
    dbs_min(date)
    # tk.get_bessel_arg(108, 12.8, 3.0, quiet=False)
    return


if __name__ == "__main__":
    main()
