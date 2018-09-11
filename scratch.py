# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 07:16:49 2018

@author: labuser
"""

import math

def atomic_units():
    """Return a dictionary of atomic units, ['GHz'], ['mVcm'], and ['ns']"""
    au = {'GHz': 1.51983e-7, 'mVcm': 1.94469e-13, 'ns': 4.13414e7}
    return au


au = atomic_units()
print((-900*au['GHz'])**2*1/4/au['mVcm']*1e-3)
print(math.sqrt(10*au['mVcm']*1e3*4)/au['GHz'])
print(1/(3*47**5)/au['mVcm'])