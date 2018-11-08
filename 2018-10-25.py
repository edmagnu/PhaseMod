# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 10:38:34 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-10-24


def diode(date):
    import os
    import matplotlib.pyplot as plt
    import pandas as pd
    import toolkit as tk
    fig, axes = plt.subplots(nrows=4, sharex=False, sharey=True)
    # short integration
    fname = os.path.join("..", date, "1_freq_diode.txt")
    data = tk.diode_scan(fname)
    tk.diode_plot(data, axes[0], "")
    # no wavelength, much faster
    fname = os.path.join("..", date, "2_freq_diode.txt")
    data = tk.diode_scan(fname)
    tk.diode_plot(data, axes[1], "")
    # using the DL-100 Scan function
    fname = os.path.join("..", date, "3_freq_diode.txt")
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['v'] = -data['v']
    data.plot('t', 'v', ax=axes[2])
    # using the DL-100 Scan Function and averaging
    fname = os.path.join("..", date, "4_freq_diode.txt")
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['v'] = -data['v']
    data.plot('t', 'v', ax=axes[3])
    return


def phase_freq(date):
    import os
    import matplotlib.pyplot as plt
    import pandas as pd
    import toolkit as tk
    fig, axes = plt.subplots(nrows=3, sharex=True, sharey=True)
    instrs = [
              ["4_freq_diode.txt", "No Modulation"],
              ["5_freq_diode.txt", "Delay = 0"],
              ["6_freq_diode.txt", r"Delay = $\pi$"],
             ]
    for i, instr in enumerate(instrs):
        [fname, label] = instr
        fname = os.path.join("..", date, fname)
        ax = axes[i]
        data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
        data['v'] = -data['v']
        data['t'] = max(data['t'].values) - data['t']
        data.plot(x='t', y='v', ax=ax, label=label)
    ax.set_xlim(2500, 9000)
    fig.tight_layout()
    fig.savefig("2018-10-25-Stark_Map_Phase.pdf")
    return

def main():
    import toolkit as tk
    date = "2018-10-25"
    # diode(date)
    phase_freq(date)
    # print(tk.wlen_to_step(0.5, 18.5097e9*2))
    # print(tk.wlen_to_step(0, 18.5097e9*2))
    return


if __name__ == "__main__":
    main()
