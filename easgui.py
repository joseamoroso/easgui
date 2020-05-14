# -*- coding: utf-8 -*-
"""
Created on Thu May 14 01:06:33 2020

@author: josel
"""


from textx import metamodel_from_file
from tkinter import Tk,Button,Label,Entry

    
class GUI:
    def __init__(self,master):
        self.functions = {}
        self.inputs = {}
        self.master = master
        # Initial size of windows is (500,500) and name easgui
        master.title("EASGUI")
        master.geometry("500x500")

#REVISAR SINTAXIS DE WRAP, IGUAL QUE BORRE CONTENIDO ANTES DE CALCULAR UNO NUEVO        
    def wrap(self,func,args):
        argsList = []
        for value in args[:-1]:
            argsList.append(int(value.get()))
        argsTuple= tuple(argsList)
        result = func(*argsTuple)
        lastArg = args[-1]
        lastArg.delete(0,"end")
        lastArg.insert(0,str(result))

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
                self.master.geometry(newSize)
                
            if c.__class__.__name__ == "CreateInputs":
                for inputs in c.parameter:
                    self.label = Label(self.master, text=inputs.inputName)
                    self.entry = Entry(self.master)
                    self.inputs[inputs.inputName]=(self.label,self.entry)
                    self.label.pack()
                    self.entry.pack()
            
            if c.__class__.__name__ == "CreateButton":
                tempListValues = []
                #tempSignature = signature(self.functions[c.functionName])
                for elem in self.inputs.values():
                    tempListValues.append(elem[1])
                listValues = tuple(tempListValues)                    
                # print(listValues)
                funTemp = self.wrap
                self.button = Button(self.master, text=c.buttonName, command=lambda:funTemp(self.functions[c.functionName],listValues))
                self.button.pack()
            

            

def main(debug=False):
    gui_mm = metamodel_from_file('easgui.tx')
    
    gui_model = gui_mm.model_from_file('program.eui')
    
    
    root = Tk()
    my_gui = GUI(root)
    my_gui.interpret(gui_model)
    root.mainloop()

if __name__ == "__main__":
    main()