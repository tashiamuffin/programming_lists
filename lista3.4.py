#napisz program, który zamieni znaki końca linii w plikach tekstowych z uniksowych na windowsowe i odwrotnie.


# "\r\n" // windows
# "\n" // linux

import sys
import os

def main(system: str, file: str):
    """a function that changes ends of lines in text document from unix to windows and vice versa. It uses two functions - unix() and windows() to do that.
    @param system: a system in which files should be converted - it has to be either "unix" or "windows"
    @param file: a name (path) of the text document that is about to be converted
    """

    if not os.path.exists(file) or not file[-3:] == "txt":
        raise ValueError("file doesn't exist or isn't a text document")

    if system == "unix": #na co chcemy zmienić
        unix(file)
    elif system == "windows":
        windows(file)
    else:
        raise ValueError("it has to be either unix or windows to convert a text")


def windows(text_doc: str): #zmienia lf na crlf
    """a function that converts ends of lines in text documents from unix to windows style.
    @param text_doc: a path to the text document that is about to be converted
    """

    file = open(text_doc, "rb")
    list_of_lines = file.readlines()  
    list_of_lines = [line.replace(b'\n', b"\r\n") if line [-2:] != b"\r\n" else line for line in list_of_lines]
    file.close()

    file = open(text_doc, "wb")
    file.writelines(list_of_lines)
    file.close()


def unix(text_doc: str): #zmienia crlf na lf
    """a function that converts ends of lines in text documents from windows to unix style.
    @param text_doc: a path to the text document that is about to be converted
    """

    file = open(text_doc, "rb")
    list_of_lines = file.readlines()
    list_of_lines = [line.replace(b'\r\n', b"\n") for line in list_of_lines]
    file.close()

    file = open(text_doc, "wb")
    file.writelines(list_of_lines)
    file.close()


if __name__ == "__main__":

    if len(sys.argv) > 3:
        raise ValueError("too many variables")
    elif len(sys.argv) < 3:
        raise ValueError("not enough variables")
    else:
	    main(sys.argv[1], sys.argv[2])