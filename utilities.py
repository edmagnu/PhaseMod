# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 23:03:35 2018

@author: edmag
"""

import numpy as np
import pandas as pd


# Utilities useful for PhaseMod analysis
# Eric Magnuson, University of Virginia, VA

def atomic_units():
    """Return a dictionary of lab -> atomic unit conversion factors.
    'GHz' : 1.51983e-7 a.u. = 1 GHz
    'mVcm' : 1.94469e-13 a.u. = 1 mV/cm
    'ns' : 4.13414e7 a.u. = 1 ns"""
    au = {"GHz": 1.51983e-7, "mVcm": 1.94469e-13, "ns": 4.13414e7}
    return au


def step_freq_fit(i, f, o=5):
    """Use polyfit and polyval to fit diode laser steps to frequency. The steps
    corresponding to a control often produce frequency changes finer than the
    resolution of the frequency meter.
    inputs:
        i : step number
        f : Measured frequency frequency
        o=5 : polynomial order
    returns:
        fpoly : polynomial-fitted frequency"""
    p = np.polyfit(i, f, o)
    fpoly = np.polyval(p, i)
    return fpoly


def fscan_import(fname, o=5):
    """Load a frequency scan from 'fname'. Add a polynomial-fitted frequency,
    background corrected signal, and a normalized signal.
    inputs:
        fname : name of data file
        o=5 : polynomial order for frequency fitting
    returns:
        data : dataframe with datafile keys and
            'fpoly' : polynomial fitted frequency
            'sig' : signal - signal background
            'nsig' : sig / (norm - norm background)
    """
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['fpoly'] = step_freq_fit(data['i'], data['f'], o)
    data['sig'] = data['s'] - data['sb']
    data['nsig'] = data['sig'] / (data['n'] - data['nb'])
    data.sort_values(by='i', inplace=True)
    return data


def dscan_import(fname, mwf):
    """Load a delay scan from 'fname'. Add a bacground corrected signal, and a
    normalized signal. Add folded signals for each.
    inputs:
        fname : name of data file
        mwf : Microwave Frequency in Hz
    returns:
        data : dataframe with datafile keys and
            'dist' : delay distance (m)
            'wlen' : delay in MW wavelenghts
            'time' : delay in path-time (s)
            'fwlen' : wlen folded into 1 wavelength
            'ftime' : time folded into 1 period
            'sig' : signal - signal background
            'nsig' : sig / (norm - norm background)
    """
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    # delays
    m = 2.539e-7  # delay stage calibration, m/step
    c = 299792458.0  # Speed of Light, meters/second
    data['dist'] = data['d']*m*2
    data['wlen'] = data['dist']*mwf/c
    data['time'] = data['dist']/c
    data['fwlen'] = data['wlen'] % 1
    data['ftime'] = data['time'] % (1/mwf)
    data.sort_values(by='fwlen', inplace=True)
    # signals
    data['sig'] = data['s'] - data['sb']
    data['nsig'] = data['sig'] / (data['n'] - data['nb'])
    return data


def dscan_plot(data, ax, nave=9):
    """Standardize plotting of delay scan.
    inputs:
        data : pandas.DataFrame with 'fwlen' and 'sig'
        ax : axes to plot on
        nave=9 : number of points for rolling mean
    returns:
        data : Same as input with one extra key
            'srol' : rolling mean of 'sig' using nave points
        ax : axes plotted on.
    """
    data['srol'] = data['sig'].rolling(window=nave, center=True).mean()
    data.plot(x='fwlen', y='sig', marker='.', ls="", color='lightgrey', ax=ax)
    data.plot(x='fwlen', y='srol', lw=3, color='k', ax=ax)
    return data, ax


def dscan_twin(ax, mwf):
    """For a delay scan, build a twiny axes for timing from wavelength
    inputs:
        ax : axes from which to build the twiny axes
        mwf : microwave frequency
    returns:
        ax2 : twiny axes with time delay in ps.
    """
    conv = 1e12/mwf  # Period in ps
    ax2 = ax.twiny()
    xlims = ax.get_xlim()
    tlims = tuple(np.array(xlims)*conv)
    ax2.set(xlim=tlims, xlabel="Delay (ps)")
    return ax2
