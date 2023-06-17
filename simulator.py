#!/bin/python3

from typing import List #Permite declaração de tipagem de listas
import os

B_R = "banco_registradores.txt" #Constantes para os nomes dos arquivos
EN = "entrada.txt"
U_C = "unidade_controle.txt"
M_R = "memoria_ram.txt"

def add(a,b): return a+b #Funções aritmeticas/logicas para executar instruções
def sub(a,b): return a-b
def anD(a,b): return a & b
def oR(a,b): return a | b
def load(regAdr,memAdr): #Função de carregamento de dados da memoria para os registradores 
    reg = GSRegMem(B_R,regAdr)
    mem = GSRegMem(M_R,memAdr) 
    memVal = mem.getRegMem()
    reg.setRegMem(memVal)
    return memVal
def store(memAdr,regAdr):
    mem = GSRegMem(M_R,memAdr) 
    reg = GSRegMem(B_R,regAdr)
    regVal = reg.getRegMem()
    mem.setRegMem(regVal)
    return regVal
def move(regValueA,regValueB):
    regA = GSRegMem(B_R,regValueA)
    regB = GSRegMem(B_R,regValueB)
    regBVal = regB.getRegMem()
    regA.setRegMem(regBVal)
    return regBVal
def branch(adr,cpuInfo): cpuInfo.pc = adr
def bneg(adr,cpuInfo): 
    if cpuInfo.alu < 0: 
        cpuInfo.pc = adr
def bzero(adr,cpuInfo): 
    if cpuInfo.alu == 0: 
        cpuInfo.pc = adr
def halt(): pass
def nop(): pass

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
        "NOP\n": nop,
        "HALT\n": halt
        }

class CPUInfo:
    def __init__(self,pc: int, ir: str, alu=0):
        self.pc = pc
        self.alu = alu
        self.ir = ir

class IOFiles: #Classe para manipulação de arquivos
    def __init__(self, name: str):
        self.name = name
        
        if not os.path.exists(self.name): #Caso o arquivo não exista ele vai ser criado e inicializado
            startText = []
            if self.name == B_R:
                for i in range(4):
                    startText.append("R"+str(i)+": 0\n")

            self.writeTxt(startText)

    def readTxt(self): #Retorna conteúdo do arquivo em str
        try:
            with open(self.name) as f:
                return f.readlines()
        except IOError:
            print("Erro na leitura do arquivo!")

    def writeTxt(self, value: List):    #Escreve no arquivo self.name
        try:
            with open(self.name,"w") as f:
                f.writelines(value)
        except IOError:
            print("Erro na escrita do arquivo!")


class GSRegMem(IOFiles): #Classe que opera sobre os registradores e ram, herda IOFiles
    def __init__(self, name: str, adr: int): #Nome do arquivo + endereço reg/ram
        self.adr = adr

        super().__init__(name)
         
    def getRegMem(self):
        auxTxt = self.readTxt()
        if auxTxt:
            lineTxt = auxTxt[self.adr].split(" ")
            return int(lineTxt[1]) #Retorna inteiro referente ao conteudo do endereço(adr)
        else:
            print("Banco vazio!")
            return False

    def setRegMem(self,value):
        auxTxt = self.readTxt() #Pega atual estado dos registradores ou memoria
        if auxTxt:
            lineTxt = auxTxt[self.adr].split(" ")   #Split a linha do endereço em uma lista
            auxTxt[self.adr] = lineTxt[0] + " " + str(value) + "\n" #Concatena o valor com os resto da string e adiciona ao respectivo endereço
            self.writeTxt(auxTxt)   #Escreve a lista no arquivo

def getAdr(name: str):      #Pega o endereço(inteiro) de um registrador ou memoria
    if name.count("R"):
        return int(name[1])
    else:
        return int(name)

def execInstruction(instructionLine: str, cpuInfo):    #Executa determinada instrução da ALU contendo dois valores
    instructionList = instructionLine.split(" ")    #Divide a linha em vários tokens
    cpuInfo.ir = instructionList[1] #Atualiza o valor do IR
    numTokens = len(instructionList)-2      #Contabiliza o número de parametros

    #A partir daqui teremos diferentes grupos de instruções sendo executados de acordo com seu número de parametros

    if numTokens == 3:  #Com 3 parametros sabe-se que será executado uma instrução lógica/aritmética
        function = dictInstructions[instructionList[1]]     #O primeiro token define a função, que será buscada no dicionario de instruções
        rA = GSRegMem(B_R, int(instructionList[2][1]))   #Criamos um objeto referente ao registrador que receberá o valor da operação
        rB = GSRegMem(B_R, int(instructionList[3][1])).getRegMem()   #Como o segundo e terceiro regs contem os valore que serão operados, buscamos seus valores
        rC = GSRegMem(B_R, int(instructionList[4][1])).getRegMem()
        
        cpuInfo.alu = function(rB,rC)

        rA.setRegMem(cpuInfo.alu)   #Seta o valor no arquivo B_R referente a função executada

    if numTokens == 2: 
        function = dictInstructions[instructionList[1]]
        cpuInfo.alu = function(getAdr(instructionList[2]), getAdr(instructionList[3]))

    if numTokens == 1:
        function = dictInstructions[instructionList[1]]
        function(int(instructionList[2])-1,cpuInfo) #Como o PC vai ser somado em 1 ao voltar pro while e as instruções seguem o inicio 0, subtraimos por 2 o valor de bneg, branch ou bzero

    if numTokens == 0:
        function = dictInstructions[instructionList[1]]
        function()

instructions = IOFiles(EN).readTxt()
if instructions:
    IOFiles(M_R).writeTxt(instructions)
    cpuInfo = CPUInfo(pc=0,ir=instructions[0],alu=0)

    while cpuInfo.pc < 32 and cpuInfo.ir != "HALT\n":
        execInstruction(instructions[cpuInfo.pc],cpuInfo)
        cpuInfo.pc = int(cpuInfo.pc) + 1

    cpuInfoText = []
    cpuInfoText = ["PC: "+str(cpuInfo.pc)+"\n","IR: "+str(cpuInfo.ir)]
    IOFiles(U_C).writeTxt(cpuInfoText)
