# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 19:44:04 2018

@author: labuser
"""

# Report of progress on phase modulation experiment.

import os
import sys
import matplotlib.pyplot as plt
sys.path.append("..")
import utilities as pmu


def n27_and_sidebands():
    """Plot Rydberg states around n=27 and the MW sidebands.
    Output:
        'n27_and_sidebands.pdf'
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4.5, 4))
    # n=26 through n=29
    folder = os.path.join("..", "..", "2018-09-06")
    fname = "1_dye_fscan.txt"
    fname = os.path.join(folder, fname)
    data = pmu.fscan_import(fname)
    ax.axhline(0, color='grey')
    data.plot(x='fpoly', y='sig', label="MW Off", c='k', ax=ax)
    # sidebands
    folder = os.path.join("..", "..", "2018-09-09")
    fname = "1_freq_dye.txt"
    fname = os.path.join(folder, fname)
    data = pmu.fscan_import(fname)
    data['asig'] = data['sig'] - 0.3
    ax.axhline(-0.3, color='grey')
    data.plot(x='fpoly', y='asig', label="MW On", c='k', ax=ax)
    # pretty figure
    ax.legend().remove()
    ax.set_ylabel(r"$e^-$ Signal")
    ax.set_yticks([])
    ax.set_xlabel("Frequency (GHz from Limit)")
    ax.set_xticks([-4863, -4511, -4195, -3908])
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
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4.5, 4))
    # n=27 without static field.
    folder = os.path.join("..", "..", "2018-09-09")
    fname = "11_freq_diode.txt"
    fname = os.path.join(folder, fname)
    data = pmu.fscan_import(fname)
    data['afpoly'] = data['fpoly'] + 4511
    ax.axhline(0, color='grey')
    data.plot(x='afpoly', y='sig', c='k', ax=ax)
    # n=27 with static field.
    fname = "10_freq_diode.txt"
    fname = os.path.join(folder, fname)
    data = pmu.fscan_import(fname)
    data['afpoly'] = data['fpoly'] + 4511
    data['asig'] = data['sig'] + 0.15
    ax.axhline(0.15, color='grey')
    data.plot(x='afpoly', y='asig', c='k', ax=ax)
    # text
    ax.text(-5.5, 0.2, "3 V/cm", horizontalalignment='right')
    ax.text(-5.5, 0.01, "0 V/cm", horizontalalignment='right')
    # pretty figure
    ax.legend().remove()
    ax.set_ylabel(r"$e^-$ Signal")
    ax.set_yticks([])
    ax.set_xlabel(r"Frequency (GHz from $3d_{5/2} \rightarrow 27f$)")
    ax.set_xlim(-8, 7)
    # save
    fig.tight_layout()
    fig.savefig('n27_and_stark.pdf')
    return


def delays():
    fig, axes = plt.subplots(nrows=5, ncols=1, sharex=True,
                             figsize=(4.5, 6))
    # n=27 without static field.
    ax = axes[0]
    folder = os.path.join("..", "..", "2018-09-09")
    fname = "2_delay.txt"
    fname = os.path.join(folder, fname)
    mwf = 19635.40*1e6*2  # Hz, doubled after generation.
    nave = 9
    data = pmu.dscan_import(fname, mwf)
    data, ax = pmu.dscan_plot(data, ax, nave)
    # n=27 with -z Static, high l
    ax = axes[1]
    fname = "3_delay.txt"
    fname = os.path.join(folder, fname)
    data = pmu.dscan_import(fname, mwf)
    data, ax = pmu.dscan_plot(data, ax, nave)
    # n=27 with +z static, high l
    ax = axes[2]
    fname = "4_delay.txt"
    fname = os.path.join(folder, fname)
    data = pmu.dscan_import(fname, mwf)
    data, ax = pmu.dscan_plot(data, ax, nave)
    # n=27 with -z static, low l
    ax = axes[3]
    fname = "7_delay.txt"
    fname = os.path.join(folder, fname)
    data = pmu.dscan_import(fname, mwf)
    data, ax = pmu.dscan_plot(data, ax, nave)
    # n=27 with +z static, low l
    ax = axes[4]
    fname = "6_delay.txt"
    fname = os.path.join(folder, fname)
    data = pmu.dscan_import(fname, mwf)
    data, ax = pmu.dscan_plot(data, ax, nave)
    # pretty
    labels = ["(a)", "(b)", "(c)", "(d)", "(e)"]
    for i, ax in enumerate(axes):
        ax.legend().remove()
        ax.text(0.9, 0.5, labels[i], transform=ax.transAxes)
        # ax.set_ylabel(r"$e^-$ Signal (arb. u.)")
    axes[2].set_ylabel(r"$e^-$ Signal" + "\n(arb. u.)")
    axes[-1].set_xlim(-0.1, 1.2)
    axes[-1].set_xlabel(r"Delay (MW $\lambda$)")
    pmu.dscan_twin(axes[0], mwf)
    # save
    fig.tight_layout()
    fig.savefig("delays.pdf")
    return data


# main script
if __name__ == "__main__":
    # n27_and_sidebands()
    # n27_and_stark()
    delays()
