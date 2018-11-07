# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 23:03:40 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-11-04


def limits(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    fname = "1_lim.txt"
    fname = os.path.join("..", date, fname)
    fig, ax = plt.subplots()
    tk.dye_qs_lim(fname, [20, 40], [-120, -60], ax)
    return


def cavity_resonances(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    folder = os.path.join("..", date)
    norm = False
    fname = "2_fscan.txt"
    d = -1
    norm = False
    fig, ax = plt.subplots()
    fname = os.path.join(folder, fname)
    data, popt = tk.mw_fscan(fname, d, ax, norm=norm)
    fig.tight_layout()
    return


def mw_res(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    fname = "3_mwres.txt"
    fname = os.path.join("..", date, fname)
    marker = -18
    label = "-19 dB"
    mwf = 18.5094*2  # GHz
    fig, ax = plt.subplots()
    tk.mw_res(fname, marker, label, mwf, ax)
    return


def delay(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    fname = "20_delay.txt"
    fname = os.path.join("..", date, fname)
    fig, ax = plt.subplots()
    mwf = 18509.4e6*2
    window = 4
    tk.delay_short(fname, mwf, ax, window)
    return


def delay_listing(date):
    import os
    import pandas as pd
    fname = os.path.join("..", date, "delay_list.txt")
    dlist = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    print(dlist)
    return dlist


def delays_res0(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    mwf = 18.5094e9*2
    dlist = delay_listing(date)
    fig, axes = plt.subplots(nrows=3, ncols=2, sharex=True)
    axes[0, 1].set_title("6.6 mV/cm")
    axes[0, 0].set_title("0 mV/cm")
    axes[0, 0].set_ylabel("PM = 1.0")
    axes[1, 0].set_ylabel("PM = 1.4")
    axes[2, 0].set_ylabel("PM = 2.4")
    # res 0, PM = 1.0, 40 mV
    obs = dlist.iloc[0]
    fname = obs['fname']
    fname = os.path.join("..", date, fname)
    tk.delay_short(fname, mwf, axes[0, 1], window=5)
    # res 0, PM = 1.0, 0 mV
    obs = dlist.iloc[1]
    fname = obs['fname']
    fname = os.path.join("..", date, fname)
    tk.delay_short(fname, mwf, axes[0, 0], window=5)
    # res 0, PM = 1.4, 40 mV
    obs = dlist.iloc[2]
    fname = obs['fname']
    fname = os.path.join("..", date, fname)
    # res 0 PM - 2.4, 40 mV
    tk.delay_short(fname, mwf, axes[1, 0], window=5)
    obs = dlist.iloc[3]
    fname = obs['fname']
    fname = os.path.join("..", date, fname)
    tk.delay_short(fname, mwf, axes[1, 1], window=5)
    # res 0 PM - 2.4, 40mV
    obs = dlist.iloc[4]
    fname = obs['fname']
    fname = os.path.join("..", date, fname)
    tk.delay_short(fname, mwf, axes[2, 1], window=5)
    # res 0 PM- 2.4, 0 mV
    obs = dlist.iloc[5]
    fname = obs['fname']
    fname = os.path.join("..", date, fname)
    tk.delay_short(fname, mwf, axes[2, 0], window=5)
    # pretty
    for row in axes:
        for ax in row:
            ax.legend().remove()
    axes[-1, 0].set_xlabel(r"Delay ($T_{MW}$)")
    axes[-1, 1].set_xlabel(r"Delay ($T_{MW}$)")
    fig.tight_layout()
    fig.savefig("2018-11-04-res0delay.pdf")
    return


def delays_resm1(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    mwf = 18.5094e9*2
    dlist = delay_listing(date)
    fig, axes = plt.subplots(nrows=3, ncols=2, sharex=True)
    # res -1 PM - 1.0, 0 mV
    obs = dlist.iloc[7]
    fname = obs['fname']
    fname = os.path.join("..", date, fname)
    tk.delay_short(fname, mwf, axes[0, 1], window=5)
    return


def scratch(date):
    from scipy.special import jv
    print(jv(0, 1)**2*912)
    return


def main():
    date = "2018-11-04"
    # limits(date)
    # cavity_resonances(date)
    # mw_res(date)
    delay(date)
    delay_listing(date)
    # delays_res0(date)
    delays_resm1(date)
    # scratch(date)
    return


if __name__ == "__main__":
    main()
