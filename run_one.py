# -*- coding: utf-8 -*-

from generate_samples import generate_samples, mix_samples
from plot_one import plot_one

import numpy as np
import os
import time

def wrap_params(T,n,r,kappa,w):
    params = {'T':T,'n':n,'r':r,'kappa':kappa,'w':w}
    return params

def make_path(sce,T,n,r,kappa,w=0):
    fpath = os.getcwd() +'/data/'+np.str(sce)+'/T-'+np.str(T)+'-n-'+np.str(n) +'/r-'+np.str(r)+'-kap-'+np.str(kappa)
    if w > 0:
        fpath += ( '-w-' + np.str(w))
    fpath += '/'
    return fpath

def eval_test_val(Y0,Y1):
    return (np.sum(Y0**2) >= np.sum(Y1**2))

def eval_test_newton(H0,X0,H1,X1):
    #H1 = np.dot(np.linalg.pinv(np.dot(Z1,Z1.T)),np.dot(Z1,Y1))
    H00 = np.dot(X0.T,H0)
    #H2 = np.dot(np.linalg.pinv(np.dot(Z2,Z2.T)),np.dot(Z2,Y2))
    H11 = np.dot(X1.T,H1)
    return (np.sum(H00**2) >= np.sum(H11**2))

def eval_test_grad(Y0,Y1,X0,X1):
    G0 = np.dot(X0,Y0)
    G1 = np.dot(X1,Y1)
    return (np.sum(G0**2) >= np.sum(G1**2))

def eval_test_plug(Y0,Y1,X0,X1,H0,H1):
    theta_hat =  H0
    theta_bar_hat = H1
    theta_bar = theta_hat + theta_bar_hat 
    return ((np.sum(Y0**2) + np.sum((Y1-np.dot(X1.T,theta_bar))**2)) \
            >= (np.sum(Y1**2) + np.sum((Y0-np.dot(X0.T,theta_bar))**2)))

def eval_test_oracle(Y0,Y1,X0,X1,theta):
    return ((np.sum(Y0**2) + np.sum((Y1-np.dot(X1.T,theta))**2)) \
            >= (np.sum(Y1**2) + np.sum((Y0-np.dot(X0.T,theta))**2)))

def run_one(T,n,r,kappa,if_show_plot,sce='gauss',w=0.0,mixed_truth=0):
    params = wrap_params(T,n,r,kappa,w)
    start_time = time.time()    
    ### Define parameters and functions     
    log_nDelta_min = -3
    log_nDelta_max = 9
    num_nDelta = 50
    ## number of trials
    # T = 50      
    ## sample size
    # n = 100      
    ## rank
    # r = 20 or r = 40      
    ## condition number 
    # kappa = 50 or kappa = 10
    d = 2*r
    eigen = np.zeros(d)
    #eigen2 = np.zeros(n)
    eigen[:r] = np.sqrt(kappa)
    #eigen2[:r] = 1./10
    eigen[r:2*r] = 1.
    #eigen2[r:2*r] = 1.
    cov = np.diag(eigen)
    #cov2 = np.diag(eigen2)
        
    #Run simulations
    
    err_val = []
    err_newton = []
    err_grad = []
    err_plug = []
    err_oracle = []
    
    dev_val = []
    dev_newton = []
    dev_grad = []
    dev_plug = []
    dev_oracle = []
    
    nDelta_values = []
    count = 0

    for nDelta in np.logspace(log_nDelta_min, log_nDelta_max, num_nDelta, base=2):
        test_val = []
        test_newton = []
        test_grad = []
        test_plug = []
        test_oracle = []
        theta = np.zeros(d)
        #theta[r+1] = sqrt_Delta
        delta = np.sqrt(nDelta/n)
        theta[r+1] = delta # np.sqrt(delta) # c * np.sqrt( 2.* r) / n
        nDelta_values.append(nDelta)
        
        for t in range(T):
            Y0,Y1,X0,X1,H0,H1 = generate_samples(n,cov,theta)
            
            if sce=='mixture': # mix the two
                if mixed_truth:
                    Y0,X0,H0 = mix_samples(w,n,Y1,Y0,X1,X0,H1,H0)
                else:
                    Y1,X1,H1 = mix_samples(w,n,Y0,Y1,X0,X1,H0,H1)
            
            test_val.append(eval_test_val(Y0,Y1))
            test_newton.append(eval_test_newton(H0,X0,H1,X1))
            test_grad.append(eval_test_grad(Y0,Y1,X0,X1))
            test_plug.append(eval_test_plug(Y0,Y1,X0,X1,H0,H1))
            test_oracle.append(eval_test_oracle(Y0,Y1,X0,X1,theta))
        
        err_val.append(np.mean(test_val))
        err_newton.append(np.mean(test_newton))
        err_grad.append(np.mean(test_grad))
        err_plug.append(np.mean(test_plug))
        err_oracle.append(np.mean(test_oracle))
        
        dev_val.append(np.std(test_val)/np.sqrt(T))        
        dev_newton.append(np.std(test_newton)/np.sqrt(T))
        dev_grad.append(np.std(test_grad)/np.sqrt(T))
        dev_plug.append(np.std(test_plug)/np.sqrt(T))
        dev_oracle.append(np.std(test_oracle)/np.sqrt(T))
        
        count+=1
        if count%10==0:
            print(count)

    elapsed = time.time() - start_time
    print("Elapsed: %.0f sec" %elapsed)
    # Save results
    
    fpath = make_path(sce,T,n,r,kappa,w)
    os.makedirs(fpath,exist_ok=True)
    
    np.savetxt(fpath+'nDelta.txt',nDelta_values)

    np.savetxt(fpath+'err_val.txt',err_val)
    np.savetxt(fpath+'err_newton.txt',err_newton)
    np.savetxt(fpath+'err_grad.txt',err_grad)
    np.savetxt(fpath+'err_plug.txt',err_plug)
    np.savetxt(fpath+'err_oracle.txt',err_oracle)
    
    np.savetxt(fpath+'dev_val.txt',dev_val)
    np.savetxt(fpath+'dev_newton.txt',dev_newton)
    np.savetxt(fpath+'dev_grad.txt',dev_grad)
    np.savetxt(fpath+'dev_plug.txt',dev_plug)
    np.savetxt(fpath+'dev_oracle.txt',dev_oracle)
    
    # PLot results
    plot_one(fpath,params,if_show_plot)
    
    return fpath, params