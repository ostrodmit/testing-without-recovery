#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 16:07:51 2020

@author: ostrodmit
"""

import numpy as np


def generate_samples(n,cov,theta):
    d = int(np.sqrt(cov.size))
    X0 = np.dot(cov,np.random.randn(d,n))
    X1 = np.dot(cov,np.random.randn(d,n))
    #ran = np.random.randn(n,2)
    e0 =  np.random.randn(n)
    e1 =  np.random.randn(n)
    Y0 = e0
    Y1 = np.dot(X1.T,theta) + e1
    H0 = np.dot(np.linalg.pinv(np.dot(X0,X0.T)),np.dot(X0,Y0))
    H1 = np.dot(np.linalg.pinv(np.dot(X1,X1.T)),np.dot(X1,Y1))
    return Y0,Y1,X0,X1,H0,H1

def mix_samples(w,n,Y0,Y1,X0,X1,H0,H1):
    # w is the fraction of adnixture
    n_add = np.int(np.round(w * n))
    Ymix = np.concatenate((Y1[:n_add],Y0[n_add:]))
    Xmix = np.concatenate((X1[:,:n_add],X0[:,n_add:]),axis=1)
    Hmix = np.dot(np.linalg.pinv(np.dot(Xmix,Xmix.T)),np.dot(Xmix,Ymix))
    return Ymix,Xmix,Hmix