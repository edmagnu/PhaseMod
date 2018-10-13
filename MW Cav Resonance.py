# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 11:16:38 2018

@author: labuser
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


f1 = os.path.join("..", "2018-06-27", "4_fscan.txt")
f2 = os.path.join("..", "2018-06-27", "3_fscan_b.txt")

df1 = pd.read_csv(f1, sep="\t", index_col=0, comment="#", names=["V"])
df1.sort_index(inplace=True)
df2 = pd.read_csv(f2, sep="\t", index_col=0, comment="#", names=["V"])
df2.sort_index(inplace=True)
fig, axes = plt.subplots(nrows=2, sharex=True)
df1.plot(ax=axes[0])
df2.plot(ax=axes[0])
df3 = df2['V'] - df1['V']
df3.plot(ax=axes[1])
# df2.sort_values(by='f', inplace=True)
# df3 = df1.copy()
# df3['V'] = df1['V'] - df2['V']
# ax = df1.plot(x=index, y='V', label="Cavity")
# df2.plot(x='f', y='V', label="Blocked", ax=ax)
