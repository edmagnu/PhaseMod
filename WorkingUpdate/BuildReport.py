# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 19:44:04 2018

@author: labuser
"""

# Report of progress on phase modulation experiment.

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append("..")
import utilities as pmu


def n27_and_sidebands():
    """Plot Rydberg states around n=27 and the MW sidebands.
    Output:
        'n27_and_sidebands.pdf'
    """
    fig, ax = plt.subplots(nrows=1, ncols=1)
    # n=26 through n=29
    folder = os.path.join("..", "..", "2018-09-06")
    fname = "1_dye_fscan.txt"
    fname = os.path.join(folder, fname)
    data = pmu.fscan_import(fname)
    data.plot(x='fpoly', y='sig', label="MW Off", ax=ax)
    # sidebands
    folder = os.path.join("..", "..", "2018-09-09")
    fname = "1_freq_dye.txt"
    fname = os.path.join(folder, fname)
    data = pmu.fscan_import(fname)
    data['asig'] = data['sig'] - 0.3
    data.plot(x='fpoly', y='asig', label="MW On", ax=ax)
    # pretty figure
    ax.legend().remove()
    ax.set_ylabel(r"$e^-$ Signal")
    ax.set_yticks([])
    ax.set_xlabel("Frequency (GHz from Limit)")
    ax.text(-4400, -0.15, "MW On")
    ax.text(-4400, 0.3, "MW Off")
    # save
    fig.tight_layout()
    fig.savefig("n27_and_sidebands.pdf")
    return


def n27_and_stark():
    """Plot scan of n=27, showing the 3D(3/2,5/2) -> 27f transitions. Also show
    the stark states resolved when applying a vertical static field.
    Output:
        'n27_and_stark.pdf'
    """
    fig, ax = plt.subplots(nrows=1, ncols=1)
    # n=27 without static field.
    folder = os.path.join("..", "..", "2018-09-09")
    fname = "11_freq_diode.txt"
    fname = os.path.join(folder, fname)
    data = pmu.fscan_import(fname)
    data['afpoly'] = data['fpoly'] + 4511
    data.plot(x='afpoly', y='sig', ax=ax)
    # n=27 with static field.
    fname = "10_freq_diode.txt"
    fname = os.path.join(folder, fname)
    data = pmu.fscan_import(fname)
    data['afpoly'] = data['fpoly'] + 4511
    data['asig'] = data['sig'] + 0.15
    data.plot(x='afpoly', y='asig', ax=ax)
    # marks
    # f = 361354.6
    # ax.axvline(f - 365869.6 + 4511, color='grey', linestyle='dashed')
    # pretty figure
    ax.legend().remove()
    ax.set_ylabel(r"$e^-$ Signal")
    ax.set_yticks([])
    ax.set_xlabel(r"Frequency (GHz from $3d_{3/2} \rightarrow 27f$)")
    ax.text(-5.5, 0.2, "~ 3 V/cm Static", horizontalalignment='right')
    ax.text(-5.5, 0.00, "No Static", horizontalalignment='right')
    ax.text(1.5, 0.05, r"$3d_{5/2} \rightarrow 27f$")
    ax.text(-0.7, 0.1, r"$3d_{3/2} \rightarrow 27f$",
            horizontalalignment='right')
    ax.text(5.2, 0.25, "Only\n" + r"$3d_{5/2} \rightarrow 27f$")
    ax.text(-1, 0.4, "Both\nOverlapped", horizontalalignment='center')
    ax.text(-5.0, 0.4, "Only\n" + r"$3d_{3/2} \rightarrow 27f$",
            horizontalalignment='right')
    # save
    fig.tight_layout()
    fig.savefig('n27_and_stark.pdf')
    return


def delays():
    fig, ax = plt.subplots(nrows=1, ncols=1)
    # n=27 without static field.
    folder = os.path.join("..", "..", "2018-09-09")
    fname = "2_delay.txt"
    mwf = 19635.40*1e6*2  # Hz, doubled after generation.
    nave = 9
    fname = os.path.join(folder, fname)
    data = pmu.dscan_import(fname, mwf)
    data['srol'] = data['sig'].rolling(window=nave, center=True).mean()
    data.plot(x='fwlen', y='sig', marker='.', ls="", color='grey', ax=ax)
    data.plot(x='fwlen', y='srol', lw=3, color='C0', ax=ax)
    # twin x
    conv = 1e12/mwf  # Period in ps
    ax2 = ax.twiny()
    xlims = ax.get_xlim()
    tlims = tuple(np.array(xlims)*conv)
    # tticks = tuple(np.arange(0, 30, 5))
    ax2.set(xlim=tlims, xlabel="Delay (ps)")
    # pretty
    ax.legend().remove()
    ax.set_xlabel(r"Delay (MW $\lambda$)")
    ax.set_ylabel(r"$e^-$ Signal (arb. u.)")
    return data


# main script
if __name__ == "__main__":
    # n27_and_sidebands()
    # n27_and_stark()
    delays()
