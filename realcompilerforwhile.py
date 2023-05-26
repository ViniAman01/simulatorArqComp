#!/bin/python3

from typing import List

B_R = "banco_registradores.txt"
EN = "entrada.txt"
U_C = "unidade_controle.txt"
M_R = "memoria_ram.txt"

def add(a,b): return a+b
def sub(a,b): return a-b
def anD(a,b): return a & b
def oR(a,b): return a | b

dictInstructions = {
        #"LOAD": load,
        #"STORE": store,
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

tupleRegisters = (
        "R0: 0\n",
        "R1: 0\n",
        "R2: 0\n",
        "R3: 0\n",
        )
class IOFiles:
    def __init__(self, name: str):
        self.name = name

    def readTxt(self): #Retorna conteúdo do arquivo em str
    #FAZER TRATAMENTO DE ERROS
        with open(self.name) as f:
            return f.readlines()

    def writeTxt(self, value: List):
        with open(self.name,"w+") as f:
            f.writelines(value)


class GSRegMem(IOFiles): #Class que opera sobre os registradores e ram
    def __init__(self, name: str, adr: int):
        self.adr = adr

        super().__init__(name)
         
    def getRegMem(self):
        auxTxt = self.readTxt()
        if auxTxt:
            return int(auxTxt[self.adr][4:])
        else:
            print("Banco vazio!")
            return False

    def setRegMem(self,value):
        auxTxt = self.readTxt()
        if not auxTxt:
            auxTxt = list(tupleRegisters)

        auxTxt[self.adr] = auxTxt[self.adr][:4] + str(value)  + auxTxt[self.adr][-1:]
        self.writeTxt(auxTxt)
        
def getInstructions(inputTxt: List[str]): #Splita as instruções em uma lista
    instructionsInput = inputTxt.splitlines()
    return instructionsInput

def execInstructionAL(instructionLine: str): #Executa determinada instrução da ALU contendo dois valores
    instructionList = instructionLine.split(" ")
    return dictInstructions[instructionList[0]](int(instructionList[1]),int(instructionList[2]))

reg0 = GSRegMem(B_R,1)    
reg0.setRegMem(99999)
