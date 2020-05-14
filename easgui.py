# -*- coding: utf-8 -*-
"""
Created on Thu May 14 01:06:33 2020

@author: Jose Amoroso
"""


from textx import metamodel_from_file
from tkinter import Tk,Button,Label,Entry,Canvas,LEFT, RIGHT,HORIZONTAL,BOTH,TOP,BOTTOM,X
from tkinter import ttk


#REVISAR SINTAXIS DE WRAP, IGUAL QUE BORRE CONTENIDO ANTES DE CALCULAR UNO NUEVO        
def wrap(func,args):
    argsList = []
    for value in args[:-1]:
        argsList.append(int(value.get()))
    argsTuple= tuple(argsList)
    result = func(*argsTuple)
    lastArg = args[-1]
    lastArg.delete(0,"end")
    lastArg.insert(0,str(result))
    
class GUI:
    def __init__(self,master):
        self.functions = {}
        self.inputs = {}
        self.master = master
        self.functionFlag = False
        self.canvasPosition = (50,50)
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
                    self.inputs[inputs.inputName]=(self.label,self.entry)
                    # self.canvas.create_window(self.canvasPosition[0],self.canvasPosition[1], window=self.entry)
                    self.label.pack(side=TOP,  fill=X,padx=5, pady=5)
                    self.entry.pack(side=TOP, expand=True)
                ######################################################################
                ################### Create button with function ######################
                ######################################################################
                tempListValues = []
                for elem in self.inputs.values():
                    tempListValues.append(elem[1])
                listValues = tuple(tempListValues)   
                funTemp = wrap
                self.button = Button(self.master, text=c.buttonName, command=lambda:funTemp(self.functions[c.functionName],listValues))      
                self.button.pack(pady=5)
                ######################################################################

            

def main(debug=False):
    gui_mm = metamodel_from_file('easgui.tx')
    
    gui_model = gui_mm.model_from_file('program.eui')
    
    
    root = Tk()
    my_gui = GUI(root)
    my_gui.interpret(gui_model)
    root.mainloop()

if __name__ == "__main__":
    main()