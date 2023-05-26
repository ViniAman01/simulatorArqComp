#!/bin/python3

text = "oi"
text2 = " all"

with open("entrada.txt") as f:
    txt = f.readlines()

print(txt)

txt[1] = txt[1][:4] + str(2345)  + txt[1][-1:] 

print(txt)

with open("entrada.txt","w") as f:
    f.writelines(txt)
