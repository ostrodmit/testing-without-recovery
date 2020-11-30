#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 16:06:37 2020

@author: ostrodmit
"""

import numpy as np
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
import matplotlib.pyplot as plt

def plot_one(fpath,params,if_show_plot):
    
    # Load data
    
    nDelta = np.loadtxt(fpath+'nDelta.txt') 
    
    #err_oracle = np.loadtxt(fpath+'err_oracle.txt')
    
    err_newton = np.loadtxt(fpath+'err_newton.txt')
    err_val = np.loadtxt(fpath+'err_val.txt')
    err_grad = np.loadtxt(fpath+'err_grad.txt')
    err_plug = np.loadtxt(fpath+'err_plug.txt')
    
    # Plot curves
    
    fig, ax = plt.subplots()
    fig.figsize = (20,20)
    
    plt.grid(linestyle=':')
    
    fs_small = 26
    fs_medium = 28
    fs_large = 30
    
    
    #ymin, ymax = ax.get_ylim()
    #xtick_freq = 2
    #ytick_freq = 2
    #ax.set_yticks(np.round(np.linspace(ymin, ymax, ytick_freq), 2))
    #ax.set_yticks(np.round(np.linspace(ymin, ymax, ytick_freq), 2))
    
    plt.locator_params(axis='y', nbins=5)
    
    plt.xticks( fontsize=fs_small)
    plt.yticks(fontsize=fs_small)
    
    plt.xlabel(r'$\log_{2}(n\Delta)$',fontsize=fs_medium)
    plt.ylabel(r'$\log_{2}(\textup{Prob})$',fontsize=fs_medium)
    _title = '$r =$ '+np.str(2*params['r'])+', $\;\kappa=$ '+np.str(params['kappa'])
    if params['w'] > 0:
        _title += ', $\;w=$ '+np.str(params['w'])
    plt.title(_title,fontsize=fs_large)
    
    log_nDelta = np.log2(np.array(nDelta)) #  
    Lw = 4
    
    #ax.plot(logDelta, err_oracle, lw=Lw)

    
    ax.plot(log_nDelta, np.log2(err_newton),\
            lw=Lw+1,linestyle='solid',color='black')
    ax.plot(log_nDelta, np.log2(err_val),\
            lw=Lw,linestyle='dashed',color='red')
    ax.plot(log_nDelta, np.log2(err_grad),\
            lw=Lw,linestyle='dotted',color='blue')
    ax.plot(log_nDelta, np.log2(err_plug),\
            lw=Lw,linestyle='dashdot',color='green')
    
    
    #plt.legend(['loss','Newton','grad','plug-in','oracle'],fontsize=fs_small)
    plt.legend([r'(Lin)',r'(Val)',r'(Grad)',r'(Plug)'],fontsize=fs_small)
    plt.savefig(fpath+"plot.pdf", bbox_inches="tight", format='pdf')
    
    if if_show_plot:
        plt.show()
        
    return plt