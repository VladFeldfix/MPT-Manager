import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import sys
import os
import datetime
from datetime import date as date_n
import re

class SmartConsole:
    # CONSTRUCTOR
    def __init__(self, program_name, rev):
        # GUI setup
        self.__title = program_name+" v"+rev

        # main window
        self.__root = tkinter.Tk()
        self.__root.geometry("1000x600")
        self.__root.minsize(640,480)
        self.__root.title(self.__title)
        self.__root.protocol("WM_DELETE_WINDOW", self.exit)
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)
        
        # console frmae
        frame = LabelFrame(self.__root, text=self.__title+" [SmartConsole v1.0]")
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
        self.__console.tag_configure("PRINT", foreground="#0048ff", background="#e9edf7")
        self.__console.tag_configure("ERROR", foreground="#e82e2e", background="#f5d3d3")
        self.__console.tag_configure("FATAL_ERROR", foreground="#ffffff", background="#e82e2e")
        self.__console.tag_configure("INPUT", foreground="#2d362a", background="#619c46")
        self.__console.tag_configure("NOTICE", foreground="#fcf6d4", background="#d1b52a")
        self.__console.tag_configure("ABORT", foreground="#ffffff", background="#949494")
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

        # main_menu
        self.main_menu = {}

        # settings
        self.__settings = self.__load_settings()

        # help
        self.test_path("help.pdf")

        # setup icon
        if os.path.isfile('favicon.ico'):
            self.__root.iconbitmap('favicon.ico')
        else:
            self.fatal_error("Missing file: favicon.ico")
    
    # CODE FLOW
    def start(self):
        # clear console
        self.clear()

        # display title
        text_length = len(self.__title)
        msg = "---"+"-"*text_length+"---\n"
        msg += "-- "+self.__title+" --\n"
        msg += "---"+"-"*text_length+"---\n"
        msg += "MAIN MENU:"
        
        # add essentials
        if not "SETTINGS" in self.main_menu:
            self.main_menu["SETTINGS"] = self.__edit_settings
        if not "HELP" in self.main_menu:
            self.main_menu["HELP"] = self.help
        if not "EXIT" in self.main_menu:
            self.main_menu["EXIT"] = self.exit

        # display options
        choices = []
        for key, value in self.main_menu.items():
            choices.append(key)

        # process answer
        ans = self.choose(msg, choices, "")
        if ans != "":
            self.main_menu[ans]()
        else:
            self.error("Invalid input: "+str(ans))
            self.restart()

    def restart(self):
        self.input("Press ENTER key to restart")
        self.start()

    def pause(self):
        self.__input_button.wait_variable(self.__input_button_var)

    def exit(self):
        os._exit(1)
        sys.exit()

    def abort(self):
        self.__send_text_to_console("Procedure aborted", "ABORT")
        self.__console.see(END)
        self.__root.update_idletasks()
        self.restart()
    
    def gui(self):
        self.__root.mainloop()

    # PRINT
    def print(self, text):
        # prints the given text to the console
        self.__send_text_to_console(text, "PRINT")
        self.__console.see(END)
        self.__root.update_idletasks()

    def clear(self):
        # clears the console
        self.__console.config(state=NORMAL)
        self.__console.delete('1.0', END)
        self.__console.config(state=DISABLED)
        self.__console.see(END)
        self.__root.update_idletasks()

    def notice(self, text):
        self.__send_text_to_console("NOTICE! "+text, "NOTICE")
        self.__console.see(END)
        self.__root.update_idletasks()

    def error(self, text):
        self.__send_text_to_console("ERROR "+text, "ERROR")
        self.__console.see(END)
        self.__root.update_idletasks()

    def fatal_error(self, text):
        self.__send_text_to_console("ERROR "+text, "FATAL_ERROR")
        self.__console.see(END)
        self.__root.update_idletasks()
        self.pause()
        self.exit()

    # INPUT
    def input(self, prompt):
        if prompt != "":
            self.__send_text_to_console(prompt+" >", "PRINT")
        self.__input.config(state=NORMAL)
        self.__input_button.config(state=NORMAL)
        self.pause()
        text = self.__input.get()
        self.__send_text_to_console(text, "INPUT")
        self.__input.delete(0,END)
        self.__input.config(state=DISABLED)
        self.__input_button.config(state=DISABLED)
        self.__console.see(END)
        self.__root.update_idletasks()
        return text

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

    def question(self, text):
        ans = self.input(text+" [Y/N]") # get answer
        ans = ans.upper() # make sure its uppercase
        # take only the first letter
        if len(ans) > 0: 
            ans = ans[0]
        
        if ans == "Y":
            return True
        if ans == "N":
            return False
        else:
            self.error("Invalid input!")
            return self.question(text)
            

    def __submit(self, event):
        self.__input_button_var.set(1)
    
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
    
    # SETTINGS
    def __load_settings(self):
        return_value = {}
        self.test_path("settings.txt")
        file = open("settings.txt", "r")
        lines = file.readlines()
        file.close()
        for line in lines:
            line = line.replace("\n", "")
            if ">" in line:
                line = line.split(">")
                if len(line) > 1:
                    var = line[0].strip()
                    val = line[1].strip()
                    return_value[var] = val
        return return_value
    
    def get_setting(self, var):
        if var in self.__settings:
            return self.__settings[var]
        else:
            self.fatal_error("Missing Setting: "+var)
    
    def __edit_settings(self):
        self.test_path("settings.txt")
        os.popen("settings.txt")
        self.restart()
    
    def help(self):
        self.test_path("help.pdf")
        os.popen("help.pdf")
        self.restart()
    
    # FILE HANDLER
    def test_path(self, path):
        if not os.path.isdir(path) and not os.path.isfile(path):
            self.fatal_error("Missing path: "+path)
    
    def csv_to_dict(self, path, headers):
        return_value = {}
        self.test_path(path)
        file = open(path, 'r')
        lines = file.readlines()
        file.close()
        ln = 0
        for line in lines:
            ln += 1
            line = line.replace("\n", "")
            if "," in line:
                original = line
                line = line.split(",")
                if len(line) == len(headers):
                    var = line[0]
                    val = line[1:]
                    if not var in return_value:
                        return_value[var] = val
                    else:
                        self.fatal_error("In file: "+path+"\nLine #"+str(ln)+": "+original+"\nNon unique primary key: "+var)
                else:
                    self.fatal_error("In file: "+path+"\nLine #"+str(ln)+": "+original+"\nIncorrect number of columns")
        return return_value

    # SCRIPT
    def run_script(self, path, functions):
        self.test_path(path)
        file = open(path, 'r')
        lines = file.readlines()
        file.close()

        ln = 0
        for line in lines:
            ln += 1
            if len(line) > 0:
                line = line.replace("\n", "")
                if "(" in line and ")" in line:
                    # get function name
                    tmp = line.split("(")
                    function = tmp[0].strip()

                    # get arguments
                    if len(tmp) == 2:
                        tmp = tmp[1].replace(")", "")
                        tmp = tmp.split(",")
                        agruments = []
                        for r in tmp:
                            agruments.append(r.strip())
                        
                        # activate function
                        if function in functions:
                            if len(agruments) == functions[function][1]:
                                functions[function][0](agruments)
                            else:
                                self.fatal_error("In script: "+path+"\nLine #"+str(ln)+" "+line+"\nWrong number of arguments!\nGiven: "+str(len(agruments))+"\nExpected: "+str(functions[function][1]))
                        else:
                            self.fatal_error("In script: "+path+"\nLine #"+str(ln)+" "+line+"\nUnknown function: "+function)
                    else:
                        self.fatal_error("In script: "+path+"\nLine #"+str(ln)+" "+line+"\nSyntex error. Expected syntex: FUNCTION( ARGUMENT0, ARGUMENT1, ARGUMENT2, ... )")
                else:
                    self.fatal_error("In script: "+path+"\nLine #"+str(ln)+" "+line+"\n'(' and ')' expected")
    # DATE
    def today(self):
        # get today
        now = datetime.datetime.now()
        yyyy = str(now.year)
        mm = str(now.month).zfill(2)
        dd = str(now.day).zfill(2)
        return yyyy+"-"+mm+"-"+dd
    
    def test_date(self, givenDate):
        # make sure the format is correct
        tmp = givenDate.replace("-","")
        tmp = re.sub('[^0-9]','', tmp)
        if len(tmp) < 8:
            self.error("Invalid date format: "+givenDate)
            return False
        
        # test year format
        YYYY = int(tmp[0:4])
        if not YYYY in range(0,10000):
            self.error("Invalid year format: "+str(YYYY)+" acceptable range 0-9999")
            return False
        YYYY = str(YYYY)
        YYYY = YYYY.zfill(4)

        # test month format
        MM = int(tmp[4:6])
        if not MM in range(1,13):
            self.error("Invalid month format: "+str(MM)+" acceptable range 1-12")
            return False
        MM = str(MM)
        MM = MM.zfill(2)

        # test day format
        DD = int(tmp[6:8])
        if not DD in range(1,32):
            self.error("Invalid day format: "+str(DD)+" acceptable range 1-31")
            return False
        DD = str(DD)
        DD = DD.zfill(2)
        
        # return true if date is good
        return True

    def compare_dates(self, firstDate, secondDate):
        if self.test_date(firstDate) and self.test_date(secondDate):
            firstDate = firstDate.replace("-","")
            secondDate = secondDate.replace("-","")
            date1 = date_n(int(firstDate[0:4]), int(firstDate[4:6]), int(firstDate[6:8]))
            date2 = date_n(int(secondDate[0:4]), int(secondDate[4:6]), int(secondDate[6:8]))
            return (date1 - date2).days
        else:
            return 0