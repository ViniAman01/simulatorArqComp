#!/bin/python3

from typing import List

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

class Registers: #Class que opera sobre os registradores
    def __init__(self, reg):
        self.reg = reg
         
    def getReg(self):
        auxTxt = readTxt("banco_registradores.txt").splitlines()
        if auxTxt:
            return int(auxTxt[self.reg][4:])
        else:
            print("Banco vazio!")
            return False

    def setReg(self,value):
        auxTxt = readTxt("banco_registradores.txt").splitlines()
        if not auxTxt:
            auxTxt = list(tupleRegisters)
        auxTxt[self.reg] = auxTxt[self.reg][:4] + str(value)  + auxTxt[self.reg][-1:]
        writeTxt("banco_registradores.txt", auxTxt)
        
def readTxt(name: str): #Retorna conteúdo do arquivo em str
#FAZER TRATAMENTO DE ERROS
    with open(name) as f:
        return f.read()

def writeTxt(name: str, value: List):
    with open(name,"w+") as f:
        f.writelines(value)

def getInstructions(inputTxt: List[str]): #Splita as instruções em uma lista
    instructionsInput = inputTxt.splitlines()
    return instructionsInput

def execInstructionAL(instructionLine: str): #Executa determinada instrução da ALU contendo dois valores
    instructionList = instructionLine.split(" ")
    return dictInstructions[instructionList[0]](int(instructionList[1]),int(instructionList[2]))

reg0 = Registers(0)    

reg0.setReg(5)
