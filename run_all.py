#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 14:22:49 2020

@author: ostrodmit
"""

from run_one import run_one, wrap_params, make_path
from plot_one import plot_one

import sys
import os
import numpy as np


#T = int(150*1e3)
T = int(150*1e0)

n = 64

#all_r = [4, 16, 32]
#all_kappa = [2, 16, 128]

all_r = [4,16,32]
all_kappa = [2,16,128]

def run_all(only_plots):
    sce = 'gauss'
    plts_path = os.getcwd() +'/plots/'+np.str(sce)+'/T-'+np.str(T)+'-n-'+np.str(n)+'/'
    os.makedirs(plts_path,exist_ok=True)
    
    for r in all_r: 
        for kappa in all_kappa:
            if only_plots:
                fpath = make_path(sce,T,n,r,kappa)
                params = wrap_params(T,n,r,kappa)
            else:
                (fpath,params) = run_one(T,n,r,kappa,1)
            plt = plot_one(fpath,params,0)
            plt_name = plts_path+'r-'+np.str(r)+'-kap-'+np.str(kappa)+'.pdf'
            plt.savefig(plt_name,bbox_inches="tight", format='pdf')
            
if __name__ == '__main__':
    only_plots = np.int(sys.argv[2])
    print('only_plots = '+np.str(only_plots))
    run_all(only_plots)            