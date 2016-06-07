#!/usr/bin/env python3

dia=int(input('\033[96mЧисло комбинаций: \033[0m'))
speed=int(input('\033[96mСкорость перебора:\033[0m '))
hour=3600
minute=60
day=24
val=dia//(speed*hour)
if val<=0:
    val=dia//(speed*minute)
    print('\033[1;32mМинут',val,'\033[1;m')
if val>0 and val<=24: 
    print('\033[1;32mЧасов',val,'\033[1;m')
if val>=24:val=val//day;print('  \033[32m',val,'Cуток\033[1;m') # укороченый синтаксис if, простые конструкции можно писать коротко
