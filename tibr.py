###
#!/usr/bin/env python3
import os
import threading
import argparse

### парсер аргументов командной строки
desc='Скрипт для подсчёта времени перебора определённого количества паролей или словаря.'
epilog=''

parser=argparse.ArgumentParser(description=desc,epilog=epilog)#,formatter_class=ihf)

parser.add_argument('-f',dest='filename',help='/patch/to/your/dict, опцию можно задать вместе с -A или -P')
parser.add_argument('-n',dest='dia',type=int,help='Количество вариантов паролей')
parser.add_argument('-s',dest='speed',type=int,help='insert your speed, допустимыми являются только целые числа')
parser.add_argument('-A',dest='speedA',action='store_true',help='Получить скорость вычисления хендшейка в Aircrack-ng')
parser.add_argument('-P',dest='speedP',action='store_true',help='Получить скорость вычисления хеншейка в pyrit')
args=parser.parse_args()

### начало определения функций ###
### функции для интерактивного ввода
def inputNumPass():
	try:
		while True:
			try:
				dia=int(input('Количество паролей: '))
				break
			except ValueError:
				print('\nДопускаются только целые числа!\n')
	except KeyboardInterrupt: # если юзер при вводе значений жмет ctrl-c то выходим и печатаем сообщение
		exit('\nВыход!') # если не ловить это то будет бросатся Traceback и стандартное сообщение в консоль
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
	try:
		# если открывать файл через менеджер контекста то не нужно тогда его закрывать, with позаботится о закрытии
		with open(args.filename,'r') as dicfile: # в open(,'r') 'r' не важен, по умолчанию открывается для чтения, на всяк случай указал
			dia=sum(1 for line in dicfile) # sum() возвращает int, думаю преобразовыватьв int лишнее.
		print('Количество паролей в словаре:',dia)
		return dia
	except FileNotFoundError:
		exit('Файл не найден!')

### функция для старта паралельно бенчмарка и анимации и возврата значения скорости полученого бенчмарком
def loadNbench():
	# проверяем установлен ли aircrack-ng
	if args.speedA: # проверка args.speedA на True, короткая запись if args.speedA is True, в PEP написано что так не верно
		whis=os.popen('whereis aircrack-ng').read() 
		check='/bin/' in whis # True если есть вхождение
		if check is False: # если нет то пишем соопчение и выходим
			exit('Пожалуйста, установите aircrack-ng')
	# проверяем установлен ли pyrit
	if args.speedP:
		whis=os.popen('whereis pyrit').read() 
		check='/bin/' in whis # если нет вхождения то False если есть True
		if check is False: # если нет то пишем соопчение и выходим
			exit('Пожалуйста, установите pyrit')
	### функция запускает бенчмарки и возвращает строку с результатом
	# если измениться эта переменная, то остановится цикл который рисует анимацию, переменная меняется когда завершит работу бенчмарк
	signal_stop=None
	def startBenchstr_num():
		global ls # делаем переменную доступную из всего остального скрипта
		if args.speedA: # если опция speedA True запускаем aircrack -S
			ls=os.popen('aircrack-ng -S').readlines()
			ls=ls.pop() # вырезаем и возвращаем в переменную последнее значения из списка полученого от aircrack-ng
		if args.speedP: # если опция speedP True запускаем pyrit benchmark
			ls=os.popen('pyrit benchmark').readlines()
			for line in ls: # вырезаем нужную строчку из списка строк приехавшим из pyrit
				if 'total.' in line: # если есть вхождение в строке присваиваим строку переменной и завершаим цикл
					ls=line
					break # в принципе не обязательно, без брик сделает сколько то лишних пустых итераций
		nonlocal signal_stop # если задана переменная внутри функции нужно nonlocal
		signal_stop=1
	### функция стартует анимацию которая проигрывается во время бенчмарка	
	def startLoadAnim():
		lo=(' Подождите',' ПОдождите',' ПоДождите',' ПодОждите',
		    ' ПодоЖдите',' ПодожДите',' ПодождИте',' ПодождиТе',' ПодождитЕ')
		an=('|','/','-','\\')
		dot=('...')
		ilo,ian=0,0
		from time import sleep
		while signal_stop is None:
			print(lo[ilo],dot,an[ian],sep='',end='\r')
			sleep(0.1) # лучше размещать после слиип, снаала выводит а потом спит, не спит перед первым ваводом.
			ilo+=1
			ian+=1
			if ilo is len(lo):ilo=0 # инкрементировать переменную нада после принт чтобы начинался перебор кортежа с 0 ()кортеж []список
			if ian is len(an):ian=0

	th_startBenchstr_num=threading.Thread(target=startBenchstr_num)
	th_startLoadAnim=threading.Thread(target=startLoadAnim)
	# стартуем две функции паралельно и ждём их завершения .join()
	th_startBenchstr_num.start();th_startLoadAnim.start()
	th_startBenchstr_num.join();th_startLoadAnim.join()

	# если не задано аргументом путь к файлу с паролями спросить интерактивно количество паролей
	if args.filename is None:
		dia=inputNumPass()
	else: # иначе взять файл и подсчитать в нём количество паролей(строк)
		dia=calcPassInDic()

	# вытягиваем число из строки полученой из бенчмарка pyrit или aircrack-ng
	dch={0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'.'}
	dot=0
	b=[]
	for char in ls:
		if char:
			for key in dch:
				if char is dch[key]:
					if dch[key] is '.':dot+=1
					b.append(dch[key])
		if dot>=1:break
	x=0
	speed='' # инициализируем пустую переменную типа str потом в цикле добавим к ней значения
	# считаем количество результатов в списке и конкантенируем их в переменную, числа в списке имеют тип str
	for i in str_num:
		speed+=str_num[x]
		x+=1
	speed=int(round(float(speed))) # приводим к числу и округляем полученый результат к целому числу, pyrit возвращает float
	return speed,dia
	
### функция запуска интерактивного режима
def interactive():
	dia=inputNumPass()
	speed=inputSpeed()
	return speed,dia

### функция выводит строку хелпа и рисует вокруг строки рамку вне зависимости от длинны строки
def helpwin():
#	from os import path
	from sys import argv
	prog=os.path.basename(argv[0]) # в переменной хранится имя скрипта, как его не назови.
	helpstring='Смотри '+prog+' -h для дополнительных аргументов'
	lenth=len(helpstring)+2
	border='-'*lenth
	win=' \033[35m+'+border+'+\n |\033[0m\033[93m '+helpstring+' \033[0m\033[35m|\n +'+border+'+\033[0m\n'
	return print(win)
### конец определения функций ###

# TODO доделать нада чтобы с бенчамрком требовалось ввести или путь к файлу паролей или количество паролей вручную
# выбор нужного режима работы, интерактивный или с определением скорости
if args.speedA and args.speedP: # если обе переменные True
#	print('error')
	exit('[ERROR] Only -A or -P')

elif args.speedA or args.speedP: # если одна из переменных True
	speed,dia=loadNbench()
# если задана только опция -f то посчитать и вывисти количество строк в словаре
elif args.filename is not None and args.speedA is False and args.speedA is False and args.dia is None and args.speed is None:
	calcPassInDic()
	exit() # выходим чтобы дальше с нулём не считало
else:
	helpwin()
	speed,dia=interactive()

### начало расчёта
# делим количество паролей в словаре на скорость перебора, паролей в секунду, получаем значение в секундах 
val=dia//speed # // - оператор деления с усечением дробной части, но если делить флоат то так флоат и останется! 

if val!=0: # если результат нулевой не выводим хедер таблики подсчёта
	print('\n---- Результат подсчёта ----\n')
	print('С скоростью',speed,'k/s, количество вариантов равное',dia,'будет перебираться\n')
# задаем значения переменных в ноль? чтобы потом при расчётах не ругалось на неопределённую переменную
year,mounth,week,day,hour,minute=0,0,0,0,0,0

mass=(('Лет','Год','Года','Года','Года','Лет','Лет','Лет','Лет'),
      ('Месяцев','Месяц','Месяца','Месяца','Месяца','Месяцев','Месяцев','Месяцев','Месяцев','Месяцев'),
      ('Дней','День','Дня','Дня','Дня','Дней','Дней','Дней','Дней','Дней'),
      ('Часов!!','Час','Часа','Часа3','Часа4','Часов0','Часов1','Часов2','Часов3','Часов4'),
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
if year>0:
	if val is 0:print(' ',year,skl(year,0))
	else:print(' ',year,skl(year,0),end='')
if year>150:val=0 # если получается больше 150 лет, обрезаем вывод месяцев дней и т.д, накапливается ошибка 29 дней февраля.
### месяцы
if val>=2635200:mounth=val//(2635200);val=val-mounth*2635200 # 24часаВсут*3600секВчас*30.5днейВмес с учётом 30-31д=2635200.0 дробь нах
if mounth>0:
	if val is 0:print(' ',mounth,skl(mounth,1))
	else:print(' ',mounth,skl(mounth,1),end='')	
### недели
if val>=604800:week=val//(604800);val=val-week*604800 # 24часа*7дней*3600секВчасе или 24часа*3600секВчасе*7днейВнеделе=604800секВнед
#print('  ',week,'Недели') if week>1 else print('  ',week,'Неделя') # трёхместное if/else
if week>1:
	if val is 0:print(' ',week,'Недели')
	else:print(' ',week,'Недели',end='')
elif week is 1:
	if val is 0:print(' ',week,'Неделю')
	else:print(' ',week,'Неделю',end='')
### сутки
if val>=86400:day=val//(86400);val=val-day*86400 # 24часаВсутках*3600секВчасе=86400секВсутках
if day>0: 
	# переносить строку если дальше нету результатов, если есть не переносить и писать след результ в одну строку
	if val is 0:print(' ',day,skl(day,2))
	else:print(' ',day,skl(day,2),end='')
### часы
if val>=3600:hour=val//3600;val=val-hour*3600 # 60секундВминуте*60минутВчасе=3600секВчасе
if hour>0:
	if val is 0:print(' ',hour,skl(hour,3))
	else:print(' ',hour,skl(hour,3),end='')
### минуты
if val>59:minute=val//60;val=val-minute*60
if minute>0:
	if val is 0:print(' ',minute,skl(minute,4))
	else:rmin=minute,skl(minute,4);print(rmin[0],rmin[1],end='') #print('    ',minute,skl(minute,4),end=' ')	
### остаток секунд
if val!=0:print (' ',val, skl(val,5))

