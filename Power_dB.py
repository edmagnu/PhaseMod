# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 21:48:57 2018

@author: labuser
"""

# get dB to relative power rates

import os
import random
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import pandas as pd


def dbm_mw(dbm):
    """Power (dBm) from Power (mW)"""
    return 1*np.power(10, dbm/10)


def mw_dbm(mw):
    """Power (mW) from Power (dBm)"""
    return 10*np.log10(mw/1)


def mw_f(mw):
    """Power in mW from field equivalent"""
    return np.power(mw, 0.5)


def f_mw(f):
    """Field equivalent from Power in mw"""
    return np.power(f, 2)


# main script
def plot_db_f():
    """Show field equivalent vs. dB"""
    db = np.arange(-24, -13)
    mw = dbm_mw(db)
    f = mw_f(mw)
    plt.plot(db, f, '.-')
    f = np.linspace(0.06, 0.20, 10)
    mw = f_mw(f)
    db = mw_dbm(mw)
    for i, field in enumerate(f):
        print(db[i])
    plt.plot(db, f, 'o-')
    return


def shuffling():
    """Shuffle the Attn dB I want to measure. -inf is MAX and inf is Blocked"""
    testdb = [-np.inf, -24.5, -22.5, -21, -19.4, -18.2, -17.2, -16.2, -15.4,
              -14.6, -14.0, np.inf]
    random.shuffle(testdb)
    for db in testdb:
        print(db)
    return


def analyze(name, ax, title, cal=False):
    """Read the Attn vs Signal data, and try to extract the Attn @ 50%"""
    # load
    fname = os.path.join("..", "2018-08-05", name)
    print(fname)
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    # convert to field equivalent
    data['f'] = mw_f(dbm_mw(data['Attn']))
    # normalize
    mask = (data['Attn'] == np.inf)
    zero = data.loc[mask, 'value'].mean()
    mask = (data['Attn'] == -np.inf)
    norm = data.loc[mask, 'value'].mean() - zero
    data['sig'] = (data['value'] - zero)/norm
    # sort
    data.sort_values(by='f', inplace=True)
    # filter relevant fitting values
    cval = 1
    if cal is True:
        cval = 0.1325/25  # from final result
    data['f'] = data['f']/cval
    alo, ahi = (-15, -22)
    mask = (data['Attn'] != np.inf) & (data['Attn'] != -np.inf)
    mask = mask & (data['Attn'] < alo) & (data['Attn'] > ahi)
    slope, intercept, rvalue, pvalue, stderr = \
        scipy.stats.linregress(data.loc[mask, 'f'], data.loc[mask, 'sig'])
    # print(slope, intercept)
    # plot
    ax.axvline(mw_f(dbm_mw(alo))/cval, c='k')
    ax.axvline(mw_f(dbm_mw(ahi))/cval, c='k')
    mask = (data['Attn'] != np.inf)
    data[mask].plot(x='f', y='sig', ls='', marker='.', ax=ax, label=title)
    xrange = max(data.loc[mask, 'f']) - min(data.loc[mask, 'f'])
    ax.set_xlim(min(data.loc[mask, 'f']) - 0.1*xrange,
                max(data.loc[mask, 'f']) + 0.1*xrange)
    ax.set_ylim(0, 1.2)
    ax.plot(data.loc[mask, 'f'], data.loc[mask, 'f']*slope + intercept, '-')
    f50 = (0.5-intercept)/slope
    db50 = mw_dbm(f_mw(f50))
    ax.axvline(f50, c='grey')
    ax.axhline(0.5, c='grey')
    # report
    title = "Attn @ 50% = " + str(np.round(db50, 1)) + " dB"
    print(title)
    return f50


# main script
# get data taking order
shuffling()
# plots
fig, ax = plt.subplots(nrows=2, sharex=True)
f50_370 = analyze("mwion370_2.txt", ax[0], "-370 GHz", cal=True)
f50_730 = analyze("mwion730_2.txt", ax[1], "-730 GHz", cal=True)
ax[1].set_xlabel("MW Field (V/cm)")
ax[0].set_ylabel("Signal")
ax[1].set_ylabel("Signal")
fig.tight_layout()
fig.savefig("MW_Ionization.pdf")
# 50% attenuation
f50 = (f50_370 + f50_730)/2
db50 = mw_dbm(f_mw(f50))
print("Attn @ 50% = " + str(np.round(db50, 1)) + " dB")
print(f50_370, f50_730)
print((f50_370-f50_730)/f50)
print(f50)
# print("370 GHz guess @ " + str(np.round(db50, 1)) + " dB = " )


