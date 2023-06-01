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
def load(regAdr,memAdr): 
    reg = GSRegMem(B_R,regAdr)
    mem = GSRegMem(M_R,memAdr) 
    reg.setRegMem(mem.getRegMem())
def store(memAdr,regAdr):
    mem = GSRegMem(M_R,memAdr) 
    reg = GSRegMem(B_R,regAdr)
    mem.setRegMem(reg.getRegMem())
def move(regValueA,regValueB):
    regA = GSRegMem(B_R,regValueA)
    regB = GSRegMem(B_R,regValueB)
    regA.setRegMem(regB.getRegMem())
def branch(adr): return adr
def bneg(adr,cpuInfo): if cpuInfo.alu < 0: cpuInfo.pc = adr
def bzero(adr,cpuInfo): if cpuInfo.alu == 0: cpuInfo.pc = adr
def halt(cpuInfo): cpuInfo.pc = 32

dictInstructions = { #Dicionario contento as intruções a serem interpretadas
        "LOAD": load,
        "STORE": store,
        "MOVE": move,
        "ADD": add,
        "SUB": sub,
        "AND": anD,
        "OR": oR,
        "BRANCH": branch,
        "BZERO": bzero,
        "BNEG": bneg,
        #"NOP": nop,
        #"HALT": halt
        }

tupleRegisters = ( #Tupla contendo configuração inicial dos registradores
        "R0: 0\n",
        "R1: 0\n",
        "R2: 0\n",
        "R3: 0\n",
        )

class CPUInfo:
    def __init__(pc: int, ir=None, alu=None):
        self.pc = pc
        self.alu = alu
        self.ir = ir

class IOFiles: #Classe para manipulação de arquivos
    def __init__(self, name: str):
        self.name = name

    def readTxt(self): #Retorna conteúdo do arquivo em str
        try:
            with open(self.name,"r+") as f:
                return f.readlines()
        except IOError:
            print("Erro na leitura do arquivo!")

    def writeTxt(self, value: List):    #Escreve no arquivo self.name
        try:
            with open(self.name,"w+") as f:
                f.writelines(value)
        except IOError:
            print("Erro na escrita do arquivo!")


class GSRegMem(IOFiles): #Classe que opera sobre os registradores e ram, herda IOFiles
    def __init__(self, name: str, adr: int): #Nome do arquivo + endereço reg/ram
        self.adr = adr

        super().__init__(name)
         
    def getRegMem(self):
        auxTxt = self.readTxt()
        lineTxt = auxTxt[self.adr].split(" ")
        if auxTxt:
            return int(lineTxt[1]) #Retorna inteiro referente ao conteudo do endereço(adr)
        else:
            print("Banco vazio!")
            return False

    def setRegMem(self,value):
        auxTxt = self.readTxt() #Pega atual estado dos registradores ou memoria
        lineTxt = auxTxt[self.adr].split(" ")   #Split a linha do endereço em uma lista
#       if not auxTxt: #Caso o arquivo esteja vazio, a tupla contendo os registrados é usada
#           if self.name == B_R:
#               auxTxt = list(tupleRegisters)
#           if self.name == M_R:
#               startM_R = IOFiles(M_R)
#                memList = []
#                for i in range(33):
#                    memList.append(str(i)+": \n")

#                startM_R.writeTxt(memList)

        auxTxt[self.adr] = lineTxt[0] + " " + str(value) + "\n" #Concatena o valor com os resto da string e adiciona ao respectivo endereço
        self.writeTxt(auxTxt)   #Escreve a lista no arquivo

def getAdr(name: str):      #Pega o endereço(inteiro) de um registrador ou memoria
    if name.count("R"):
        return int(name[1])
    else:
        return int(name)

def execInstruction(instructionLine: str, cpuInfo):    #Executa determinada instrução da ALU contendo dois valores
    instructionList = instructionLine.split(" ")    #Divide a linha em vários tokens
    numTokens = len(instructionList)-1      #Contabiliza o número de parametros

    #A partir daqui teremos diferentes grupos de instruções sendo executados de acordo com seu número de parametros
    cpuInfo.ir = instructionList[0] #Atualiza o valor do IR

    if numTokens == 3:  #Com 3 parametros sabe-se que será executado uma instrução lógica/aritmética
        function = dictInstructions[instructionList[0]]     #O primeiro token define a função, que será buscada no dicionario de instruções
        rA = GSRegMem(B_R, int(instructionList[1][1]))   #Criamos um objeto referente ao registrador que receberá o valor da operação
        rB = GSRegMem(B_R, int(instructionList[2][1])).getRegMem()   #Como o segundo e terceiro regs contem os valore que serão operados, buscamos seus valores
        rC = GSRegMem(B_R, int(instructionList[3][1])).getRegMem()
        
        cpuInfo.alu = function(rB,rC)

        rA.setRegMem(cpuInfo.alu)   #Seta o valor no arquivo B_R referente a função executada

    if numTokens == 2: 
        function = dictInstructions[instructionList[0]]
        cpuInfo.alu = function(getAdr(instructionList[1]), getAdr(instructionList[2]))

    if numTokens == 1:
        function = dictInstructions[instructionList[0]]
        cpuInfo.alu = function(instructionList[1],cpuInfo)

    if numTokens == 0:


instructions = IOFiles(EN).readTxt()
cpuInfo = CPUInfo(0)
while cpuInfo.pc < 32:
    execInstruction(instructions[cpuInfo.pc],cpuInfo)
