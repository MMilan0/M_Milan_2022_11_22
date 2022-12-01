from os import system
from sys import stdout
from msvcrt import getch

write = stdout.write
system('') # https://stackoverflow.com/a/64222858/20316480

cursor = 0
menuText = [
	'Exit',
	'Open File',
	'New File',
	'Save File',
	'Continue Editing'
]

def line(n):
	space = ' '
	if n > 9:
		space = ''

	return f'\n\x1b[38;2;105;105;105m{n}{space}│\x1b[0m'

def insert(string, insert, index):
	return string[:index] + insert + string[index:]

def renderMenu():
	global cursor
	global menuText

	while True:
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
					system('cls')
					exit()
				return cursor


def openFile():
	system('cls')

	name = input('Enter filename: \x1b[32m')
	write('\x1b[0m') # Reset style

	try:
		file = open(name, 'r')
		lines = file.read().splitlines()
		file.close()

		return [lines, name]
	except:
		print('\x1b[31mFile does not exist.\x1b[0m')
		exit()

def newFile():
	system('cls')

	name = input('Enter filename: \x1b[32m')
	write('\x1b[0m')

	file = open(name, 'w')
	file.close()

	return name

def renderEditor(text, file_name):

	system('cls')
	write(f'  \x1b[47;30m Editing {file_name} - ESC to show menu \x1b[0m\n')

	keyMemory = text # Stores text line by line

	i = 1
	for _line in keyMemory:
		write(line(i) + _line)
		i += 1

	write('\x1b[3;4H')

	# Editor cursor coordinates
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
					x = len(keyMemory[y])
					write(f'\x1b[1F\x1b[{x + 3}C')

			elif keypress == 'M': # Right
				if x != len(keyMemory[y]):
					x += 1
					write('\x1b[1C')
				elif y != len(keyMemory) - 1:
					y += 1
					x = 0
					write('\x1b[1E\x1b[3C')

			elif keypress == 'H': # Up
				prevLine = len(keyMemory[y - 1])

				if y != 0:
					if x > prevLine:
						write(f'\x1b[1F\x1b[{prevLine + 3}C')
						x = prevLine
					else:
						write('\x1b[1A')

					y -= 1

			elif keypress == 'P': # Down
				if y != len(keyMemory) - 1:
					nextLine = len(keyMemory[y + 1])

					if x > nextLine:
						write(f'\x1b[1E\x1b[{nextLine + 3}C')
						x = nextLine
					else:
						write('\x1b[1B')
					y += 1

			continue

		if keypress == '\\x1b': # Escape
			system('cls')
			return keyMemory

		elif keypress == '\\r': # Enter
			afterCursor = keyMemory[y][x:]
			keyMemory[y] = keyMemory[y][:x]

			keyMemory.insert(y + 1, afterCursor)
			write(f'\x1b[0J{line(y + 2)}' + afterCursor + '\x1b[4G\x1b7')

			i = y + 3
			for _line in keyMemory[y + 2:]:
				write(line(i) + _line)
				i += 1

			x = 0
			y += 1
			write('\x1b8')

		elif keypress == '\\x08': # Backspace
			if x != 0:
				after = keyMemory[y][x:]

				if len(after) != 0:
					after += f'\x1b[{len(after)}D'

				write('\b \b\x1b[0K' + after)

				x -= 1
				keyMemory[y] = keyMemory[y][:x] + keyMemory[y][x + 1:]

			elif x == 0 and y != 0:
				currentLine = keyMemory[y]
				del keyMemory[y]
				write(f'\x1b[1F\x1b[{len(keyMemory[y - 1]) + 3}C\x1b7{currentLine}\x1b[0J')

				keyMemory[y - 1] += currentLine

				i = y + 1
				for _line in keyMemory[y:]:
					write(line(i) + _line)
					i += 1

				x = len(keyMemory[y - 1]) - len(currentLine)
				y -= 1
				write('\x1b8')

		elif keypress == '\\\\': # AltGR + Q
			write('\\')

		elif keypress.startswith('\\'):
			continue

		else:
			after = keyMemory[y][x:]
			write(keypress + '\x1b7\x1b[0K' + after + '\x1b8')
			keyMemory[y] = insert(keyMemory[y], keypress, x)
			x += 1
