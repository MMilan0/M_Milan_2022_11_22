from os import system

cursor = 0
menuText = [
	'Open File',
	'New File',
	'Save File',
	'Exit'
]

def renderMenu():
	global cursor
	global menuText

	system('cls')

	i = 0
	for item in menuText:
		if i == cursor:
			print('\x1b[47;30m' + item + '\x1b[0m')
		else:
			print(item)
		i += 1

	print('\nUse W/S to navigate, E to confirm')

	key = system('choice /C wse /N >NUL')

	if key == 2:
		cursor += 1
	elif key == 1:
		cursor -= 1

	# Wrap around
	if cursor > len(menuText) - 1:
		cursor = 0
	elif cursor < 0:
		cursor = len(menuText) - 1

	if key == 3:
		if cursor == 0:
			openFile()
		elif cursor == 1:
			newFile()
		elif cursor == 2:
			saveFile()
		else:
			exit()


def openFile():
	system('cls')

	name = input('Enter filename: \x1b[32m')
	print('\x1b[0m', end='') # Reset style

	file = open(name, 'r')


while True:
	renderMenu()