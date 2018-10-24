# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:31:19 2018

@author: labuser
"""

# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-10-22


def cavity_resonances(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    """Using the dye laser at -180 GHz, the MW f is scanned over the
    cavity resonances, finding center, FWHM, and Q values."""
    fig, axes = plt.subplots(nrows=1, sharex=True)
    folder = os.path.join("..", date)
    norm = False
    instrs = [["1_fscan.txt", axes]]
    for instr in instrs:
        [fname, ax] = instr
        print("\n", fname)
        fname = os.path.join(folder, fname)
        data, popt = tk.mw_fscan(fname, 1, ax, norm=norm)
    fig.tight_layout()
    return


def delays(date):
    import os
    import matplotlib.pyplot as plt
    import toolkit as tk
    fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
    instrs = [["1_delay_diode.txt", "PM = 1.0", ax]]
    xkey = 'd'
    ykey = 'nsig_rm'
    ykey2 = 'nsig'
    nave = 4
    mwf = 18.5117e9*2  # Hz after doubler.
    fold = 1
    blink = False
    for instr in instrs:
        [fname, label, ax] = instr
        fname = os.path.join("..", date, fname)
        data = tk.delay_load(fname)
        data, popt, pconv = tk.transform_delay(data, mwf, nave, xkey, fold,
                                               blink)
        data.plot(x='d', y='nsig', ax=ax, label=label)
        print(popt[2], tk.wlen_to_step(6+popt[2], mwf))
        # args = (fname, xkey, ykey, ykey2, mwf, nave, ax, label, fold, blink)
        # data, popt, pcov = tk.delay_plot(*args)
        # if popt[1] > 0:
        #     phi1 = (popt[2] + 0.5)%1.0
        # else:
        #     phi1 = (popt[2])%1.0
        # print("Step at minimum = ", 100e3 + tk.wlen_to_step(phi1, mwf))
    # minima = mins_by_eye()
    # for minimum in minima:
    #     ax.axvline(minimum, c='grey', linestyle='dashed')
    return



def main():
    # import toolkit as tk
    date = "2018-10-22"
    # cavity_resonances(date)
    delays(date)
    # tk.get_bessel_arg(108, 67.2, 4.0)
    return


if __name__ == "__main__":
    main()