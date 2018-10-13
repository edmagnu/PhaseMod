# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 20:53:17 2018

@author: labuser
"""

# Load and display limit scans from 2018-09-23

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def limit_scan(fname):
    data = pd.read_csv(fname, sep='\t', comment="#", index_col=False)
    data['sig'] = data['s'] - data['sb']
    data.sort_values(by='f', inplace=True)
    data.plot(x='f', y='sig')
    return
    

if __name__ == "__main__":
    fname = "1_lim_dye.txt"
    folder = os.path.join("..", "2018-09-23")
    fname = os.path.join(folder, fname)
    limit_scan(fname)