from errorMessages import TextXSemanticError, TextXRuntimeError
import numpy as np
import inspect 
class bcolors:
    HEADER = '\u001b[35;1m'
    BLUE = '\u001b[34;1m'
    OKGREEN = '\u001b[32;1m'
    RED = '\033[91m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def procMessage(message, color , line, col):
    color_flag = True    
    if color_flag:
        messageColor = "\n"+message +"\n\t" + color + "\nIn:\n\t[line:"+str(line)+", col:"+str(col)+"]"+bcolors.ENDC 
    else:
        messageColor = "\n"+message +"\n\t" + "\nIn:\n\t[line:"+str(line)+", col:"+str(col)+"]" 
        
    return messageColor
    
def underlineStr(text):
    return bcolors.UNDERLINE+text+bcolors.ENDC


def wrap(func,args):
    argsList = []
    outlist = []
    
    for value in args:
        #ARREGLAR PARA VERIFICAR CAMPO VACIOS DE TODOS ANTES
        if value[1] != "BOOLINPUT":
            if value[0].get()=='' and value[1] != 'OUTPUT':
                lineInput,colInput = value[2]
                messageError ="Empy data on entry defined at:\n\t{} {}".format(value[1],value[3])
                message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                raise TextXRuntimeError(message,line=lineInput,col=colInput)
      
        if value[1] == 'BOOLINPUT':
            # print(inspect.getmembers(value[0].variable))
            if "selected" in value[0].state():
                argsList.append(True)
            else:
                argsList.append(False)
                
        if value[1] == 'INTINPUT':
            try:
                if "." in value[0].get():
                    argsList.append(int(float(value[0].get())))
                else:
                    argsList.append(int(value[0].get()))
            except ValueError:
                lineInput,colInput = value[2]
                messageError ="{} data type declared but another type was used:\n\t{} {}".format(value[1],value[1],value[3])
                message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                raise TextXRuntimeError(message,line=lineInput,col=colInput)
                
        if value[1] == 'MATRIXINPUT':
            try:
                tempList=[]
                tempMatrix = value[0].get().split(';')
                for sublist in tempMatrix:
                    tempSplit = sublist.split(',')
                    tempSplit = [int(x) for x in tempSplit]
                    tempList.append(tempSplit)
                tempList = np.array(tempList)
                argsList.append(tempList)
            except:
                lineInput,colInput = value[2]
                messageError ="{} data type declared but another type was used:\n\t{} {}".format(value[1],value[1],value[3])
                message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                raise TextXRuntimeError(message,line=lineInput,col=colInput)
                
        if value[1] == 'DECIMALINPUT':
            try:
                argsList.append(float(value[0].get()))
            except ValueError:
                lineInput,colInput = value[2]
                messageError ="{} data type declared but another type was used: \n\t{} {}".format(value[1],value[1],value[3])
                message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                raise TextXRuntimeError(message,line=lineInput,col=colInput)
        
        if value[1] == 'LISTINTINPUT':
            try:
                tempList = value[0].get().split(',')
                tempList = [int(i) for i in tempList]
                argsList.append(tempList)
            except:
                lineInput,colInput = value[2]
                messageError ="{} data type declared but another type was used: \n\t{} {}".format(value[1],value[1],value[3])
                message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                raise TextXRuntimeError(message,line=lineInput,col=colInput)
                
        if value[1] == 'LISTIDECIMALINPUT':
            try:
                tempList = value[0].get().split(',')
                tempList = [float(i) for i in tempList]
                argsList.append(tempList)
            except:
                lineInput,colInput = value[2]
                messageError ="{} data type declared but another type was used: \n\t{} {}".format(value[1],value[1],value[3])
                message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                raise TextXRuntimeError(message,line=lineInput,col=colInput)
        if value[1] == 'LISTSTRINGINPUT':
            try:
                tempList = value[0].get().split(',')
                tempList = [str(i) for i in tempList]
                argsList.append(tempList)
            except:
                lineInput,colInput = value[2]
                messageError ="{} data type declared but another type was used: \n\t{} {}".format(value[1],value[1],value[3])
                message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                raise TextXRuntimeError(message,line=lineInput,col=colInput)
        if value[1] == 'STRINGINPUT':
            try:
                argsList.append(str(value[0].get()))
            except:
                lineInput,colInput = value[2]
                messageError ="{} data type declared but another type was used: \n\t{} {}".format(value[1],value[1],value[3])
                message = procMessage(messageError,bcolors.BLUE,lineInput,colInput)
                raise TextXRuntimeError(message,line=lineInput,col=colInput)
                
        if value[1] == 'OUTPUT':
             outlist.append(value[0])
             
    #Declare function with arguments of input in entries
    try:         
        result = func(*tuple(argsList))
    except:
        raise TextXRuntimeError(message="INTERNAL ERROR OF FUNCTION")

    
    if len(outlist)>1:
        if type(result)!=tuple:
            raise TextXRuntimeError(message="INCOMPATIBLE: different number of output results than OUTPUT declarated")
        if len(result) != len(outlist) :
            raise TextXRuntimeError(message="INCOMPATIBLE: different number of values at return and defined outputs")
            
        else:
            for i in range(len(outlist)):
                outlist[i].configure(state="normal")
                outlist[i].delete(0,"end")
                outlist[i].insert(0,str(result[i]))
    
    if len(outlist)==1:
        if type(result)==tuple: 
            raise TextXRuntimeError(message="INCOMPATIBLE: imported function does not return more than one result")
        else:
            outlist[0].configure(state="normal")
            outlist[0].delete(0,"end")
            outlist[0].insert(0,str(result))
