# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 22:31:32 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-10-24


def cavity_resonances(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    """Using the dye laser at -180 GHz, the MW f is scanned over the
    cavity resonances, finding center, FWHM, and Q values."""
    folder = os.path.join("..", date)
    norm = False
    instrs = [
              ["1_fscan.txt"],
              ["22_fscan.txt"]
             ]
    fig, axes = plt.subplots(nrows=len(instrs))
    for iax, instr in enumerate(instrs):
        [fname] = instr
        ax = axes[iax]
        print("\n", fname)
        fname = os.path.join(folder, fname)
        data, popt = tk.mw_fscan(fname, 1, ax, norm=norm)
    fig.tight_layout()
    return


def bessel(sb0, sb1, norm, zero):
    import toolkit as tk
    tk.get_bessel_arg(norm, sb0, zero, quiet=False, order=0)
    print()
    tk.get_bessel_arg(norm, sb1, zero, quiet=False, order=1)
    return


def delay_short_9(date):
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import toolkit as tk
    instrs = [
              [ "10_delay_diode.txt", "PM = MAX", -70],
              [ "9_delay_diode.txt", "PM = -48.5 dB", -48.5],
              [ "8_delay_diode.txt", "PM = -45.5 dB", -45.5],
              [ "7_delay_diode.txt", "PM = -42.5 dB", -42.5],
              [ "6_delay_diode.txt", "PM = -39.5 dB", -39.5],
              [ "4_delay_diode.txt", "PM = -36.5 dB", -36.5],
              [ "2_delay_diode.txt", "PM = -33.5 dB", -33.5],
              [ "3_delay_diode.txt", "PM = -30.5 dB", -30.5],
              [ "21_delay_diode.txt", "PM = -27.5 dB", -28.5],
              [ "5_delay_diode.txt", "PM = -27.5 dB", -27.5],
             ]
    fig, axes = plt.subplots(nrows=len(instrs), sharex=True, sharey=True)
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18.5099e9*2  # Hz after doubler.
    fold = 1
    blink = False
    fits = pd.DataFrame()
    # Delays figure
    for iax, instr in enumerate(instrs):
        [fname, label, pm] = instr
        ax = axes[iax]
        fname = os.path.join("..", date, fname)
        data, popt, pcov = tk.delay_plot(fname, xkey, ykey, ykey2, mwf, nave,
                                         ax, label, fold=fold, blink=blink)
        # data = tk.delay_load(fname)
        # data, popt, pcov = tk.transform_delay(data, mwf, nave, xkey, fold,
        #                                       blink)
        obs = {"mw": 9, "pm": pm, "a0": popt[0], "a1": popt[1], "a2": popt[3],
               "a3": popt[5], "a4": popt[7]}
        fits = fits.append(obs, ignore_index=True)
        ax.legend().remove()
    # Amplitudes Figure
    instrs = ["a0", "a1", "a2", "a3", "a4"]
    for instr in instrs:
        fits["p_" + instr] = np.abs(fits[instr])
    fig, ax = plt.subplots()
    for i, instr in enumerate(instrs):
        fits.plot(x='pm', y='p_' + instr, ax=ax)
    ax.set_ylim(0,)
    fig.tight_layout()
    fig.savefig("2018-10-24-amps_9db.pdf")
    return


def delay_short_21(date):
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import toolkit as tk
    instrs = [
              [ "20_delay_diode.txt", "PM = MAX", -70],
              [ "19_delay_diode.txt", "PM = 48.5", -48.5],
              [ "18_delay_diode.txt", "PM = 45.5", -45.5],
              [ "17_delay_diode.txt", "PM = 42.5", -42.5],
              [ "16_delay_diode.txt", "PM = 39.5", -39.5],
              [ "15_delay_diode.txt", "PM = 36.5", -36.5],
              [ "14_delay_diode.txt", "PM = 33.5", -33.5],
              [ "13_delay_diode.txt", "PM = 31.5", -30.5],
              [ "11_delay_diode.txt", "PM = 28.5", -28.5],
              [ "12_delay_diode.txt", "PM = 27.5", -27.5],
             ]
    fig, axes = plt.subplots(nrows=len(instrs), sharex=True, sharey=True)
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18.5099e9*2  # Hz after doubler.
    fold = 1
    blink = False
    fits = pd.DataFrame()
    for iax, instr in enumerate(instrs):
        [fname, label, pm] = instr
        ax = axes[iax]
        fname = os.path.join("..", date, fname)
        data, popt, pcov = tk.delay_plot(fname, xkey, ykey, ykey2, mwf, nave,
                                         ax, label, fold=fold, blink=blink)
        obs = {"mw": 9, "pm": pm, "a0": popt[0], "a1": popt[1], "a2": popt[3],
               "a3": popt[5], "a4": popt[7]}
        fits = fits.append(obs, ignore_index=True)
        ax.legend().remove()
    # Amplitudes Figure
    instrs = ["a0", "a1", "a2", "a3", "a4"]
    for instr in instrs:
        fits["p_" + instr] = np.abs(fits[instr])
    fig, ax = plt.subplots()
    for i, instr in enumerate(instrs):
        fits.plot(x='pm', y='p_' + instr, ax=ax)
    ax.set_ylim(0,)
    fig.tight_layout()
    fig.savefig("2018-10-24-amps_21db.pdf")
    return


def delay_mock(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18.5099e9*2  # Hz after doubler.
    fold = 1
    blink = False
    instrs = [
              ["5_delay_diode.txt", 3, 0, "MW -9, PM -27.5"],
              ["12_delay_diode.txt", 3, 1, "MW -21, PM -27.5"],
              # ["21_delay_diode.txt", 2, 0, "MW -9, PM -28.5"],
              # ["11_delay_diode.txt", 2, 1, "MW -21, PM -28.5"],
              ["3_delay_diode.txt", 2, 0, "MW -9, PM -30.5"],
              ["13_delay_diode.txt", 2, 1, "MW -21, PM -30.5"],
              ["2_delay_diode.txt", 1, 0, "MW - 9, PM -33.5"],
              ["14_delay_diode.txt", 1, 1, "MW - 21, PM -33.5"],
              ["4_delay_diode.txt", 0, 0, "MW - 9, PM - 36.5"],
              ["15_delay_diode.txt", 0, 1, "MW - 21, PM - 36.5"],
              # ["6_delay_diode.txt", 0, 0, "MW - 9, PM - 39.5"],
              # ["16_delay_diode.txt", 0, 1, "MW - 21 , PM - 39.5"],
              # ["7_delay_diode.txt", 0, 0, "MW - 9, PM - 42.5"],
              # ["17_delay_diode.txt", 0, 1, "MW - 21, PM - 42.5"]
             ]
    fig, axes = plt.subplots(nrows=4, ncols=2, sharex=True, sharey=True)
    for instr in instrs:
        [fname, i, j, label] = instr
        fname = os.path.join("..", date, fname)
        ax = axes[i, j]
        data, popt, pcov = tk.delay_plot(fname, xkey, ykey, ykey2, mwf, nave,
                                         ax, label, fold=fold, blink=blink)
    return


def delay_pretty(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18.5097e9*2  # Hz after doubler.
    fold = 1
    blink = False
    instrs = [
              ["22_delay_diode.txt", 4, 0, "MW -9, PM -27.5"],
              [os.path.join("..", "2018-10-25", "8_delay_diode.txt"),
               3, 0, "MW -9, PM -28.2"],
              ["23_delay_diode.txt", 2, 0, "MW -9, PM -30.5"],
              ["24_delay_diode.txt", 1, 0, "MW -9, PM -33.5"],
              ["25_delay_diode.txt", 0, 0, "MW -9, PM -36.5"],
              ["26_delay_diode.txt", 4, 1, "MW -21, PM -27.5"],
              [os.path.join("..", "2018-10-25", "7_delay_diode.txt"),
               3, 1, "MW -21, PM -28.2"],
              ["27_delay_diode.txt", 2, 1, "MW -21, PM -30.5"],
              ["28_delay_diode.txt", 1, 1, "MW -21, PM -33.5"],
              ["29_delay_diode.txt", 0, 1, "MW -21, PM -36.5"],
             ]
    fig, axes = plt.subplots(nrows=5, ncols=2, sharex=True, sharey=True,
                             figsize=(8,10))
    for instr in instrs:
        [fname, i, j, label] = instr
        fname = os.path.join("..", date, fname)
        ax = axes[i, j]
        data = tk.delay_load(fname)
        data, popt, pcov = tk.transform_delay(data, mwf, nave, xkey, fold,
                                              blink)
        # data, popt, pcov = tk.delay_plot(fname, xkey, ykey, ykey2, mwf, nave,
        #                                  ax, label, fold=fold, blink=blink)
        data.plot(x=xkey, y=ykey2, ax=ax, ls=None, marker='.', c='lightgrey')
        data.plot(x=xkey, y=ykey, ax=ax, c='C0', lw=2)
        data.plot(x=xkey, y='fit', ax=ax, c='C1', lw=2)
        ax.legend().remove()
    # columns
    axes[0, 0].set_title("MW = - 9 dB")
    axes[0, 1].set_title("MW = - 21 dB")
    # rows
    axes[0, 0].set_ylabel("PM = -36.5 dB")
    axes[1, 0].set_ylabel("PM = -33.5 dB")
    axes[2, 0].set_ylabel("PM = -30.5 dB")
    axes[3, 0].set_ylabel("PM = -28.2 dB")
    axes[4, 0].set_ylabel("PM = -27.5 dB")
    fig.tight_layout()
    fig.savefig("2018-10-24-delay_pretty.pdf")
    return


def delay_pmc(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18.5097e9*2  # Hz after doubler.
    fold = 1
    blink = False
    instrs = [
              ["24_delay_diode.txt", 0, "l=3"],
              ["30_delay_diode.txt", 2, "l=26"],
              ["31_delay_diode.txt", 1, "l=13"]
             ]
    fig, axes = plt.subplots(nrows=3, sharex=True, sharey=True)
    for instr in instrs:
        [fname, i, label] = instr
        fname = os.path.join("..", date, fname)
        ax = axes[i]
        data = tk.delay_load(fname)
        data, popt, pcov = tk.transform_delay(data, mwf, nave, xkey, fold,
                                              blink)
        # data, popt, pcov = tk.delay_plot(fname, xkey, ykey, ykey2, mwf, nave,
        #                                  ax, label, fold=fold, blink=blink)
        data.plot(x=xkey, y=ykey2, ax=ax, ls=None, marker='.', c='lightgrey')
        data.plot(x=xkey, y=ykey, ax=ax, c='C0', lw=2)
        data.plot(x=xkey, y='fit', ax=ax, c='C1', lw=2)
        ax.legend().remove()
        ax.set_ylabel(label)
    fig.tight_layout()
    fig.savefig("2018-10-24-pmc.pdf")
    return


def main():
    import toolkit as tk
    date = "2018-10-24"
    # cavity_resonances(date)
    # delay_short_9(date)
    # delay_short_21(date)
    # delay_mock(date)
    delay_pretty(date)
    # delay_pmc(date)
    # bessel(30.6, 21.8, 70.2, 3.0)
    return


if __name__ == "__main__":
    main()
