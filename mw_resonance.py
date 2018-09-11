# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 16:10:25 2018

@author: labuser
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(8, 10.5))

folder = os.path.join("..", "2018-07-19")
fname = "1_mw_atom.txt"
fname = os.path.join(folder, fname)
data = pd.read_csv(fname, comment="#", sep="\t", index_col=False)
data['f'] = data['f']*2e-9
data['v'] = -data['v']
data.sort_values(by='f', inplace=True)
data['v_rl'] = data['v'].rolling(window=5, center=True).mean()
data.plot(x='f', y='v_rl', ax=axes[0])
axes[0].set(ylabel="Atom Signal (arb. u.)")

fname = "2_mw_det_inj.txt"
fname = os.path.join(folder, fname)
data = pd.read_csv(fname, comment="#", sep="\t", index_col=False)
data['f'] = data['f']*2e-9
data['v'] = -data['v']*1000
data.sort_values(by='f', inplace=True)
data['v_rl'] = data['v'].rolling(window=5, center=True).mean()
data.plot(x='f', y='v_rl', ax=axes[1])
axes[1].set(ylabel="Power Injected (mV)")

fname = "3_mw_det_ref.txt"
fname = os.path.join(folder, fname)
data = pd.read_csv(fname, comment="#", sep="\t", index_col=False)
data['f'] = data['f']*2e-9
data['v'] = -data['v']*1000
data.sort_values(by='f', inplace=True)
data['v_rl'] = data['v'].rolling(window=5, center=True).mean()
data.plot(x='f', y='v_rl', ax=axes[2])
axes[2].set(ylabel="Power Reflected (mV)",
            xlabel="MW Frequency (GHz)")

fig.tight_layout()
fig.savefig("Cavity Resonance.pdf")
                   