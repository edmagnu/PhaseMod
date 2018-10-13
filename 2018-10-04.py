# University of Virginia, Department of Physics
# Eric Magnuson, edm5gb@virginia.edu

# 2018-10-04

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def step_freq_fit(o, i, f):
    p = np.polyfit(i, f, o)
    fpoly = np.polyval(p, i)
    return fpoly


def diode_scan(fname, ax, label):
    """Display diode scan with polynomial fitted laser frequency."""
    data = pd.read_csv(fname, sep="\t", comment="#", index_col=False)
    data['fpoly'] = step_freq_fit(5, data['i'], data['f'])
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='i', inplace=True)
    data.plot(x='fpoly', y='sig', ax=ax, label=label)
    ax.set_xlabel("Frequency (GHz)")
    # ax.set_ylabel("Signal (arb. u.)")
    # fig.savefig("DiodeScan.pdf")
    return


def stark_spectroscopy(date):
    fig, axes = plt.subplots(nrows=4, sharex=True)
    instrs = [["4_stark_0V.txt", "0 V", axes[0]],
              ["2_stark_20V.txt", "20 V", axes[1]],
              ["1_stark_40V.txt", "40 V", axes[2]],
              ["3_stark_200V.txt", "200 V", axes[3]]]
    for instr in instrs:
        [fname, label, ax] = instr
        fname = os.path.join("..", date, fname)
        diode_scan(fname, ax, label)
    fig.tight_layout()
    fig.savefig("stark_scans.pdf")
    return


if __name__ == "__main__":
	date = "2018-10-04"
	stark_spectroscopy(date)
	plt.show()