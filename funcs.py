from os import system
from sys import stdout
from msvcrt import getch

write = stdout.write
system('')

cursor = 0
menuText = [
	'Open File',
	'New File',
	'Save File',
	'Exit'
]

def insert(string, insert, index):
	return string[:index] + insert + string[index:]

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
	write('\x1b[0m') # Reset style

	try:
		file = open(name, 'w')
	except:
		print('\x1b[31mFile does not exist.\x1b[0m')
		exit()

	print(''.join(file.readlines()))


system('cls')
write('  \x1b[47;30m Editing asd.txt - ESC to show menu \x1b[0m\n')
write('\n\x1b[38;2;105;105;105m1 │\x1b[0m')

keyMemory = ['']
x = 0
y = 0

while True:
	keypress = str(getch())[2:-1]

	if keypress == '\\x00':
		keypress = str(getch())[2:-1]

		if keypress == 'K': # Left arrow
			if x != 0:
				x -= 1
				write('\x1b[1D')
			elif y != 0:
				y -= 1
				x = len(keyMemory[y]) - 1
				write(f'\x1b[1F\x1b[{x + 1}C')

		elif keypress == 'M': # Right
			if x != len(keyMemory[y]) - 1:
				x += 1
				write('\x1b[1C')
			elif y != len(keyMemory) - 1:
				y += 1
				x = 0
				write('\x1b[1E')

		elif keypress == 'H': # Up
			prevLine = len(keyMemory[y - 1])

			if y != 0:
				if len(keyMemory[y]) > prevLine:
					write(f'\x1b[1F\x1b[{prevLine}C')
					x = prevLine - 1
				else:
					write('\x1b[1A')

				y -= 1

		elif keypress == 'P': # Down
			if y != len(keyMemory) - 1:
				nextLine = len(keyMemory[y + 1])

				if len(keyMemory[y]) > nextLine:
					write(f'\x1b[1E\x1b[{nextLine}C')
					x = nextLine - 1
				else:
					write('\x1b[1B')
				y += 1

		continue

	if keypress == '\\x1b': # Escape
		system('cls')
		exit()

	elif keypress == '\\r': # Enter
		write('\n\x1b[38;2;105;105;105m1 │\x1b[0m')
		keyMemory.append('')
		x = 0
		y += 1

	elif keypress == '\\x08': # Backspace
		if x != 0 and x != len(keyMemory[y]) - 1:
			after = keyMemory[y][x:]
			write('\b \b\x1b[0K' + after + f'\x1b[{len(after) - 1}D')
			x -= 1

	elif keypress == '\\\\': # AltGR + Q
		write('\\')

	elif keypress.startswith('\\'):
		continue

	else:
		after = keyMemory[y][x:]
		write(keypress + '\x1b[0K' + after + f'\x1b[{len(after) - 1}D')
		x += 1
		keyMemory[y] = insert(keyMemory[y], keypress, x)
		write('\x1b7\x1b[0;37H ' + 'DEBUG MODE   keyMEM:' + str(keyMemory) + '  x:' + str(x) + '  y:' + str(y) + '\x1b8')