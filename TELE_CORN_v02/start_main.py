import os
import subprocess
import sys
#from colorama import init, Fore, Back, Style
import time



#init()
print("Нажми Enter чтобы запустить...")
input()

while (True):
    process = subprocess.Popen([sys.executable, "main2.py"])
    process.wait()