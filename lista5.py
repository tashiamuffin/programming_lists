#Napisz program, który będzie przeliczał kursy walut. Program ma pobierać aktualne kursy
#walut z sieci (np. ze strony NBP) i oferować użytkownikowi prosty interfejs graficzny o następujących funkcjonalnościach:
#• wybór waluty źródłowej z listy rozwijanej,
#• wybór waluty docelowej z listy rozwijanej,
#• pole tekstowe do wpisania kwoty w walucie źródłowej,
#• pole do wyświetlenia wyniku,
#• przycisk uruchamiający obliczenia,
#• przycisk kończący program.
#Dodatkowo program powinien przechowywać ostatnią ściągniętą tabelę kursów i używać jej podczas kolejnego uruchomienia w przypadku braku połaczenia z Internetem.

import requests
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msb
from datetime import date


path = r"C:\Users\admin\OneDrive\Pulpit\inflista3\walut.txt"

def file_backup(path: str, currency_dict: dict):
    """
    a function that creates a file with backup currencies' list for future use
    @param path (str): a path to the file with currencies 
    @param currency_dict (dict): a dictionary with currencies
    """

    text = open(path, "w")
    for i in currency_dict.keys():
        text.write(str(i) + "\n" + str(currency_dict[i]) + "\n")
    text.write(str(date.today().strftime("%d/%m/%Y")))
    text.close()

def get_currencies(path: str):
    """
    a function that gathers currencies and their bids - download them from NBP website or from backup file
    @param path (str): a path to the backup file
    @return currencies: dictonary with currencies
    @return names: list of names of the currencies
    @return date_tod: a date, from which the data was gathered
    """

    if not os.path.exists(path) or os.path.getsize(path) == 0:
        raise ValueError("your path doesn't exist or the dictionary is empty") 

    try:
        response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C/")
    except requests.exceptions.ConnectionError:
        return fail(path)

    if response:
        message = response.json()[0]
        data = message['rates']
        currencies = {}
        currencies['PLN'] = "1"
        names = []
        names.append("PLN")
        for i in range(0,len(data)):
            currencies[data[i]['code']] = data[i]['ask']
            names.append(data[i]['code'])
        file_backup(path, currencies)
        date_tod = date.today().strftime("%d/%m/%Y")
        return currencies, names, date_tod
    else:
        return fail(path)

def fail(path: str):
    """
    a function that gathers data (currency rates) from the text file in case of no Internet
    @param path: a path to the text document with backup data
    @return currencies: dictonary with currencies
    @return names: list of names of the currencies
    @return date_tod: a date, from which the data was gathered
    """

    text = open(path, "r")
    message = text.readlines()
    currencies = {}
    names = []
    for i in range(0, len(message)-1,2):
        currencies[message[i][:-1]] = message[i+1][:-1]
        names.append(message[i][:-1])
    date_tod = message[-1]
    return currencies, names, date_tod

def calculating(given: str, wanted: str, amount: float):
    """
    a function that converts the money
    @param given (str): the given currency
    @param wanted (str): the wanted currency
    @param amount (float): the amount of money to convert
    @return result (float): the converted amount of money
    """

    currencies_dict = get_currencies(path)[0]
    rate_given = currencies_dict[given]
    rate_wanted = currencies_dict[wanted]
    result = round(amount* float(rate_given)/float(rate_wanted),2) 

    return result


class Application():
    def __init__(self):
        """
        a function initializing the currency converter widget
        """

        self.result = get_currencies(path)
        self.currencies = self.result[1]
        dat = self.result[2]
        self.window = tk.Tk()
        self.geometry = self.window.geometry(('450x300+200+200'))
        self.window.resizable(0, 0)
        self.color = self.window.configure(bg = "#F6FF97")

        self.title = self.window.title("Currency Converter")
        self.tekst = tk.Label(self.window, text="$ The Best Currency Converter $", background = "#76D7C4", relief = tk.RAISED, font = "Helvetica 16 bold italic")
        self.tekst.place(x = 55, y = 30)

        self.cb_value = tk.StringVar()
        self.cb_value2 = tk.StringVar()
        self.wart_var = tk.StringVar()

        self.combobox = ttk.Combobox(self.window, textvariable = self.cb_value) 
        self.combobox.place(x = 50, y = 80) 
        self.combobox['values'] = self.currencies  
        self.combobox.bind("<<ComboboxSelected>>", self.on_select_changed)
        self.combobox.current(0)

        self.combobox2 = ttk.Combobox(self.window, textvariable = self.cb_value2) 
        self.combobox2.place(x = 250, y = 80)
        self.combobox2['values'] = self.currencies
        self.combobox2.bind("<<ComboboxSelected>>", self.on_select_changed)
        self.combobox2.current(0)

        self.btn = tk.Button(self.window, text = "QUIT", foreground = "#4fa897",  command = quit)
        self.btn.pack(side = tk.BOTTOM)

        self.entry = tk.Entry(self.window, bd = 5, textvariable = self.wart_var)
        self.entry.place(x = 150, y = 110)
        self.wartosc = self.entry.get()

        self.output_desc = tk.Label(self.window, text = "the result:", font = "Helvetica 10")
        self.output_desc.place(x = 150,y = 200)

        self.date = tk.Label(self.window, text = "Date: ", foreground = "#4fa897", font = "Helvetica 12 bold italic", bg = "#F6FF97")
        self.date.place(x = 20,y = 270)

        self.output_label = tk.Label(self.window)
        self.output_label.place(x = 210,y = 200)

        self.date_label = tk.Label(self.window, text = str(dat), bg = "#F6FF97", font = "Helvetica 12 italic")
        self.date_label.place(x = 70,y = 270)

        self.btn2 = tk.Button(self.window, text = "Calculate!", font = "Helvetica 10")
        self.btn2.place(x = 185, y = 150)
        self.btn2.bind('<Button-1>', self.calculate)

        self.btn_info = tk.Button(self.window, text = "show info", bg = "#F6FF97", font = "Helvetica 10 bold italic", foreground = "#4fa897" )
        self.btn_info.place(x = 300, y = 265)
        self.btn_info.bind('<Button-1>', self.info)

        self.window.mainloop()


    def info(self, event):
        """
        a function that displays the info about the application
        """

        tk.messagebox.showinfo(title = "INFO", message = "choose one currency then the other from boxes and enter your desired amount of money and click calculate! The result will then appear") 


    def on_select_changed(self, event):
        """
        a function that checks whether the chosen currencies are the same or not
        """

        if self.cb_value.get() == self.cb_value2.get():
            tk.messagebox.showinfo(title = None, message = "We don't do that here, there is no sense in that.\nPlease choose another currency, so that I could display my abilities.")


    def calculate(self, event = None):
        """
        a function that converts and shows the result
        """

        given = str(self.cb_value.get())
        wanted = str(self.cb_value2.get())

        if given == wanted:
            tk.messagebox.showinfo(title = None, message = "I just told you we don't do that here, stop it and choose different currencies")

        else:
            amount = self.wart_var.get()
            dat = str(self.date)
            if "," in amount:
                amount = amount.replace(",", ".")

            try:
                self.amount = float(amount)
            except ValueError:
                tk.messagebox.showinfo(title = None, message = "Please enter A NUMBER, random input can't be calculated into currency")
                return

            if "." in amount and len(amount.split(".")[-1]) > 2:
                tk.messagebox.showinfo(title = None, message = "there is no 0.001 and above parts of money")
            elif self.amount <= 0:
                tk.messagebox.showinfo(title = None, message = "you don't want a negative amount of money in your bank account, do you?")
            else:
                result = calculating(given, wanted, self.amount)
                self.output_label.config(text = result, background = "#76D7C4", font = "Helvetica 16 bold italic")


if __name__ == "__main__":
    apl = Application()
