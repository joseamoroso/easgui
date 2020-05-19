# -*- coding: utf-8 -*-
"""
Created on Thu May 14 02:19:04 2020

@author: josel
"""
from inspect import signature


def suma(x,y):
    print("Funcion Suma")
    return x+y,x*y

def calTax(inc,tax,taxEx):
    print("Funcion Taxes")
    return (inc*(tax/100))-taxEx

def conc(text):
    return("Hola "+text)
 
def arrAvg(array):
    # text = ""
    # for val in array:
    #     text+=val +" " 
    # return text
    return [i**2 for i in array]

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
 
