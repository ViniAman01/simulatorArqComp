#!/bin/python3

from typing import List #Permite declaração de tipagem de listas

B_R = "banco_registradores.txt" #Constantes para os nomes dos arquivos
EN = "entrada.txt"
U_C = "unidade_controle.txt"
M_R = "memoria_ram.txt"

def add(a,b): return a+b #Funções aritmeticas/logicas para executar instruções
def sub(a,b): return a-b
def anD(a,b): return a & b
def oR(a,b): return a | b
def load(regX,memX): 
    reg = GSRegMem(B_R,regX)
    mem = GSRegMem(M_R,memX) 
    reg.setRegMem(mem.getRegMem())
def store(memX,regX):
    mem = GSRegMem(M_R,memX) 
    reg = GSRegMem(B_R,regX)
    mem.setRegMem(reg.getRegMem())

dictInstructions = { #Dicionario contento as intruções a serem interpretadas
        "LOAD": load,
        "STORE": store,
        #"MOVE": move,
        "ADD": add,
        "SUB": sub,
        "AND": anD,
        "OR": oR,
        #"BRANCH": branch,
        #"BZERO": bzero,
        #"BNEG": bneg,
        #"NOP": nop,
        #"HALT": halt
        }

tupleRegisters = ( #Tupla contendo configuração inicial dos registradores
        "R0: 0\n",
        "R1: 0\n",
        "R2: 0\n",
        "R3: 0\n",
        )


class IOFiles: #Classe para manipulação de arquivos
    def __init__(self, name: str):
        self.name = name

    def readTxt(self): #Retorna conteúdo do arquivo em str
    #FAZER TRATAMENTO DE ERROS
        with open(self.name) as f:
            return f.readlines()

    def writeTxt(self, value: List):
        with open(self.name,"w+") as f:
            f.writelines(value)

startM_R = IOFiles(M_R)
memList = []
for i in range(33):
    memList.append(str(i)+": \n")

startM_R.writeTxt(memList)

class GSRegMem(IOFiles): #Classe que opera sobre os registradores e ram, herda IOFiles
    def __init__(self, name: str, adr: int): #Nome do arquivo + endereço reg/ram
        self.adr = adr

        super().__init__(name)
         
    def getRegMem(self):
        auxTxt = self.readTxt()
        if auxTxt:
            return int(auxTxt[self.adr][4:]) #Retorna inteiro referente ao conteudo do endereço(adr)
        else:
            print("Banco vazio!")
            return False

    def setRegMem(self,value):
        auxTxt = self.readTxt() #Pega atual estado dos registradores
        if not auxTxt: #Caso o arquivo esteja vazio, a tupla contendo os registrados é usada
            auxTxt = list(tupleRegisters)

        auxTxt[self.adr] = auxTxt[self.adr][:4] + str(value)  + auxTxt[self.adr][-1:] #Concatena o valor desejado com o começo e fim da linha do reg/mem
        self.writeTxt(auxTxt)

def getAdr(name: str):
    if name.count("R"):
        return int(name[1])
    else:
        return int(name)

def getInstructions(inputTxt: List[str]): #Splita as instruções em uma lista
    instructionsInput = inputTxt.splitlines()
    return instructionsInput

def execInstructionAL(instructionLine: str):    #Executa determinada instrução da ALU contendo dois valores
    instructionList = instructionLine.split(" ")    #Divide a linha em vários tokens
    numTokens = len(instructionList)-1      #Contabiliza o número de parametros

    #A partir daqui teremos diferentes grupos de instruções sendo executados de acordo com seu número de parametros

    if numTokens == 3:  #Com 3 parametros sabe-se que será executado uma instrução lógica/aritmética
        function = dictInstructions[instructionList[0]]     #O primeiro token define a função, que será buscada no dicionario de instruções
        rA = GSRegMem(B_R, int(instructionList[1][1]))   #Criamos um objeto referente ao registrador que receberá o valor da operação
        rB = GSRegMem(B_R, int(instructionList[2][1])).getRegMem()   #Como o segundo e terceiro regs contem os valore que serão operados, buscamos seus valores
        rC = GSRegMem(B_R, int(instructionList[3][1])).getRegMem()

        rA.setRegMem(function(rB,rC))   #Seta o valor no arquivo B_R referente a função executada

    if numTokens == 2: 
        function = dictInstructions[instructionList[0]]
        function(getAdr(instructionList[1]), getAdr(instructionList[2]))

txt = IOFiles(EN).readTxt()
execInstructionAL(txt[0])
