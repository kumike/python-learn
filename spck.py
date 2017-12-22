#skl=(['Секунд','Секунда','Секунды'],['Минут','Минута','Минуты'],['Час','Часа','Часов'],['День','Дня','Дней'])
#skl=(['Неделя','Недели'],['День','Дня','Дней'],['Час','Часа','Часов'],['Минут','Минута','Минуты'],['Секунд','Секунда','Секунды'])
#print(skl[0][1],skl[1][2],skl[2][1],skl[3][2],skl[4][0],sep='\n')
import os
import sys
import re
import threading
import time
from optparse import OptionParser,IndentedHelpFormatter
#import optparse
prog=os.path.basename(sys.argv[0]) # в переменной хранится имя скрипта, как его не назови.

### парсер аргументов командной строки
desc='считалка времени ламалки чёртовой както форматит этот модуль вроде неплохо так форматит описание считалки'
epilog='от така хуйня малята :)'
ihf=IndentedHelpFormatter(max_help_position=32) # задаем ширину вывода строчек справки в столбцах(длинна строки 32 знака\столбца)
#parser=OptionParser(usage=optparse.SUPPRESS_USAGE,description=desc,epilog=epilog,formatter=ihf)
parser=OptionParser(description=desc,epilog=epilog,formatter=ihf)

parser.add_option('-f',dest='filename',type='string',help='/patch/to/your/dict, опцию можно задать вместе с -A или -P')
parser.add_option('-n',dest='dia',type='int',help='Количество вариантов паролей')
parser.add_option('-s',dest='speed',type='int',help='insert your speed, допустимыми являются только целые числа')
parser.add_option('-A',dest='speedA',action='store_true',help='Получить скорость вычисления хендшейка в Aircrack-ng')
parser.add_option('-P',dest='speedP',action='store_true',help='Вычислить скорость pyrit')
(opt,args)=parser.parse_args()

### начало определения функций ###
### функции для интерактивного ввода
def inputNumPass():
	try:
		while True:
			try:
				dia=int(input('Число комбинаций: '))
				break
			except ValueError:
				print('\nДопускаются только целые числа!\n')
	except KeyboardInterrupt: # если юзер при вводе значений жмет ctrl-c то выходим и печатаем сообщение
		exit('\nВыход!') # если не ловить это то будет бросатся Traceback и стандартное сообщение в консоль
	#	exit('\r') # выйти молча
	return dia
def inputSpeed():
	try:
		while True:
			try:
				speed=int(input('Скорость перебора: '))
				if speed==0:
					print('\nВведите не ноль!\n')
					continue
				break
			except ValueError:
				print('\nДопускаются только целые числа!\n')
	except KeyboardInterrupt: # если юзер при вводе значений жмет ctrl-c то выходим и печатаем сообщение
		exit('\nВыход!')
#		exit('\r') # выйти молча
	return speed

### функция подсчёта паролей в словаре	
def calcPassInDic():
	dicfile=open(opt.filename,'r')
	dia=sum(1 for line in dicfile) # переменная содержит количество строк в файле
	dicfile.close()
	# или так, если файл не оч большой 
#	dia=int(len(open(opt.filename,'r').readlines())) # как в таком случае закрыть файл? что нада обязательно как пишут ..
#	print('Number of passwords in the dictionary:',dia)
	print('Количество паролей в словаре:',dia),dia
	return dia

#ls=os.popen('cat so.txt','r') # открываем файл с строчкой, пока для тестов
fle='cat so.txt' # можно передать в функцию ниже значения переменной, например значение аргумента при запуске скрипта
### функция для старта паралельно бенчмарка и анимации и возврата значения скорости полученого бенчмарком
def loadNbench():
	# проверяем установлен ли aircrack-ng
	if opt.speedA: # проверка opt.speedA на True, короткая запись if opt.speedA is True, в PEP написано что так не верно
		whis=os.popen('whereis aircrack-ng').read() 
		check=None
		check=re.search('(/bin/|/sbin/)',whis)
		#check='/bin/' in whis # True если есть вхождение, лучше пока проверять регулярками дарма что лишний модуль..
		if check is None: # если нет то пишем соопчение и выходим
			exit('Пожалуйста, установите aircrack-ng')
	# проверяем установлен ли pyrit
	if opt.speedP is True:
		whis=os.popen('whereis pyrit').read() 
		check=None
		check=re.search('(/bin/|/sbin/)',whis)
		if check is None: # если нет то пишем соопчение и выходим
			exit('Пожалуйста, установите pyrit')
	### функция запускает бенчмарки и возвращает строку с результатом
	# если измениться эта переменная, то остановится цикл который рисует анимацию, переменная меняется когда завершит работу бенчмарк
	signal_stop=0
	def startBenchstr_num():
		global ls # делаем переменную доступную из всего остального скрипта
		if opt.speedA: # если опция speedA True запускаем aircrack -S
			ls=os.popen(fle).readlines()
			ls=ls.pop() # вырезаем и возвращаем в переменную последнее значения из списка полученого от aircrack-ng
		if opt.speedP: # если опция speedP True запускаем pyrit benchmark
			ls=os.popen('cat pso.txt').readlines()
			for line in ls: # вырезаем нужную строчку регулярным выражением из списка строк приехавшим из pyrit
				m=re.search('.+total.+',line)
				if m is not None: # re.search возвращает None если не находит вхождения в строке. if m != None
					ls=m.group()
					break
		nonlocal signal_stop # если задана переменная внутри функции нужно nonlocal
		signal_stop+=1
	### функция стартует анимацию которая проигрывается во время бенчмарка	
	def startLoadAnim():
		lo=(' Загрузка...',' ЗАгрузка...',' ЗaГрузка...',' ЗaгРузка...',
		    ' ЗaгрУзка...',' ЗaгруЗка...',' ЗaгрузКа...',' ЗaгрузкА...')
		an=('|','/','-','\\')
		ilo,ian=0,0
		while signal_stop is 0:
			print(lo[ilo],an[ian],sep='',end='\r')
			time.sleep(0.1) # лучше размещать после слиип, снаала выводит а потом спит, не спит перед первым ваводом.
			if ilo==7:ilo=0 # инкрементировать переменную нада полсле принт, чтобы начинался перебор кортежа с 0 ()кортеж []список
			if ian==3:ian=0
			ilo+=1
			ian+=1 # тут работает такое присваивание переменной =+, просто инкремент + нет
	
	th_startBenchstr_num=threading.Thread(target=startBenchstr_num)
	th_startLoadAnim=threading.Thread(target=startLoadAnim)
	# стартуем две функции паралельно и ждём их завершения .join()
	th_startBenchstr_num.start();th_startLoadAnim.start()
	th_startBenchstr_num.join();th_startLoadAnim.join()

	# если не задано аргументом путь к файлу с паролями спросить интерактивно количество паролей
	if opt.filename is None:
		dia=inputNumPass()
	else: # иначе взять файл и подсчитать в нём количество паролей(строк)
		dia=calcPassInDic()

	# вытягиваем число из строки полученой из бенчмарка
	str_num=[]
	dot=0
	for i in ls:
		if i is chr(0x30):
			str_num.append(i)
		if i is chr(0x31):
			str_num.append(i)
		if i is chr(0x32):
			str_num.append(i)
		if i is chr(0x33):
			str_num.append(i)
		if i is chr(0x34):
			str_num.append(i)
		if i is chr(0x35):
			str_num.append(i)
		if i is chr(0x36):
			str_num.append(i)
		if i is chr(0x37):
			str_num.append(i)
		if i is chr(0x38):
			str_num.append(i)
		if i is chr(0x39):
			str_num.append(i)
		if i is chr(0x2e):
			dot+=1
			str_num.append(i)
			if dot>=2:
				str_num.pop()
#	print(str_num)
#	print('количество точек ',dot)
	x=0
	speed='' # инициализируем пустую переменную типа str потом в цикле добавим к ней значения
	# считаем количество результатов в списке и конкантенируем их в переменную, числа в списке имеют тип str
	for i in str_num:
		speed+=str_num[x]
		x+=1
#	print(type(speed),speed)
	speed=int(round(float(speed))) # приводим к числу и округляем полученый результат к целому числу, pyrit возвращает float
#	print(type(speed),speed)
	return speed,dia
	
### функция запуска интерактивного режима
def interactive():
	dia=inputNumPass()
	speed=inputSpeed()
	return speed,dia

### функция выводит строку хелпа и рисует вокруг строки рамку вне зависимости от длинны строки
def helpwin():
	helpstring='Смотри '+prog+' -h для дополнительных аргументов'
	lenth=len(helpstring)+2
	border='-'*lenth
	win=' \033[35m+'+border+'+\n |\033[0m\033[93m '+helpstring+' \033[0m\033[35m|\n +'+border+'+\033[0m\n'
	return print(win)
### конец определения функций ###

# TODO доделать нада чтобы с бенчамрком требовалось ввести или путь к файлу паролей или количество паролей вручную
# выбор нужного режима работы, интерактивный или с определением скорости
if opt.speedA and opt.speedP: # если обе переменные True
#	print('error')
	exit('error!!')

elif opt.speedA or opt.speedP: # если одна из переменных True
	speed,dia=loadNbench()
# если задана только опция -f то посчитать и вывисти количество строк в словаре
elif opt.filename is not None and opt.speedA is None and opt.speedA is None and opt.dia is None and opt.speed is None:
	calcPassInDic()
	exit() # выходим чтобы дальше с нулём не считало
else:
	helpwin()
#	print('+',aster,'+\n| ',helpstring,' |\n+',aster,'+',sep='')
	speed,dia=interactive()



### начало расчёта
# делим количество паролей в словаре на скорость перебора, паролей в секунду, получаем значение в секундах 
val=dia//speed # // - оператор деления с усечением дробной части, но если делить флоат то так флоат и останется! 

if val!=0: # если результат нулевой не выводим хедер таблики подсчёта
	print('\n---- Результат подсчёта ----\n')
	print('С скоростью',speed,'k/s, количество вариантов равное',dia,'будет перебираться\n')
# задаем значения переменных в ноль? чтобы потом при расчётах не ругалось на неопределённую переменную
year,mounth,week,day,hour,minute=(0,0,0,0,0,0)

mass=(('Лет','Год','Года','Года','Года','Лет','Лет','Лет','Лет'),
      ('Месяцев','Месяц','Месяца','Месяца','Месяца','Месяцев','Месяцев','Месяцев','Месяцев','Месяцев'),
      ('Дней','День','Дня','Дня','Дня','Дней','Дней','Дней','Дней','Дней'),
      ('Часов!!!!!','Час','Часа','Часа3','Часа4','Часов0','Часов1','Часов2','Часов3','Часов4'),
	  ('Минут','Минута','Минуты','Минуты','Минуты','Минут','Минут','Минут','Минут','Минут'),
	  ('Секунд','Секунда','Секунды','Секунды','Секунды','Секунд','Секунд','Секунд','Секунд','Секунд'))
### функция для выбора склонений для названий чисел в зависимости от числа
def skl(va,x): # x при вызове функции задается номер подмасива
	n=va%100 # получаем остаток от деления, например 123 дня, остаток 23,сделано для годов которые больше 100 :)
	if n>9 and n<20: # -надцать склоняется по другому :)
		return mass[x][0] # если входит в диапазон вернуть это, если нет считать далее по другой формуле
	n=va%10 # получаем остаток от деления, например 9 остаток 9, 12 остаток 2 или 12/10
	return mass[x][n]

### годы
if val>=31557600:year=val//(31557600);val=val-year*31557600 # 86400секВсут*365.25днейВгоду с учётом высокосного каждый 4 год.
if year>0:print('    ',year,skl(year,0),end=' ')
if year>150:val=0 # если получается больше 150 лет, обрезаем вывод месяцев дней и т.д, накапливается ошибка 29 дней февраля.
### месяцы
if val>=2635200:mounth=val//(2635200);val=val-mounth*2635200 # 24часаВсут*3600секВчас*30.5днейВмес с учётом 30-31д=2635200.0 дробь нах
if mounth>0:print('    ',mounth,skl(mounth,1),end=' ')
### недели
if val>=604800:week=val//(604800);val=val-week*604800 # 24часа*7дней*3600секВчасе или 24часа*3600секВчасе*7днейВнеделе=604800секВнед
#print('  ',week,'Недели') if week>1 else print('  ',week,'Неделя') # трёхместное if/else
if week>1:
	print('    ',week,'Недели',end=' ')
elif week==1:
	print('    ',week,'Неделю',end=' ')
### сутки
if val>=86400:day=val//(86400);val=val-day*86400 # 24часаВсутках*3600секВчасе=86400секВсутках
if day>0:
	if val==0: # переносить строку если дальше нету результатов, если есть не переносить и писать след результ в одну строку
		print('    ',day,skl(day,2))
	else:print('    ',day,skl(day,2),end=' ')
### часы
if val>=3600:hour=val//3600;val=val-hour*3600 # 60секундВминуте*60минутВчасе=3600секВчасе
if hour>0:print('    ',hour,skl(hour,3),end=' ')
### минуты
if val>59:minute=val//60;val=val-minute*60
if minute>0:rmin=minute,skl(minute,4);print(rmin[0],rmin[1]) #print('    ',minute,skl(minute,4),end=' ')
### остаток секунд
if val!=0:print ('и   ',val, skl(val,5))

