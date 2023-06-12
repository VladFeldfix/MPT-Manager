# This library will help you to create a customazible Personal Assistant application for any purpose
# The library will generate the Personal Assistant's GUI and some functions

import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import sys
import os
import datetime
import sqlite3

class PersonalAssistant:
    def __init__(self, program_name, rev):
        # Create GUI
        self.__root = tkinter.Tk()
        self.__root.geometry("1000x600")
        self.__root.minsize(640,480)
        title = program_name+" v."+rev
        self.__root.title(title)
        self.__root.protocol("WM_DELETE_WINDOW", self.exit)
        self.icon = 'favicon.ico'
        if os.path.isfile(self.icon):
            self.__root.iconbitmap(self.icon)
        else:
            self.fatal_error("Missing file favicon.ico")
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)

        # Personal Assistant frame
        frame = LabelFrame(self.__root, text=title+" [PA v.0.1]")
        frame.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # console scroll bar
        console_frame = Frame(frame)
        console_frame.grid(column=0, row=0, padx=5, pady=5, columnspan=2, sticky='nsew')
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        vscrollbar = Scrollbar(console_frame, orient='vertical')
        vscrollbar.grid(column=1, row=0, sticky='nsew')
      
        # console
        self.__console = Text(console_frame, state=DISABLED, yscrollcommand=vscrollbar.set)
        self.__console.grid(column=0, row=0, sticky='nsew')
        self.__console.tag_configure("PA", foreground="#0048ff", background="#e9edf7")
        self.__console.tag_configure("ERROR", foreground="#e82e2e", background="#f5d3d3")
        self.__console.tag_configure("USER", foreground="#2d362a", background="#619c46")
        vscrollbar.config(command=self.__console.yview) # attach scrollbar to console

        # input
        self.__input = Entry(frame)
        self.__input.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
        self.__input.config(state=DISABLED)

        # send button
        self.__input_button_var = tkinter.IntVar()
        self.__input_button = Button(frame, text="Send", command=lambda: self.__submit(""))
        self.__input_button.grid(column=1, row=1, padx=5, pady=5, sticky="nsew")
        self.__input_button.config(state=DISABLED)
        self.__root.bind('<Return>', self.__submit)
        self.__input.focus()
        
        # progress bar
        self.__progress = ttk.Progressbar(frame, orient='horizontal', mode='determinate')
        self.__progress.grid(column=0, row=2, padx=5, pady=5, columnspan=2, sticky="nsew")

        # main menu
        self.main_menu = {}

        # load settings
        self.__load_settings()

        # global variables
        self.__currently_displaying_database = False

    # PUBLIC FUNCTIONS
    def print(self, text):
        # prints the given text to the console
        self.__send_text_to_console(text, "PA")
        self.__console.see(END)
        self.__root.update_idletasks()

    def clear(self):
        # clears the console
        self.__console.config(state=NORMAL)
        self.__console.delete('1.0', END)
        self.__console.config(state=DISABLED)
        self.__console.see(END)
        self.__root.update_idletasks()
    
    def progress_bar_value_set(self, percent):
        # set thg value of the progress bar
        self.__progress['value'] = percent
        self.__root.update_idletasks()
    
    def progress_bar_value_get(self):
        # returns thg value of the progress bar
        return self.__progress['value']
    
    def display_menu(self):
        # this function clears the console and displays a menu
        # after the menu is displayed, Personal Assistant requests an input
        # if the input is a valid number, Personal Assistant calls the given function. otherwise it displays an error
        self.clear()
        # settings
        if not "SETTINGS" in self.main_menu:
            self.main_menu["SETTINGS"] = self.__settings
        if not "HELP" in self.main_menu:
            self.main_menu["HELP"] = self.help
        if not "EXIT" in self.main_menu:
            self.main_menu["EXIT"] = self.exit
        msg = "Hello, I am your personal assistant! How can I help you?\n"
        i = 0
        self.__main_menu_enumirated = {}
        for key, value in self.main_menu.items():
            i += 1
            msg += str(i)+". "+key+"\n"
            self.__main_menu_enumirated[i] = value
        msg = msg[:-1]
        self.print(msg)
        self.__activate_menu(i)
    
    def input(self, prompt):
        if prompt != "":
            self.__send_text_to_console(prompt+" >", "PA")
        self.__input.config(state=NORMAL)
        self.__input_button.config(state=NORMAL)
        self.pause()
        text = self.__input.get()
        self.__send_text_to_console(text, "USER")
        self.__input.delete(0,END)
        self.__input.config(state=DISABLED)
        self.__input_button.config(state=DISABLED)
        self.__console.see(END)
        self.__root.update_idletasks()
        return text
    
    def question(self, text):
        ans = self.input(text+" (Y/N)") # get answer
        ans = ans.upper() # make sure its uppercase
        # take only the first letter
        if len(ans) > 0: 
            ans = ans[0]
        return ans == "Y"
    
    def choose(self, text, choices, default):
        # display the message
        self.print(text)

        # display choices
        i = 0
        possibleChoices = []
        for choice in choices:
            i += 1
            possibleChoices.append(str(i))
            self.print(str(i)+". "+choice)

        # get input
        ans = self.input("Press the relevant number to select your choice")

        # process input
        if ans in possibleChoices:
            return choices[int(ans)-1]
        else:
            return default

    def error(self, text):
        self.__send_text_to_console(text, "ERROR")
        self.__console.see(END)
        self.__root.update_idletasks()
    
    def fatal_error(self, text):
        self.__send_text_to_console("Fatal error! "+text, "ERROR")
        self.__console.see(END)
        self.__root.update_idletasks()
        self.pause()
        self.exit()
    
    def pause(self):
        self.__input_button.wait_variable(self.__input_button_var)

    def save(self, content, initialdir, defaultType, possibleTypes):
        # save a file
        file = fd.asksaveasfile(initialdir=initialdir, initialfile = 'Untitled', defaultextension=defaultType, filetypes=possibleTypes)
        if not file is None:
            self.print("Saved!")
            file.write(content)
            file.close()
        else:
            self.print("File not saved!")
    
    def load_file(self, initialdir, defaultType, possibleTypes):
        # load a file
        file = fd.askopenfilename(initialdir=initialdir, defaultextension=defaultType, filetypes=possibleTypes)
        return file

    def load_files(self, initialdir, defaultType, possibleTypes):
        # load a directory
        files = fd.askopenfilenames(initialdir=initialdir, defaultextension=defaultType, filetypes=possibleTypes)
        return files

    def load_folder(self, initialdir):
        # load a directory
        files = fd.askdirectory(initialdir=initialdir)
        return files

    def restart(self):
        self.input("Press ENTER key to restart")
        self.progress_bar_value_set(0)
        self.display_menu()

    def script(self, file, functions):
        if os.path.isfile(file):
            f = open(file, 'r')
            lines = f.readlines()
            f.close()
            script = []
            for line in lines:
                line = line.replace("\n", "").replace(")", "").strip()
                line = line.split("(")
                Function = line[0]
                if "," in line[1]:
                    line = line[1].split(",")
                    Args = line
                else:
                    Args = []
                script.append((Function, Args))
            
            for x in script:
                key = x[0]
                value = x[1]
                if key in functions:
                    functions[key](value)
                else:
                    self.error("No such function: "+key)
        else:
            self.error("File not found: "+file)

    def today(self):
        # get today
        now = datetime.datetime.now()
        yyyy = str(now.year)
        mm = str(now.month).zfill(2)
        dd = str(now.day).zfill(2)
        return yyyy+"-"+mm+"-"+dd

    def read_csv(self, file):
        if os.path.isfile(file):
            f = open(file, 'r')
            lines = f.readlines()
            f.close()
            content = []
            for line in lines:
                line = line.replace("\n", "").strip()
                line = line.split(",")
                content.append(line)
            return content
        else:
            self.error("File not found: "+file)

    def get_setting(self, key):
        if key in self.__general_settings:
            return self.__general_settings[key]
        else:
            self.fatal_error("Missing setting vriable: "+key)
    
    def display_database(self, db, table, order_by):
        if not self.__currently_displaying_database:
            self.__currently_displaying_database = True
            # set GUI
            # top window
            self.__dbbox = Toplevel(self.__root)
            self.__dbbox.geometry("640x480")
            self.__dbbox.minsize(320,240)
            self.__dbbox.columnconfigure(0, weight=1)
            self.__dbbox.rowconfigure(0, weight=1)
            self.__dbbox.protocol("WM_DELETE_WINDOW", self.exit_database)
            if os.path.isfile(self.icon):
                self.__dbbox.iconbitmap(self.icon)
            else:
                self.fatal_error("Missing file favicon.ico")

            # frame
            frame = LabelFrame(self.__dbbox, text=db+" - "+table)
            frame.grid(sticky='nsew', padx=10, pady=10)
            frame.columnconfigure(1, weight=1)
            frame.rowconfigure(1, weight=1)

            # scrollbar
            vscrollbar = Scrollbar(frame, orient='vertical')
            vscrollbar.grid(column=4, row=1, sticky='nsew', pady=5)
            hscrollbar = Scrollbar(frame, orient='horizontal')
            hscrollbar.grid(column=0, row=2, sticky='nsew', padx=5, columnspan=4)

            # the database itself
            self.__database_display_window = Listbox(frame, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set, font="TkFixedFont", activestyle="none")
            self.__database_display_window.grid(column=0, row=1, padx=5, pady=5, sticky='nsew', columnspan=4)
            vscrollbar.config(command=self.__database_display_window.yview) # attach scrollbar to console
            hscrollbar.config(command=self.__database_display_window.xview) # attach scrollbar to console

            # set global variables
            self.__database = db
            self.__db_table = table
            self.__db_order_by = order_by

            # fill
            self.update_database()
        
        else:
            self.error("Error! Database window is already open")

    def update_database(self):
        # empty
        self.__database_display_window.delete(0, END)

        # get data
        data = []
        longest_column = {0:1} # column number: size
        con = sqlite3.connect(self.__database)
        cur = con.cursor()
        cur.execute("SELECT * FROM "+self.__db_table+" ORDER BY '"+self.__db_order_by+"'")
        fetched_values = cur.fetchall()

        # get headers
        headers = [i[0] for i in cur.description]
        data.append(headers)
        
        # get rows
        if len(fetched_values) > 0:
            for row in fetched_values:
                data.append(row)

        # calculate longest column
        for row in data:
            i = 0
            for col in row:
                if not i in longest_column:
                    longest_column[i] = min(len(col), 100)
                else:
                    if longest_column[i] < len(col):
                        longest_column[i] = min(len(col), 100)
                i += 1

        # fill
        for row in data:
            i = 0
            display_row = ""
            for col in row:
                col = str(col)
                column_size = longest_column[i]
                for j in range(column_size+1):
                    if j < len(col):
                        display_row += col[j]
                    else:
                        display_row += " "
                display_row += " "
                i += 1
            self.__database_display_window.insert(END, display_row)
            self.__root.update_idletasks()
        self.__database_display_window.itemconfig(0, foreground="White", background="Black")
    
    def exit_database(self):
        self.__dbbox.destroy()
        self.__currently_displaying_database = False

    def exit(self):
        if self.__currently_displaying_database:
            self.__dbbox.destroy()
        self.__root.destroy()
        os._exit(1)
        sys.exit()
    
    def help(self):
        if os.path.isfile("help.pdf"):
            os.popen("help.pdf")
        else:
            self.error("Missing file: help.pdf")
        self.restart()

    def run(self):
        # activates the GUI
        self.__root.mainloop()

    # PRIVATE FUNCTIONS
    def __submit(self, event):
        self.__input_button_var.set(1)
    
    def __activate_menu(self, size):
        ans = self.input("Press the number of the action you want to perform")
        error = False
        try:
            ans = int(ans)
        except:
            self.error("Invalid Input!")
            self.restart()
            error = True
        if not error:
            if ans in range(1,size+1):
                self.__main_menu_enumirated[ans]()
            else:
                self.error("Invalid Input!")
                self.restart()

    def __load_settings(self):
        settings = "settings.txt"
        self.__general_settings = {}
        if os.path.isfile(settings):
            file = open(settings, 'r')
            lines = file.readlines()
            file.close()
            for line in lines:
                line = line.replace("\n","").strip()
                line = line.split(" --> ")
                self.__general_settings[line[0]] = line[1]
        else:
            self.fatal_error("Missing file: settings.txt")
    
    def __write_settings(self):
        if len(self.__general_settings) > 0:
            file = open("settings.txt", 'w')
            for key, value in self.__general_settings.items():
                file.write(str(key)+" --> "+str(value)+"\n")
            file.close()
    
    def __settings(self):
        self.print("Current Settings:")
        if len(self.__general_settings) == 0:
            self.print("There are no settings variables.\nTo Make a setting variable open file settings.txt and write it in the following format Variable --> Value")
            self.restart()
        else:
            for key, value in self.__general_settings.items():
                self.print(str(key)+" --> "+str(value))
            user_input = self.input("Would you like to change the current settings? Y/N").upper()
            if len(user_input) > 0:
                if user_input[0] == "Y":
                    for key, value in self.__general_settings.items():
                        user_input = self.input(str(key)+" --> "+"(Leave empty to keep current value: "+str(value))
                        if user_input != "":
                            self.__general_settings[key] = user_input
        self.__write_settings()
        self.restart()
    
    def __send_text_to_console(self, text, text_type):
        self.__console.config(state=NORMAL)
        if "\n" in text:
            lines = text.split("\n")
            for line in lines:
                self.__console.insert(END, str(line)+"\n", text_type)
                self.__console.see(END)
        else:
            self.__console.insert(END, str(text)+"\n", text_type)
        self.__console.config(state=DISABLED)
    
