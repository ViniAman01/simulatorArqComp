#!/bin/python3
import typing

class TextManipulation:
    def __init__(self, name: str, mode: str, text=None):
        self.name = name
        self.mode = mode
        self.text = text

    def fopen(self):
        try:
            with open(self.name, self.mode) as f:
                if(self.mode == "r" or self.mode == "r+"):
                    return f.read()
                if(self.mode == "w" or self.mode == "w+"):
                    f.write(self.text)
        except IOError: 
            print("I/O Error")

txt = "LOAD R1 13"

class InstructionsDM:
    def __init__(self, reg_mem: str, mem_reg: int):
        self.reg_mem = reg_mem
        self.mem_reg = mem_reg

class InstructionsAL:
    def __init__(self, R1: int, opr2: int):
        self.name = name
        self.opr1 = opr1
        self.opr2 = opr2

    def add(self):
        return self.opr1+self.opr2 
