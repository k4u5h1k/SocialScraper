import pyfiglet
import colorama
import time
import sys
from time import sleep
from termcolor import cprint
from colorama import init 
from termcolor import colored 
from os import system

class colors: 
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg: 
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg: 
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'

def intro():
    colorama.init()
    system("clear")
    system("say welcome to social scraper")
    result = pyfiglet.figlet_format(23*' '+'SOCIAL\n'+17*' '+'SCRAPER') 
    cprint(result, 'yellow')
    time.sleep(1)
    r = pyfiglet.figlet_format(17*' '+'USING PYTHON', font = "bubble") 
    cprint(r, 'white')
    time.sleep(1)
    n = pyfiglet.figlet_format(29*' '+'Written By\n'+10*' '+'Kaushik Sivashankar(19BAI1052)\n'+22*' '+'Priyanshu(19BAI1077)', font = "digital") 
    cprint(n, 'green')
    time.sleep(1)
    print(colors.bg.lightgrey,colors.fg.red, "---DISCLAIMER : Please only use this project for educational purposes---")
    # time.sleep(1)
    # print(colors.bg.black,colors.fg.cyan, "First Lets understand what scraping is.. :)")
    # print()
    # print(colors.bg.lightgrey,colors.fg.purple, "Web scraping is a term used to describe the use of a program or algorithm to extract and process large amounts of data from the web. For this project we have scraped some of the major social platforms including Facebook and Twitter.")
    print(colors.reset)
    # c = pyfiglet.figlet_format('Now Lets scrap', font = "slant")
    # cprint(c,'blue')
    time.sleep(1)


def inred(r):
    print(colors.bg.cyan,colors.fg.red,r)
    print(colors.reset)
def ingreen(r):
    print(colors.bg.lightgrey,colors.fg.green,r)
    print(colors.reset)
def inlightred(r):
    print(colors.bg.black,colors.fg.lightred,r)
    print(colors.reset)
def inyellow(r):
    print(colors.bg.blue,colors.fg.yellow,r)
    print(colors.reset)
def inpink(r):
    print(colors.bg.cyan,colors.fg.pink,r)
    print(colors.reset)
def inorange(r):
    print(colors.bg.blue,colors.fg.orange,r)
    print(colors.reset)
def inlightcyan(r):
    print(colors.bg.black,colors.fg.lightcyan,r)
    print(colors.reset)
def inpurple(r):
    print(colors.bg.lightgrey,colors.fg.purple,r)
    print(colors.reset)
def incyan(r):
    print(colors.bg.red,colors.fg.cyan,r)
    print(colors.reset)
def inblue(r):
    print(colors.bg.lightgrey,colors.fg.blue,r)
    print(colors.reset)
def inblack(r):
    print(colors.bg.lightgrey,colors.fg.black,r)
    print(colors.reset)
def load():
    n = 20
    for i in range(n):
        time.sleep(1)
        sys.stdout.write('\r'+'  loading...  process '+str(i)+'/'+str(n)+' '+ '{:.2f}'.format(i/n*100)+'%')
        sys.stdout.flush()
    sys.stdout.write('\r'+'  loading... finished               \n')
    print()
def bar():
    for i in range(101):
        sys.stdout.write('\r')
        sys.stdout.write("  [%-10s] %d%%" % ('='*i, 1*i))
        sys.stdout.flush()
        sleep(0.1)
    print()

if __name__=="__main__":
    intro()
    load()
    bar()
