from funcs import *

fileName = fileText = ''


while True:
	choice = renderMenu()

	if choice == 1:
		opened = openFile()

		fileText = opened[0]
		fileName = opened[1]

	elif choice == 2:
		fileName = newFile()
		fileText = ['']

	elif choice == 3:

		if fileName == '':
			continue

		file = open(fileName, 'w')
		file.write('\n'.join(fileText))

		system('cls')
		input('File saved [Enter]')
		file.close()

		continue

	elif choice == 4 and fileName == '':
		continue

	fileText = renderEditor(fileText, fileName)