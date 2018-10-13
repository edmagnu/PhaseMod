# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 19:44:04 2018

@author: labuser
"""

# Import and plot frequency scans from the dye laser.

import os
import matplotlib.pyplot as plt
import pandas as pd


def dye_scan():
    fname = os.path.join("..", "2018-09-09", "1_freq_dye.txt")
    data = pd.read_csv(fname, sep='\t', comment="#", index_col=False)
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='f', inplace=True)
    fig, ax = plt.subplots()
    # ax.axvline(0, c='k')
    ax.axhline(0, c='k')
    # e29 = -3910.510993878823
    # e26 = -4865.269534632156
    # print(max(data['sig']))
    # ax.plot([e26]*2, [0, 1.2*max(data['sig'])], '--', c='grey')
    # ax.text(e26, ax.get_ylim()[1], "26",
    #         horizontalalignment='center', verticalalignment='top')
    # ax.plot([e29]*2, [0, 1.2*max(data['sig'])], '--', c='grey')
    # ax.text(e29, ax.get_ylim()[1], "29",
    #         horizontalalignment='center', verticalalignment='top')
    e27 = -4511.5
    for i in [-2, -1, 0, 1, 2]:
        ax.axvline(e27 + 2*i*19.6354, color='grey', linestyle='dashed')
    data.plot(x='f', y='sig', ax=ax)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Signal (arb. u.)")
    ax.set_xlim(-4800, -4200)
    fig.tight_layout()
    fig.savefig("DyeScan.pdf")
    return


# main
dye_scan()
