# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 23:24:07 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-07-19

def static_delays(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    fig, axes = plt.subplots(nrows=3, sharex=True, sharey=True,
                             figsize=(4, 6))
    instrs = [["10_delay.txt", "0 mV/cm", axes[0]],
              ["11_delay.txt", "+14 mV/cm", axes[1]],
              ["15_delay.txt", "-14 mV/cm", axes[2]]]
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18268e6*2
    fold = 3
    blink = False
    for instr in instrs:
        [fname, label, ax] = instr
        fname = os.path.join("..", date, fname)
        # args = (fname, xkey, ykey, ykey2, mwf, nave, ax, label, fold, blink)
        # data, popt, pcov = tk.delay_plot(*args)
        data = tk.delay_load(fname)
        data, popt, pcov = tk.transform_delay(data, mwf, nave, xkey, fold,
                                              blink)
        data.plot(x=xkey, y=ykey, ax=ax, label=label)
        data.plot(x=xkey, y='fit', ax=ax)
        tk.fit_report(fname, label, popt)
        print("max , min = ", max(data['fit'].values), min(data['fit'].values))
    axes[-1].set_xlabel(r"Delay (MW $\lambda$)")
    axes[1].set_ylabel("Normalized Signal")
    axes[0].set_ylim(0, 1)
    fig.tight_layout()
    fig.savefig("2018-07-19-Static_at_Limit.pdf")
    return


def power_delays(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    fig, axes = plt.subplots(nrows=3, sharex=True, sharey=True,
                             figsize=(4, 6))
    instrs = [["10_delay.txt", r"$P_0$", axes[1]],
              ["12_delay.txt", r"$P_0$ - 6 dB", axes[2]],
              ["13_delay.txt", r"$P_0$ + 6 dB", axes[0]]]
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18268e6*2
    fold = 3
    blink = False
    for instr in instrs:
        [fname, label, ax] = instr
        fname = os.path.join("..", date, fname)
        # args = (fname, xkey, ykey, ykey2, mwf, nave, ax, label, fold, blink)
        # data, popt, pcov = tk.delay_plot(*args)
        data = tk.delay_load(fname)
        data, popt, pcov = tk.transform_delay(data, mwf, nave, xkey, fold,
                                              blink)
        data.plot(x=xkey, y=ykey, ax=ax, label=label)
        data.plot(x=xkey, y='fit', ax=ax)
        tk.fit_report(fname, label, popt)
        print("max , min = ", max(data['fit'].values), min(data['fit'].values))
    axes[-1].set_xlabel(r"Delay (MW $\lambda$)")
    axes[1].set_ylabel("Normalized Signal")
    axes[0].set_ylim(0, 1)
    fig.tight_layout()
    fig.savefig("2018-07-19-Power_at_Limit.pdf")
    return


def main():
    date = "2018-07-19"
    static_delays(date)
    power_delays(date)
    return


if __name__ == "__main__":
    main()
