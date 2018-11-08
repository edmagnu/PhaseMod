# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:26:06 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-10-30


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

def DG535(date):
    import os
    # import matplotlib.pyplot as plt
    import pandas as pd
    # import toolkit as tk
    fname = os.path.join("..", date, "2_DG535_diode.txt")
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['sig'] = data['s'] - data['b']
    data['ref'] = data['r'] - data['b']
    data['nrm'] = data['sig'] - data['ref']
    ax = data.plot(x='d', y='nrm', marker='.')
    ax.axvline(2.275, c='grey', ls='dashed')
    ax.axvline(2.585, c='grey', ls='dashed')
    ax.legend().remove()
    ax.set_xlabel(r"MW Pulse Delay ($\mu$s)")
    ax.set_ylabel("Signal - Reference")
    ax.set_title("MW Power Shift from MW Pulse Delay")
    return


def bessels(date):
    import toolkit as tk
    a0 = 39.2
    a1 = 29.6
    off = 92.8
    zero = 3.20
    tk.get_bessel_arg(off, a0, zero, guess=1.0, quiet=False, order=0)
    print()
    tk.get_bessel_arg(off, a1, zero, guess=1.0, quiet=False, order=1)
    return


def main():
    date = "2018-10-30"
    # cavity_resonances(date)
    # DG535(date)
    bessels(date)
    return


if __name__ == "__main__":
    main()
