# -*- coding: utf-8 -*-
"""
Created on Thu May 14 02:19:04 2020

@author: josel
"""
from inspect import signature


def suma(x,y):
     return x+y

def calTax(inc,tax,taxEx):
    return (inc*(tax/100))-taxEx

 
def sumaLocal():
    print("Hola")

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
 
