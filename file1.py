# -*- coding: utf-8 -*-
"""
Created on Thu May 14 02:19:04 2020

@author: josel
"""
from inspect import signature
import numpy as np

def suma(x,y,boola):
    print(boola)
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

# a = suma
# lista=[]
# s = signature(a)
# s = s.parameters
# c=4
# for elem in s:
#     lista.append(c)
#     c+=8
# lista=tuple(lista)
# v = suma(*lista)
 
