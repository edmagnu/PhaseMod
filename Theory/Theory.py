# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 18:20:36 2018

@author: edmag
"""


def progress(source, i, total):
    """print an updating report of 'source: i/total'"""
    # start on fresh line
    if i == 0:
        print()
    # progress
    print("\r{0}: {1} / {2}".format(source, i+1, total), end="\r")
    # newline if we've reached the end.
    if i+1 == total:
        print()
    return


def build_phsig(kmax, dpm, dmw):
    import numpy as np
    import scipy.special as sp
    import pandas as pd
    ts = np.linspace(-2*np.pi, 4*np.pi, 64*3 + 1)
    # Amplitude modifying <g|mu|f> matrix element due to modulation
    amp = sp.jv(0, dpm)*sp.jv(0, dmw)
    for k in range(1, kmax+1):
        progress("build_phsig()", k, kmax+1)
        term = sp.jv(k, dpm)*sp.jv(k, dmw)*np.cos(k*ts)
        amp = amp + 2*term
    # value is actually the square of the amplitude.
    amp = np.square(amp)
    phsig = pd.DataFrame({'t': ts, 's': amp})
    return phsig


def build_phsig_1(kmax, dpm, dmw):
    import numpy as np
    import scipy.special as sp
    import pandas as pd
    ts = np.linspace(-2*np.pi, 4*np.pi, 64*3 + 1)
    # Amplitude modifying <g|mu|f> matrix element due to modulation
    amp = sp.jv(0, dpm)*sp.jv(0, dmw)
    for k in range(1, kmax+1):
        progress("build_phsig()", k, kmax+1)
        term = sp.jv(k+1, dpm)*sp.jv(k, dmw)*np.cos(k*ts)
        amp = amp + 2*term
    # value is actually the square of the amplitude.
    amp = np.square(amp)
    phsig = pd.DataFrame({'t': ts, 's': amp})
    return phsig


def turning_phsig(kmax, dpm, dmw, ts):
    import numpy as np
    import scipy.special as sp
    import pandas as pd
    amp = sp.jv(0, dpm)*sp.jv(0, dmw)
    for k in range(1, kmax+1):
        progress("scalar_phsig()", k, kmax+1)
        term = sp.jv(k, dpm)*sp.jv(k, dmw)*np.cos(k*ts)
        amp = amp + 2*term
    amp = np.square(amp)
    phsig = pd.DataFrame({'pm': dpm, 's': amp})
    return phsig


def pm_mw_lattice_plots():
    import numpy as np
    import matplotlib.pyplot as plt
    kmax = 10
    # dpm = 2.0  # Phase Modulation coefficient
    # dmw = 1.0  # MW modulation, k_s * E / omega_MW
    dpms = [0, 0.5, 1.5, 2.5]
    dmws = [0.0, 0.2, 0.5]
    fig, axes = plt.subplots(nrows=len(dpms), ncols=len(dmws), sharex=True,
                           sharey=True, figsize=(8, 8))
    for i, dpm in enumerate(dpms):
        for j, dmw in enumerate(dmws):
            data = build_phsig(kmax, dpm, dmw)
            data['wlen'] = data['t']/(2*np.pi)
            # label = "PM = {0}, MW = {1}".format(dpm, dmw)
            data.plot(x='wlen', y='s', ax=axes[i, j])
            axes[i, j].legend().remove()
    for i, dpm in enumerate(dpms):
        axes[i, 0].set_ylabel("PM = " + str(dpm))
    for i, dmw in enumerate(dmws):
        axes[0, i].set_title("MW = " + str(dmw))
    axes[-1, 1].set_xlabel(r"Delay (MW $\lambda$)")
    for i in [0, 2]:
        axes[-1, i].set_xlabel("")
    # fig.tight_layout()
    fig.suptitle("Calculated Phase Dependence for Different Atom and Laser" +
                 " Modulation Indicies")
    fig.savefig("PhaseDependence.pdf")
    return


def turnaround_plots():
    import numpy as np
    import matplotlib.pyplot as plt
    kmax = 10
    # dmw = 0.5
    dpm = np.linspace(0, 3, 100)
    # ts = np.pi
    fig, axes = plt.subplots(ncols=2)
    for dmw in [0, 0.2, 0.4, 0.6]:
        ts = 0
        data = turning_phsig(kmax, dpm, dmw, ts)
        axes[0].plot(data['pm'], data['s'], label=dmw)
        axes[0].set_title("delay = 0")
        ts = np.pi
        data = turning_phsig(kmax, dpm, dmw, ts)
        axes[1].plot(data['pm'], data['s'], label=dmw)
        axes[1].set_title(r"delay = $\pi$")
    axes[1].legend()
    axes[0].set_xlabel("PM Index")
    axes[0].set_ylabel("Normalized Signal")
    fig.suptitle("Minimum and Maximum Signal vs. PM for State Modulation" + 
                 " Indicies")
    # fig.tight_layout()
    fig.savefig("MinMaxMod.pdf")
    return



def main():
    pm_mw_lattice_plots()
    turnaround_plots()
    return


if __name__ == "__main__":
    main()
