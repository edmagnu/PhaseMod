# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 21:13:32 2018

@author: labuser
"""


def delays(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    fig, axes = plt.subplots(nrows=3, sharex=True, sharey=True)
    instrs = [["1_delay_diode.txt", "PM = 0.9", axes[0]],
              ["2_delay_diode.txt", "PM = 1.3", axes[1]],
              ["3_delay_diode.txt", "PM = 2.4", axes[2]]]
    xkey = 'wlen_fold'
    ykey = 'nsig_fold'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18.5100e9*2  # Hz after doubler.
    fold = 1
    blink = False
    for instr in instrs:
        [fname, label, ax] = instr
        fname = os.path.join("..", date, fname)
        args = (fname, xkey, ykey, ykey2, mwf, nave, ax, label, fold, blink)
        tk.delay_plot(*args)
    # minima = mins_by_eye()
    # for minimum in minima:
    #     ax.axvline(minimum, c='grey', linestyle='dashed')
    return


def mins_by_eye():
    import numpy as np
    mins = [56200, 72000, 87900, 104000, 119900, 136000]
    sep = np.mean(np.diff(mins))
    cent = np.mean(mins)
    off = 8e3
    fit = np.linspace(cent + off - 3*sep, cent + off + 2*sep, 6)
    print(fit)
    print(np.sum(fit-mins))
    return fit


def gba_target(x, value):
    import scipy.special as sp
    return abs(sp.jv(0, x)**2 - value)

def get_bessel_arg(amp_off, amp_on, amp_0, guess=1.0):
    import scipy.optimize as opt
    import scipy.special as sp
    value = (amp_on - amp_0)/(amp_off - amp_0)
    args = (value,)
    fit = opt.minimize(gba_target, guess, args=args, bounds=[(0, 100)])
    print(fit)
    fit = fit['x'][0]
    print("fit = ", fit)
    print("result = ", gba_target(fit, value))
    print("value = ", value)
    print("jv(0, fit) = ", sp.jv(0, fit)**2)
    return

def main():
    date = "2018-10-21"
    delays(date)
    get_bessel_arg(84.8, 4.0, 4.0)
    return


if __name__ == "__main__":
    main()
