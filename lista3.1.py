#Napisz program, który „spakuje” kilka plików tekstowych do jednego pliku. Nazwy plików wejściowych i archiwum wynikowego powinny być podane jako argumenty
#konsoli. (Uwaga: w tym zadaniu nie używamy modułu zipfile i jemu podobnych).

#!/usr/bin/env python

import sys
import os
import shutil
from datetime import date

def main(texts: list, archive_name: str):
	"""a function that takes some text documents and archives them in a catalog by the given name.
	@param texts: text files that are about to be archived
	@param archive_name: name of the archive catalog
	"""

	for file in texts:
		if os.path.exists(file) == False:
			raise FileNotFoundError("a path is damaged or doesn't exist")
		elif file[-3:] != "txt":
			raise ValueError("file should be a text document")

	try:
		os.mkdir(archive_name)
	except FileExistsError:
		pass

	for file in texts: 
		name = file[:-4] + str(date.today()) + "-copy.txt"
		try:
			shutil.copyfile(file, name)
			shutil.move(name, archive_name)
		except shutil.Error:
			os.remove(name)
			print(("don't worry, you have already done a backup of {} today").format(file))
			pass
 
 
if __name__ == "__main__":
	
	if len(sys.argv) < 3:
		raise ValueError("not enough variables")
	else:
		main(sys.argv[1:-1], sys.argv[-1])
