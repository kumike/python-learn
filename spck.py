#!/usr/bin/env python3

import argparse
from sys import exit
p=argparse.ArgumentParser()
p.add_argument('-s','--speed',metavar=' ',action='store',type=int,dest='speed',help=('Скорость подбора'),default='0')
p.add_argument('-n','--number_of_pass',metavar=' ',action='store',type=int,dest='number',help=('Количество паролей в словаре'),default='0')
args=p.parse_args()
if args.speed==0 or args.number==0:
    print (p.print_help())
    exit() 
d={'hour':3600,'minute':60,'day':24}
val=args.number//(args.speed*d['hour'])
if val<=0:
    val=args.number//(args.speed*d['minute'])
    print('\033[1;32mМинут',val,'\033[1;m')
if val>=0 and val<=d['day']:   
    print('\033[1;32mЧасов',val,'\033[1;m')
if val>=d['day']:val=val//d['day'];print('  \033[1;32m',val,'Cуток\033[1;m') 
