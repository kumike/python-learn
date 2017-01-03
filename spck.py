#!/usr/bin/env python3

import argparse
from sys import exit

p=argparse.ArgumentParser()
p.add_argument('-s','--speed',metavar=' ',action='store',
               type=int,dest='speed',help=('Скорость подбора'),default='0')
p.add_argument('-f','--file',metavar=' ',action='store',
               type=str,dest='file',help=('/путь/к_словарю/dict.txt'),required=False)

args=p.parse_args()

if args.speed==0 or args.file==False:
    print(p.print_help()) #('Смотри spck -h для списка опций')
    exit()  ### Выход если одна из опций имеет значение по умолчанию

### Считаем строки в файле с паролями
result=sum(1 for l in open(args.file, 'r'))### переменная содержит количество строк в файле
print('Number of passwords in the dictionary: ',result)


d={'hour':3600,'day':24}

val=result//(args.speed*d['hour'])
if val>=0 and val<=d['day']:  
    print('Время перебора, часов:',val)
if val>=d['day']:val=val//d['day'];print('Время перебора, суток:',val) ### укороченый синтаксис if, простые конструкции можно писать коротко
