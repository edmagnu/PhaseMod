# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 22:42:17 2018

@author: labuser
"""

# Look at oscilloscope traces of the PM Laser sidebands at different MW Attn
# Try to find hints of non-linearity and higher harmonics.

import os
import matplotlib.pyplot as plt
import pandas as pd


def read_files():
    """Import all CSV oscilloscope traces and match to MW Attenuation"""
    dname = os.path.join("..", "2018-08-02")
    # load log file with fnumber <-> MW Attenuation
    fname = "log.txt"
    fname = os.path.join(dname, fname)
    log = pd.read_csv(fname, index_col=False, sep="\t", comment="#")
    log.sort_values(by='Attn', inplace=True)
    # master data set
    data_tot = pd.DataFrame()
    # Load oscilloscope trace
    for n in log['Fnum'].values:
        fname = "TEK000" + str(n) + ".CSV"
        fname = os.path.join(dname, fname)
        data = pd.read_csv(fname, index_col=False, header=None, usecols=[3, 4],
                           names=['t', 'V'])
        mask = (log['Fnum'] == n)
        attn = log.loc[mask, 'Attn'].values[0]
        data['Attn'] = attn
        data['n'] = n
        data_tot = data_tot.append(data, ignore_index=True)
    # plot
    fig, ax = plt.subplots(nrows=len(log['Fnum']), ncols=1, sharex=True)
    for i, n in enumerate(log['Fnum']):
        mask = (data_tot['n'] == n)
        data = data_tot[mask].copy()
        data.plot(x='t', y='V', label=data['Attn'].unique()[0], ax=ax[i])
    return data_tot, log


# main script
def main():
    result = read_files()
    return result


result = main()
