# -*- coding: utf-8 -*-
"""
Created on Thu May 14 01:06:33 2020

@author: Jose Amoroso
"""


from textx import metamodel_from_file
from tkinter import Tk,Button,Label,Entry,Canvas,LEFT, RIGHT,HORIZONTAL,BOTH,TOP,BOTTOM,X
from tkinter import ttk
from functools import partial

#REVISAR SINTAXIS DE WRAP, IGUAL QUE BORRE CONTENIDO ANTES DE CALCULAR UNO NUEVO        
def wrap(func,args):
    # print("\n"+("#"*56))
    # print(args)
    argsList = []
    outlist = []
    for value in args:
        # print(value.get()+"\n")
        if value[1] == 'INTINPUT':
             argsList.append(int(value[0].get()))
        if value[1] == 'DECIMALINPUT':
             argsList.append(float(value[0].get()))
             ###################################################
        if value[1] == 'LISTINTINPUT':
            tempList = value[0].get().split(',')
            tempList = [int(i) for i in tempList]
            argsList.append(tempList)
        if value[1] == 'LISTIDECIMALINPUT':
            tempList = value[0].get().split(',')
            tempList = [float(i) for i in tempList]
            argsList.append(tempList)
        if value[1] == 'LISTSTRINGINPUT':
            tempList = value[0].get().split(',')
            tempList = [str(i) for i in tempList]
            argsList.append(tempList)
        if value[1] == 'STRINGINPUT':
             argsList.append(str(value[0].get()))
        if value[1] == 'OUTPUT':
             outlist.append(value[0])
    
    result = func(*tuple(argsList)) 
    
    if type(result)==tuple:
        if len(outlist)<=1: 
            print("INCOMPATIBLEN: not result is tuple")
            return
    
    if len(outlist)>1:
        if type(result)!=tuple:
            print("INCOMPATIBLEN: not tuple result")
            return
        if len(result) != len(outlist) :
            print("INCOMPATIBLEN between results and OUTPUTS")
            return
        else:
            for i in range(len(outlist)):
                outlist[i].delete(0,"end")
                outlist[i].insert(0,str(result[i]))
                
    if len(outlist)==1:
        outlist[0].delete(0,"end")
        outlist[0].insert(0,str(result))
        
class GUI:
    def __init__(self,master):
        self.co=0
        self.functions = {}
        self.master = master
        self.functionFlag = False
        self.allButton ={}
        # self.canvasPosition = (50,50)
        # Initial size of windows is (500,500) and name easgui
        master.title("EASGUI")
        # self.canvas = Canvas(self.master, width=500,
        #                     height=500, bg = "black")
        master.geometry("500x500")



    def interpret(self, model):
        for c in model.commands:
            if c.__class__.__name__ == "ImportFunction": 
                package = c.fileName
                name = c.functionName
                imported = getattr(__import__(package, fromlist=[name]), name)
                self.functions[c.newFunctionName]=imported
                
    
            if c.__class__.__name__ == "CreateWindow": 
                self.master.title(c.NameID)
                newSize = "{}x{}".format(c.coor1[0],c.coor1[1])
                # self.canvas = Canvas(self.master, width=c.coor1[0],
                #             height=c.coor1[1], bg = "black")
                # self.canvas.pack()
                self.master.geometry(newSize)


            if c.__class__.__name__ == "CreateFunction":
                self.inputs = {}
                self.listValues = None
                self.button=None
                #Insert line horizontal
                if (self.functionFlag):
                    self.separ = ttk.Separator(self.master, orient=HORIZONTAL)
                    self.separ.pack(side=TOP,fill=BOTH, expand=True)
                self.functionFlag = True
                ######################################################################
                ########################## Create inputs #############################
                ######################################################################
                for inputs in c.parameter:
                    self.label = Label(self.master, text=inputs.inputName+':', anchor='w')
                    self.entry = Entry(self.master)
                    self.inputType = inputs.inputType
                    self.inputs[inputs.inputName]=(self.label,(self.entry,self.inputType))
                    # self.canvas.create_window(self.canvasPosition[0],self.canvasPosition[1], window=self.entry)
                    self.label.pack(side=TOP,  fill=X,padx=5, pady=5)
                    self.entry.pack(side=TOP, expand=True)
                ######################################################################
                ################### Create button with function ######################
                ######################################################################
                self.tempListValues = []
                for elem in self.inputs.values():
                    self.tempListValues.append(elem[1])
                self.listValues = tuple(self.tempListValues)
                self.button = Button(self.master, text=c.buttonName)
                # self.button.configure(command=lambda: wrap(self.functions[c.functionName],self.listValues))
                self.button.configure(command=partial(wrap,self.functions[c.functionName],self.listValues))
                self.button.pack(pady=5)
                ######################################################################
            

            


gui_mm = metamodel_from_file('easgui.tx')

gui_model = gui_mm.model_from_file('program.eui')


root = Tk()
my_gui = GUI(root)
my_gui.interpret(gui_model)

root.mainloop()
