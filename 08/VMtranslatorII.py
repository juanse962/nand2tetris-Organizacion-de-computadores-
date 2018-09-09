import sys
from os import listdir
from os.path import isfile, isdir

#Esta función suma los valores que estan en las posiciones SP-1 y SP-2
def add():
    return ("@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n" + "D=D+M\n" + "M=D\n" + "@SP\n" + "M=M-1\n")

#Le resta al valor que esta en la posición SP-2 el valor de la posición SP-1
def sub():
    return ("@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n" + "M=M-D\n" + "@SP\n" + "M=M-1\n")

#Cambia el simbolo al valor de la posición SP-1
def neg():
    return ("@SP\n" + "A=M-1\n" + "M=-M\n")

#Compara logicamente si RAM[SP-1] == RAM[SP-2] y el resultado lo deja en el stack
def eq(cont):
    return ("@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n" + "D=D-M\n" + "@IF_TRUE" + str(cont) + "\n" + "D;JEQ\n" + "@SP\n" + "A=M-1\n" + "A=A-1\n" + "M=0\n" + "@END" + str(cont) + "\n" + "0;JMP\n" + "(IF_TRUE" + str(cont) + ")\n" + "@SP\n" + "A=M-1\n" + "A=A-1\n" + "M=-1\n" + "(END" + str(cont) + ")\n" + "@SP\n" + "M=M-1\n")

#Compara logicamente si RAM[SP-2] > RAM[SP-1], deja el resultado en el  stack
def gt(cont):
    return ("@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n" + "M=M-D\n" + "D=M\n" + "@IF_TRUE" + str(cont) + "\n" + "D;JGT\n" + "@SP\n" + "A=M-1\n" + "A=A-1\n" + "M=0\n" + "@END" + str(cont) + "\n" + "0;JMP\n" + "(IF_TRUE" + str(cont) + ")\n" + "@SP\n" + "A=M-1\n" + "A=A-1\n" + "M=-1\n" + "(END" + str(cont) + ")\n" + "@SP\n" + "M=M-1\n")

#Compara logicamente si RAM[SP-2] < RAM[SP-1], almacena el resultado en el stack
def lt(cont):
    return ("@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n" + "M=M-D\n" + "D=M\n" + "@IF_TRUE" + str(cont) + "\n" + "D;JLT\n" + "@SP\n" + "A=M-1\n" + "A=A-1\n" + "M=0\n" + "@END" + str(cont) + "\n" + "0;JMP\n" + "(IF_TRUE" + str(cont) + ")\n" + "@SP\n" + "A=M-1\n" + "A=A-1\n" + "M=-1\n" + "(END" + str(cont) + ")\n" + "@SP\n" + "M=M-1\n")

#Compara dos valores booleanos, RAM[SP-2] && RAM[SP-1], deja el resultado en el stack
def andComp():
    return ("@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n" + "M=D&M\n" + "@SP\n" + "M=M-1\n")

#Compara dos valores booleanos, RAM[SP-2] || RAM[SP-1], almacena el resultado en el stack
def orComp():
    return ("@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n" + "M=D|M\n" + "@SP\n" + "M=M-1\n")

#Modifica el valor booleano, del valor en RAM[SP-1], si es true se convierte en false y viceversa
def notComp():
    return ("@SP\n" + "A=M-1\n" + "M=!M\n")

#Mete una constante 'x' en el tope del stack
def pushConstant(x):
    return ("@" + str(x) + "\n" + "D=A\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n")

#Mete el valor de un argumento 'x' en el tope del stack, este valor se encuentra en el segmento de memoria argument
def pushArgument(x):
    return("@ARG\n" + "A=M\n" + "D=A\n" + "@" + str(x) + "\n" + "D=D+A\n" + "A=D\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n")

#Mete el valor de la posición 'x' del segmento that en el tope del stack
def pushThat(x):
    return("@THAT\n" + "A=M\n" + "D=A\n" + "@" + str(x) + "\n" + "D=D+A\n" + "A=D\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n")

#Mete el valor de la posición 'x' del segmento this en el tope del stack
def pushThis(x):
    return ("@THIS\n" + "A=M\n" + "D=A\n" + "@" + str(x) + "\n" + "D=D+A\n" + "A=D\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n")

#Mete el valor de la posición 'x' del segmento local en el tope del stack
def pushLocal(x):
    return ("@LCL\n" + "A=M\n" + "D=A\n" + "@" + str(x) + "\n" + "D=D+A\n" + "A=D\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n")

#Extrae el valor de RAM[SP-1] y lo almacena en el segmento argument en la posición 'x' de tal segmento de memoria
def popArgument(x):
    return ("@ARG\n" + "A=M\n" + "D=A\n" + "@" + str(x) + "\n" + "D=D+A\n" + "@R15\n" + "M=D\n" + "@SP\n" + "A=M-1\n" + "D=M\n" + "@R15\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M-1\n")

#Extrae el valor de RAM[SP-1] y lo almacena en el segmento that en la posición 'x' de tal segmento de memoria
def popThat(x):
    return("@THAT\n" + "A=M\n" + "D=A\n" + "@" + str(x) + "\n" + "D=D+A\n" + "@R15\n" + "M=D\n" + "@SP\n" + "A=M-1\n" + "D=M\n" + "@R15\n" + "A=M\n" + "M=D\n" +"@SP\n" + "M=M-1\n")

#Extrae el valor de RAM[SP-1] y lo almacena en el segmento this en la posición 'x' de tal segmento de memoria
def popThis(x):
    return ("@THIS\n" + "A=M\n" + "D=A\n" + "@" + str(x) + "\n" + "D=D+A\n" + "@R15\n" + "M=D\n" + "@SP\n" + "A=M-1\n" + "D=M\n" + "@R15\n" + "A=M\n" + "M=D\n" +"@SP\n" + "M=M-1\n")

#Extrae el valor de RAM[SP-1] y lo almacena en el segmento local en la posición 'x' de tal segmento de memoria
def popLocal(x):
    return ("@LCL\n" + "A=M\n" + "D=A\n" + "@" + str(x) + "\n" + "D=D+A\n" + "@R15\n" + "M=D\n" + "@SP\n" + "A=M-1\n" + "D=M\n" + "@R15\n" + "A=M\n" + "M=D\n" +"@SP\n" + "M=M-1\n")

#Extrae el valor de RAM[SP-1] y este valor lo almacena en la posición 'x' del segmento temp
def popTemp(x):
    return ("@5\n" + "D=A\n" + "@" + str(x) + "\n" + "D=D+A\n" + "@R15\n" + "M=D\n" + "@SP\n" + "A=M-1\n" + "D=M\n" + "@R15\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M-1\n")

#Mete en el tope del stack el valor de la posición 'x' del segmento temp
def pushTemp(x):
    return("@5\n" + "D=A\n" + "@" + str(x) + "\n" + "A=D+A\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n")

#Mete en tope del stack el valor del puntero this o that dependiendo del valor que asuma 'x'
def pushPointer(x):
    if (int(x) == 0):
        return("@THIS\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n")
    else:
        return("@THAT\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n")

#Extrae el valor de RAM[SP-1] y dependiendo del valor de 'x' lo almacena en la posición THIS o THAT
def popPointer(x):
    if (int(x) == 0):
        return("@SP\n" + "A=M-1\n" + "D=M\n" + "@THIS\n" + "M=D\n" + "@SP\n" + "M=M-1\n")
    else:
        return("@SP\n" + "A=M-1\n" + "D=M\n" + "@THAT\n" + "M=D\n" + "@SP\n" + "M=M-1\n")

#Mete en el tope del stack el valor de la posición 'x' del segmento static
def pushStatic(x,file):
    return("@" + str(file) + "." + str(x) + "\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n")

#Extrae el valor de RAM[SP-1] y lo almacena en la posición 'x' del segmento static
def popStatic(x,file):
    return("@" + str(file) + "." + str(x) + "\n" + "D=A\n" + "@R15\n" + "M=D\n" + "@SP\n" + "A=M-1\n" + "D=M\n" + "@R15\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M-1\n")

#Agrega una etiqueta de label según el nombre de etiqueta dado
def addLabel(label):
    return "(" + str(label) + ")\n"

#Agrega una sentencia If - Goto, y salta a la posición dada en caso de cumplirse la condición
def checkIfGoto(goto):
    return "@SP\n" + "A=M-1\n" + "D=M\n" + "@SP\n" + "M=M-1\n" + "@" + str(goto) + "\n" + "D;JNE\n"

#Agrega un Goto que salta a la posición especificada
def addGoto(goto):
    return "@" + str(goto) +"\n" + "0;JMP\n"

#Agrega un label con el nombre de la función, y n ceros a la pila dependiendo el numero de variables locales especificadas
def addFunction(function,nVars):
    funct =  "(" + str(function) + ")\n"
    while nVars != 0:
        funct += pushConstant(0)
        nVars -= 1
    return funct

#Esta función devuelve el resultado obtenido de la ejecución de la subrutina y lo deja en el tope de la pila
#Luego devuelve el control del programa a la función original desde donde fue llamada la subrutina
#Finalmente salta a la posición de retorno para continuar con la ejecución del programa original
def addReturn():
    return "@LCL\n" + "D=M\n" + "@R13\n" + "M=D\n" + getSegment("R14",int(5)) + "@SP\n" + "A=M-1\n" + "D=M\n" + "@ARG\n" + "A=M\n" + "M=D\n" + "@ARG\n" + "D=M+1\n" + "@SP\n" + "M=D\n" + getSegment("THAT",int(1)) + getSegment("THIS",int(2)) + getSegment("ARG",int(3)) + getSegment("LCL",int(4)) + "@R14\n" + "A=M\n" + "0;JMP\n"

#Esta función asigna al segmento dado el elemento *(FRAME - num)
def getSegment(segment,num):
    return "@R13\n" + "D=M\n" + "@" + str(num) + "\n" + "D=D-A\n" + "A=D\n" + "D=M\n" + "@" + str(segment) + "\n" + "M=D\n"

#Esta función se encarga de llamar a una subrutina de forma que almacena los valores actuales de los segmentos de memoria y
#La posición a la que debe retornar el programa despues de finalizar la ejecución de la subrutina
def addCall(funct,nArgs,cont):
    return  "@return" + str(cont) + "\n" + "D=A\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n" + pushSegment("LCL") + pushSegment("ARG") + pushSegment("THIS") + pushSegment("THAT") + "@5\n" + "D=A\n" + "@SP\n" + "A=M\n" + "D=A-D\n" + "@" + str(nArgs) + "\n"+ "D=D-A\n" + "@ARG\n" + "M=D\n" + "@SP\n" + "D=M\n" + "@LCL\n" + "M=D\n" + addGoto(funct) + addLabel("return" + str(cont))

#Esta función se encarga de pushear el segmento de memoria dado en la pila
def pushSegment(segment):
    return "@" + str(segment) + "\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n"

"""Esta función inicia con la ejecución del programa, cuando recibe un archivo que es procesado
linea por linea, y genera un archivo de respuesta .asm en donde se encuentra la traducción a lenguaje ensamblador
del archivo pasado como parametro de entrada"""
def VMTranslate(vmFile,asmFile,file):
    line = vmFile.readline()
    cont = 1
    while line != '':
        lineParser(line,asmFile,cont,file)
        line = vmFile.readline()
        asmFile.write("//Linea #" + str(cont) + ": " + line)
        cont += 1

    vmFile.close()

"""Esta función recibe como parametro de entrada una linea, esta linea es analizada y
traducida a lenguaje ensamblador, la traducción de la linea es escrita en el archivo de respuesta"""
def lineParser(line,asmFile,cont,file):
    if not line.startswith("//"):
        words = line.split(" ")
        if line.startswith("push"):
            if(words[1] == "static"):
                asmFile.write(pushStatic(words[2].replace("\n",""),file))
            elif(words[1] == "pointer"):
                asmFile.write(pushPointer(words[2].replace("\n","")))
            elif(words[1] == "constant"):
                asmFile.write(pushConstant(words[2].replace("\n","").replace("//","")))
            elif(words[1] == "argument"):
                asmFile.write(pushArgument(words[2].replace("\n","")))
            elif(words[1] == "local"):
                asmFile.write(pushLocal(words[2].replace("\n","")))
            elif(words[1] == "that"):
                asmFile.write(pushThat(words[2].replace("\n","")))
            elif(words[1] == "temp"):
                asmFile.write(pushTemp(words[2].replace("\n","")))
            else:
                asmFile.write(pushThis(words[2].replace("\n","")))

        elif line.startswith("pop"):
            if(words[1] == "static"):
                asmFile.write(popStatic(words[2].replace("\n",""),file))
            elif(words[1] == "pointer"):
                asmFile.write(popPointer(words[2].replace("\n","")))
            elif(words[1] == "argument"):
                asmFile.write(popArgument(words[2].replace("\n","")))
            elif(words[1] == "local"):
                asmFile.write(popLocal(words[2].replace("\n","")))
            elif(words[1] == "that"):
                asmFile.write(popThat(words[2].replace("\n","")))
            elif(words[1] == "temp"):
                asmFile.write(popTemp(words[2].replace("\n","")))
            else:
                asmFile.write(popThis(words[2].replace("\n","")))

        elif line.startswith("add"):
            asmFile.write(add())
        elif line.startswith("sub"):
            asmFile.write(sub())
        elif line.startswith("neg"):
            asmFile.write(neg())
        elif line.startswith("eq"):
            asmFile.write(eq(cont))
        elif line.startswith("gt"):
            asmFile.write(gt(cont))
        elif line.startswith("lt"):
            asmFile.write(lt(cont))
        elif line.startswith("and"):
            asmFile.write(andComp())
        elif line.startswith("or"):
            asmFile.write(orComp())
        elif line.startswith("not"):
            asmFile.write(notComp())
        #Aqui agregue los comandos correspondientes a este proyecto
        #Para generar el código assembler correspondiente a cada comando
        elif line.startswith("label"):
            asmFile.write(addLabel(words[1].replace("\n","")))
        elif line.startswith("if-goto"):
            asmFile.write(checkIfGoto(words[1].replace("\n","")))
        elif line.startswith("goto"):
            asmFile.write(addGoto(words[1].replace("\n","")))
        elif line.startswith("function"):
            asmFile.write(addFunction(words[1],int(words[2].replace("\n",""))))
        elif line.startswith("call"):
            asmFile.write(addCall(words[1],int(words[2].replace("\n","")),cont))
        elif line.startswith("return"):
            asmFile.write(addReturn())

#Esta función se ejecuta cuando se le pasa como parametro al programa una carpeta
# Y la carpeta contiene el archivo Sys.vm
def inicio(asmFile):
    asmFile.write("@256\n" + "D=A\n" + "@SP\n" + "M=D\n")
    asmFile.write(addCall("Sys.init",0,0))

#Esta función inicia con la ejecución del programa, leyendo la carpeta o el archivo
def lecturaDatos():
    if (len(sys.argv) <= 1):
        print("Por favor, ingrese un archivo o un directorio")
    else:
        path = sys.argv[1]
        if isdir(path):
            nameFile = path + path[:len(path)-1] + ".asm"
            asmFile = open(nameFile,'w')
            dirs = listdir(path)
            for file in dirs:
                if (file[len(file)-2:] == "vm" and file[:len(file)-3:] == "Sys"):
                    inicio(asmFile)
            for file in dirs:
                if (file[len(file)-2:] == "vm"):
                    nameVMFile = path + file
                    vmFile = open(nameVMFile)
                    VMTranslate(vmFile,asmFile,file[:len(file)-3:])

            asmFile.write("(INFINITE_LOOP)\n" + "@INFINITE_LOOP\n" + "0;JMP\n")
            asmFile.close()
        else:
            nameFile = path[:len(path)-2] + "asm"
            asmFile = open(nameFile,'w')
            vmFile = open(path)
            VMTranslate(vmFile,asmFile,nameFile[:len(nameFile)-4:])
            asmFile.write("(INFINITE_LOOP)\n" + "@INFINITE_LOOP\n" + "0;JMP\n")
            asmFile.close()

lecturaDatos()