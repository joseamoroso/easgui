# -*- coding: utf-8 -*-
"""
Created on Thu May 14 01:06:33 2020

@author: Jose Amoroso
"""


from textx import metamodel_from_file
from errorMessages import TextXSemanticError, TextXRuntimeError
from tkinter import Tk,Button,Label,Entry,LEFT,HORIZONTAL,BOTH,TOP,X,Frame,RAISED,Checkbutton,IntVar
from tkinter import ttk
from functionCaller import wrap, procMessage,bcolors,underlineStr
from functools import partial
import inspect
import numpy as np
import sys



############    Semantics         ##############################   
def checkSemantics(model, metamodel):
    modelCommands = model.commands
    inputIDList=[]
    importedFunctions = []
    for command in modelCommands:
        line,col = model._tx_parser.pos_to_linecol(command._tx_position)
        if command.__class__.__name__ == "ImportFunction":
            importedFunctions.append(command.newFunctionName)

        if command.__class__.__name__ == "CreateFunction":
            #CHECK REPEATED IDS -> INPUTS
            for inputs in command.parameter:
                inputValue = inputs.inputName
                inputType = inputs.inputType
                if inputValue in inputIDList:
                    lineInput,colInput = model._tx_parser.pos_to_linecol(inputs._tx_position)
                    messageError ="Repeated inputs IDs, check it is not used before.\n\t{} {}".format(
                                    underlineStr(inputValue),underlineStr(inputType))
                    message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                    raise TextXSemanticError(message,line=line,col=col,filename=model._tx_filename)
                inputIDList.append((inputValue))
            #Check if function is not declared before
            if command.functionName not in importedFunctions:
                lineInput,colInput = model._tx_parser.pos_to_linecol(command._tx_position)
                messageError ="Used function was not imported before.\n\t{}".format(
                                underlineStr(command.functionName ))
                message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                raise TextXSemanticError(message,line=line,col=col,filename=model._tx_filename)

                
################################################################

##########      Processors      ################################
def createWindowProcessor(createWindowCmd):
  # If steps is not given, set it do default 1 value.
   if len(createWindowCmd.coor)==1:
       createWindowCmd.coor.append(createWindowCmd.coor[0])
   if len(createWindowCmd.coor)==0:
       createWindowCmd.coor = [500,500]

################################################################
        
class GUI:
    def __init__(self,master):
        self.functions = {}
        self.master = master
        self.functionFlag = False
        self.allButton ={}

    def interpret(self, model):
        for c in model.commands:
            if c.__class__.__name__ == "ImportFunction": 
                package = c.fileName
                name = c.functionName
                try:
                    imported = getattr(__import__(package, fromlist=[name]), name)
                    self.functions[c.newFunctionName]=imported
                except ModuleNotFoundError:
                    lineInput,colInput = model._tx_parser.pos_to_linecol(c._tx_position)
                    messageError ="FILE {} NOT FOUND".format(underlineStr(package))
                    message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                    raise TextXRuntimeError(message,line=lineInput,col=colInput,filename=model._tx_filename)
                    sys.exit()
                except AttributeError:
                    lineInput,colInput = model._tx_parser.pos_to_linecol(c._tx_position)
                    messageError ="FUNCTION {} NOT FOUND IN {}".format(underlineStr(name),underlineStr(package))
                    message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                    raise TextXRuntimeError(message,line=lineInput,col=colInput,filename=model._tx_filename)
                    sys.exit()

            if c.__class__.__name__ == "CreateWindow": 
                    self.master.title(c.windowID)
                    newSize = "{}x{}".format(c.coor[0],c.coor[1])
                    self.master.geometry(newSize)

            if c.__class__.__name__ == "CreateFunction":
                self.inputs = {}
                self.listValues = None
                self.button=None
                #Create frame for each function
                self.frame = Frame(self.master, relief=RAISED, borderwidth=1)
                self.frame.pack(fill=BOTH, expand=True)
                self.tempListValues = []


                #Insert line horizontal
                if (self.functionFlag):
                    self.separ = ttk.Separator(self.master, orient=HORIZONTAL)
                    self.separ.pack(side=TOP,fill=BOTH, expand=True)
                self.functionFlag = True
                ######################################################################
                ########################## Create inputs #############################
                ######################################################################
                for inputs in c.parameter:
                    self.frameInner = Frame(self.frame, relief=RAISED)
                    self.frameInner.pack(fill=BOTH, expand=True)
                    line,col= model._tx_parser.pos_to_linecol(inputs._tx_position)
                    self.inputPosition = (line,col)
                    
                    self.inputType = inputs.inputType
                    if self.inputType == 'OUTPUT':
                        self.label = Label(self.frameInner, text=inputs.inputName+':', anchor='w',font=("Calibri", 10, "bold underline"))
                        self.entry = Entry(self.frameInner,state='disabled')
                        self.label.pack(side=LEFT,padx=5, pady=5)
                        self.entry.pack(side=LEFT,fill=X,expand=True,padx=10)
                        self.tempListValues.append((self.entry,self.inputType,self.inputPosition,inputs.inputName))

                        
                    elif self.inputType == 'BOOLINPUT':
                        self.label = Label(self.frameInner, text=inputs.inputName+':', anchor='w')
                        self.label.pack(side=LEFT,padx=5, pady=5)
                        self.checkvar = IntVar() 
                        self.Checkbutton = ttk.Checkbutton(self.frameInner)
                        self.Checkbutton.state(['!alternate'])
                        self.Checkbutton.pack(side=LEFT,fill=X,padx=10)
                        self.tempListValues.append((self.Checkbutton,self.inputType,self.inputPosition,inputs.inputName))

                    else:
                        self.label = Label(self.frameInner, text=inputs.inputName+':', anchor='w')
                        self.entry = Entry(self.frameInner)
                        self.label.pack(side=LEFT,padx=5, pady=5)
                        self.entry.pack(side=LEFT,fill=X,expand=True,padx=10)
                        self.tempListValues.append((self.entry,self.inputType,self.inputPosition,inputs.inputName))



                ######################################################################
                ################### Create button with function ######################
                ######################################################################
                self.listValues = tuple(self.tempListValues)
                self.button = Button(self.frame, text=c.buttonName)
                self.button.configure(command=partial(wrap,self.functions[c.functionName],self.listValues))
                self.button.pack(pady=5)
                ######################################################################
            

def main(debug=False):

    
    gui_mm = metamodel_from_file('tx_easgui/easgui.tx')
    
    gui_mm.register_model_processor(checkSemantics)
    gui_mm.register_obj_processors({'CreateWindow': createWindowProcessor})

    
    gui_model = gui_mm.model_from_file('program.eui')
    # gui_model = gui_mm.model_from_file(str(sys.argv[1]))

    
    
    root = Tk()
    my_gui = GUI(root)
    my_gui.interpret(gui_model)
    
    root.mainloop()

if __name__ == "__main__":
    main()