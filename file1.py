# -*- coding: utf-8 -*-
"""
Created on Thu May 14 02:19:04 2020

@author: josel
"""
from inspect import signature
import numpy as np

def suma(x,y):
    return x+y,x*y

def calTax(inc,tax,taxEx):
    # print("Funcion Taxes")
    return (inc*(tax/100))-taxEx

def conc(text):
    return("Hola "+text)
 
def arrAvg(array):
    # text = ""
    # for val in array:
    #     text+=val +" " 
    # return text
    return [i**2 for i in array]

def covMatrix(matrix):
    return np.cov(matrix)


