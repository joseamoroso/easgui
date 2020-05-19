# -*- coding: utf-8 -*-
"""
Created on Thu May 14 01:06:33 2020

@author: Jose Amoroso
"""


from textx import metamodel_from_file,TextXSyntaxError,TextXSemanticError
from tkinter import Tk,Button,Label,Entry,Canvas,LEFT, RIGHT,HORIZONTAL,BOTH,TOP,BOTTOM,X,Frame,RAISED
from tkinter import ttk
from functools import partial
import inspect

class bcolors:
    HEADER = '\u001b[35;1m'
    OKBLUE = '\u001b[34;1m'
    OKGREEN = '\u001b[32;1m'
    RED = '\u001b[31;1m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


    
def procMessage(message, color , line, col, tupleInput):
    messageColor = "\n"+message +"\n\t" + color+tupleInput[1]+" "+tupleInput[0]+"\033[0m" + "\nIn:\n\t[line:"+str(line)+", col:"+str(col)+"]" 
    return messageColor
    
def check_some_semantics(model, metamodel):
    modelCommands = model.commands
    inputIDList=[]
    for command in modelCommands:
        if command.__class__.__name__ == "CreateFunction":
            #CHECK REPEATED IDS -> INPUTS
            for inputs in command.parameter:
                inputValue = inputs.inputName
                inputType = inputs.inputType
                if inputValue in inputIDList:
                    line,col = model._tx_parser.pos_to_linecol(command._tx_position)
                    lineInput,colInput = model._tx_parser.pos_to_linecol(inputs._tx_position)
                    messageError ="Repeated inputs IDs, check it is not used before."
                    messageComp = inputValue,inputType
                    message = procMessage(messageError,bcolors.RED,lineInput,colInput,messageComp)
                    raise TextXSemanticError(message,line=line,col=col,filename=model._tx_filename)
                inputIDList.append((inputValue))
        

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
    print(result)
    
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
                outlist[i].configure(state="normal")
                outlist[i].delete(0,"end")
                outlist[i].insert(0,str(result[i]))
                
    if len(outlist)==1:
        outlist[0].configure(state="normal")
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
                try:
                    self.master.title(c.windowID)
                except:
                    pass
                try:
                    newSize = "{}x{}".format(c.coor[0],c.coor[1])
                    self.master.geometry(newSize)
                except:
                    pass
                try:
                    newSize = "{}x{}".format(c.coor[0],c.coor[0])
                    self.master.geometry(newSize)
                except:
                    pass


            if c.__class__.__name__ == "CreateFunction":
                # raise TextXSyntaxError("Putito")
                self.inputs = {}
                self.listValues = None
                self.button=None
                #Create frame for each function
                self.frame = Frame(self.master, relief=RAISED, borderwidth=1)
                self.frame.pack(fill=BOTH, expand=True)

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
                    self.inputType = inputs.inputType

                    if self.inputType == 'OUTPUT':
                        self.label = Label(self.frameInner, text=inputs.inputName+':', anchor='w',font=("Calibri", 10, "bold underline"))
                        self.entry = Entry(self.frameInner,state='disabled')
                    else:
                        self.label = Label(self.frameInner, text=inputs.inputName+':', anchor='w')
                        self.entry = Entry(self.frameInner)
                        
                    self.inputs[inputs.inputName]=(self.label,(self.entry,self.inputType))
                    self.label.pack(side=LEFT,padx=5, pady=5)
                    self.entry.pack(side=LEFT,fill=X,expand=True,padx=10)
                ######################################################################
                ################### Create button with function ######################
                ######################################################################
                self.tempListValues = []
                for elem in self.inputs.values():
                    self.tempListValues.append(elem[1])
                self.listValues = tuple(self.tempListValues)
                self.button = Button(self.frame, text=c.buttonName)
                # self.button.configure(command=lambda: wrap(self.functions[c.functionName],self.listValues))
                self.button.configure(command=partial(wrap,self.functions[c.functionName],self.listValues))
                self.button.pack(pady=5)
                ######################################################################
            

            


gui_mm = metamodel_from_file('easgui.tx')

gui_mm.register_model_processor(check_some_semantics)

gui_model = gui_mm.model_from_file('program.eui')



root = Tk()
my_gui = GUI(root)
my_gui.interpret(gui_model)

root.mainloop()
