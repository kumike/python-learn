#!/usr/bin/env python3

# В стандартной поставке путона3 нету модуля termcolor отвечающего за цветной вывод,
# TODO когда буду делать пакет, учесть как зависимость етот модуль
# модуль устанавливается командой pip3 install termcolor, пришлось доустанавливать сам пип, apt install python3-pip


dia=int(input('Число комбинаций: '))
speed=int(input('\033[96mСкорость перебора:\033[0m '))
hour=3600
minute=60
val=dia//(speed*hour)
if val<=0:
    val=dia//(speed*minute)
    print('Минут',val)
if val>0 and val<=24: 
    print('Часов',val)
if val>=24:val=val//24;print('  ',val,'Cуток') # укороченый синтаксис if, простые конструкции можно писать коротко
