
#Napisz program, który będzie rysował wykresy funkcji na płaszczyźnie. Program ma oferować użytkownikowi prosty interfejs graficzny o następujących funkcjonalnościach:
#• pole tekstowe do wpisania wzoru funkcji,
#• opcjonalnie przyciski do budowania wzoru funkcji (jak w kalkulatorach, czyli przyciski z nawiasami, operatorami arytmetycznymi oraz wspieranymi funkcjami elementarnymi),
#• pola tekstowe do określenia zakresów na osiach X i Y,
#• pola tekstowe do określenia tytułu rysunku oraz etykiet osi,
#• płótno, na którym pojawia się wykres,
#• przycisk (check button) wyboru legendy,
#• przycisk uruchamiający rysowanie,
#• przycisk kończący program.
#Program powinien dopuszczać możliwość rysowania funkcji na jednym wykresie (w polu wpisywania ich wzory należy oddzielać średnikami) i automatycznie tworzyć legendę na podstawie podanych wzorów. Udokumentuj
#kod tego programu zgodnie z zasadami opisanymi w dokumentcie https: //www.python.org/dev/peps/pep-0257/. Wygeneruj dokumentację programu przy pomocy narzędzia pydoc1
#-----------do wywołania z konsoli!-------------

"""this module creates an app, which plots function formulas."""
from functools import partial
import sys
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class Application(QMainWindow):
    """ Class building the application window."""

    def __init__(self):
        """Function that initializes the window, creates the widgets"""

        super().__init__()
        
        self.setWindowTitle('Plots')
        self.setFixedSize(700, 820)
        
        self.generalLayout = QVBoxLayout()
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.generalLayout)

        self.buttons = {}
        
        self.createDisplay()
        self.createEntries()
        self.createButtons()
        self.createCanva()

    def createDisplay(self):
        """Function that creates the main entry, few special buttons and their labels"""

        displayLayout = QGridLayout()
        self.formula = QLabel("THE FORMULA")
        self.entry = QLineEdit()
        
        self.entry.setFixedHeight(40)
        self.entry.setAlignment(Qt.AlignRight)
        self.entry.setReadOnly(False)

        self.form = QLabel("Enter the formula here and click DRAW")

        self.buttons["EXIT"] = QPushButton("EXIT")
        self.buttons["EXIT"].setFixedSize(100, 30)

        self.buttons["DRAW"] = QPushButton("DRAW")
        self.buttons["DRAW"].setFixedSize(100, 40)
        displayLayout.addWidget(self.buttons["DRAW"], 1, 1)

        displayLayout.addWidget(self.entry, 1, 0)
        displayLayout.addWidget(self.form, 0, 0)
        displayLayout.addWidget(self.buttons["EXIT"], 0, 1)

        self.generalLayout.addLayout(displayLayout)
        


    def createButtons(self):
        """Function that creates most of the buttons"""

        buttonsLayout = QGridLayout()
        names = ["7","8","9","C","Bck","4","5","6","+","-","sqrt(x)","1","2","3","/","*","**","0","x",";",".","(",")","sin(x)","cos(x)","tan(x)","exp(x)","pi","e"]
        positions = [(i, j) for i in range(1,6) for j in range(1,7) if (i,j) != (1,4)]

        for i in range(0,len(names)):
            self.buttons[names[i]] = QPushButton(names[i])
            self.buttons[names[i]].setFixedSize(70, 40)
            buttonsLayout.addWidget(self.buttons[names[i]], positions[i][0], positions[i][1])

        self.generalLayout.addLayout(buttonsLayout)

    def createEntries(self):
        """ Function that creates all the entries and their labels and a checkbox"""

        entriesLayout = QGridLayout()

        self.x_dom = QLabel("X domain - a,b")
        self.entry1 = QLineEdit()
        self.entry1.setFixedSize(110, 30)
        self.y_dom = QLabel("Y domain - a,b")
        self.entry2 = QLineEdit()
        self.entry2.setFixedSize(110, 30)

        self.lab_title = QLabel("TITLE")
        self.title = QLineEdit()
        self.title.setFixedSize(110, 30)

        self.lab_x = QLabel("X LABEL")
        self.lab_y = QLabel("Y LABEL")
        self.etx = QLineEdit()
        self.etx.setFixedSize(110, 30)
        self.ety = QLineEdit()
        self.ety.setFixedSize(110, 30)

        entriesLayout = QGridLayout()
        entriesLayout.addWidget(self.lab_title, 0,1)
        entriesLayout.addWidget(self.lab_x, 0,3)
        entriesLayout.addWidget(self.lab_y, 0,4)
     

        entriesLayout.addWidget(self.title,1,1)
        entriesLayout.addWidget(self.etx,1,3)
        entriesLayout.addWidget(self.ety,1,4)

        entriesLayout.addWidget(self.x_dom,0,6)
        entriesLayout.addWidget(self.y_dom, 0,7)
        entriesLayout.addWidget(self.entry1,1,6)
        entriesLayout.addWidget(self.entry2,1,7)

        self.box = QCheckBox("Legend")
        self.box.setChecked(True)
        entriesLayout.addWidget(self.box, 1,8)

        self.generalLayout.addLayout(entriesLayout)

    def createCanva(self):
        """Function that creates a canva for plotting"""

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        canvaLayout = QVBoxLayout()
        canvaLayout.addWidget(self.canvas)

        self.generalLayout.addLayout(canvaLayout)

    def setDisplayText(self, text):
        """Function that sets main entry's text."""
        self.entry.setText(text)
        self.entry.setFocus()

    def displayText(self):
        """Function that gets formula from main entry"""
        return self.entry.text()

    def clearDisplay(self):
        """Function that clears the main entry"""

        self.setDisplayText('')

    def backDisplay(self):
        """Function for the backspace button"""

        text = self.entry.text()[:-1]
        self.setDisplayText(text)

class Drawer:
    """A class that plots the given formula on the screen"""

    def __init__(self, window):
        """ A function that initializes the class and interpret events"""

        self.window = window
        self.check()

    def check(self):
        """ A function that interpret events based on which button has been pressed """

        for button, btn in self.window.buttons.items():
            if button not in {'Bck', 'C',"DRAW","EXIT"}:
                btn.clicked.connect(partial(self.buildExpression, button))
        
        self.window.buttons['C'].clicked.connect(self.window.clearDisplay)
        self.window.buttons['Bck'].clicked.connect(self.window.backDisplay)
        self.window.buttons["DRAW"].clicked.connect(self.drawing)
        self.window.buttons["EXIT"].clicked.connect(self.done)

    def drawing(self):
        """A function that checks for any possible errors and plots the given formula"""

        function_list = self.window.displayText().split(";")
        x_dom = self.window.entry1.text().split(",")
        y_dom = self.window.entry2.text().split(",")
        f_title = self.window.title.text()
        x_label = self.window.etx.text()
        y_label = self.window.ety.text()

        try:
            if len(x_dom) != 2 or len(y_dom) != 2:
                QMessageBox.about(self.window, "Domain Error", "wrong domain")
                return
            elif int(x_dom[0]) >= int(x_dom[1]) or int(y_dom[0]) >= int(y_dom[1]):
                QMessageBox.about(self.window, "Domain Error", "wrong domain")
                return
        except:
            QMessageBox.about(self.window, "Domain Error", "wrong domain")
            return

        self.window.figure.clear()

        ax = self.window.figure.add_subplot(111)

        try:
            x = np.arange(int(x_dom[0]),int(x_dom[1]),0.1)
            plt.ylim(int(y_dom[0]),int(y_dom[1]))
        except ValueError:
            QMessageBox.about(self.window, "Domain Error", "wrong domain, not integers")
            return

        plt.title(f_title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)

        for y in function_list:
            if "sqrt" in y and int(x_dom[0]) < 0:
                QMessageBox.about(self.window, "Value Error", "sqrt takes only positive values")
                return
            if "x" not in y:
                try:
                    y = add_np(y)
                    y = constant_function(y,x)
                    ax.plot(x,y)
                except:
                    QMessageBox.about(self.window, "Formula Error", "wrong formula")
            else:
                try:
                    y = add_np(y)
                    y = add_times(y)
                    y1 = eval(y)
                    ax.plot(x,y1)
                except SyntaxError:
                    QMessageBox.about(self.window, "Formula Error", "wrong formula")
                    return
                except TypeError:
                    QMessageBox.about(self.window, "Formula Error", "wrong formula")
                    return
                except ValueError:
                    QMessageBox.about(self.window, "Formula Error", "wrong formula")
                    return
                except NameError:
                    QMessageBox.about(self.window, "Formula Error", "wrong formula")
                    return
            

        if self.window.box.isChecked():
            plt.legend(function_list)
           
        self.window.canvas.draw()

    def buildExpression(self, text_exp):
        """A function that displays text in the main entry after clicking the button."""
    
        expression = self.window.displayText() + text_exp
        self.window.setDisplayText(expression)

    def done(self):
        """A function that closes the app"""

        sys.exit()

def add_np(text: str):
    """A function that adds 'np' to the formula's elements
    @param text: a text to format
    return text: a formatted text
    """
    
    for i in ["sin","cos","tan","sqrt","e","pi"]:
        if i in text:
            text = text.replace(i, "np." + str(i))
    return text

def add_times(text):
    """A function that replaces the expression's part in which a '*' was missing
    @param text: a text to format
    return text: a formatted text
    """
    
    for i in ["0x","1x","2x","3x","4x","5x","6x","7x","8x","9x",")x","pix"]:
        if i in text:
            text = text.replace(i, i[:-1] + "*" + i[-1])
    if "ex" in text:
        text = text.replace("ex","e*x")
        text = text.replace("np.e*xp","np.exp")
    if "xnp.e" in text:
        text = text.replace("xnp.e","x*np.e")
    for i in ["x1","x2","x3","x4","x5","x6","x7","x8","x9","x(","xpi"]:
        if i in text:
            text = text.replace(i, "x*" + i[1:])
    for i in ["pin","pi("]:
        text = text.replace(i, "pi*" + i[2:])
    for i in ["en", "e("]:
        text = text.replace(i, "e*" + i[1:]) 
    if ")n" in text:
        text = text.replace(")n", ")*n")
    
    return text

def constant_function(formula, domain):
    """ A function that handles constant functions and makes them possible to draw"""

    if "x" not in formula:
        vector = [eval(formula) for i in range(0,len(domain))]
        return vector
    else:
        return formula
        
def main():
    """Main function"""

    appl = QApplication(sys.argv)
    window = Application()
    window.show()
    Drawer(window)
    sys.exit(appl.exec_())

if __name__ == '__main__':
    main()
    