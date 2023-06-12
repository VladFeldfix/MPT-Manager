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
import re
import collections

class PersonalAssistant:
    def __init__(self, program_location, program_name, rev):
        # Create GUI
        # main window
        self.__root = tkinter.Tk()
        self.__root.geometry("1000x600")
        self.__root.minsize(640,480)
        self.__title = program_name+" v"+rev
        self.__root.title(self.__title)
        self.__root.protocol("WM_DELETE_WINDOW", self.exit)
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)

        # Personal Assistant frame
        frame = LabelFrame(self.__root, text=self.__title+" [PA v2.1]")
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
        self.__console.tag_configure("NOTICE", foreground="#fcf6d4", background="#d1b52a")
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

        # private global variables
        self.__currently_displaying_database = False
        self.__program_location = program_location
        self.__double_click_return_value = 0

        # load settings
        self.__load_settings()
        self.__generate_help()

        # public global variables
        self.main_menu = {}

        # setup icon
        self.icon = 'favicon.ico'
        if os.path.isfile(self.icon):
            self.__root.iconbitmap(self.icon)
        else:
            self.fatal_error("favicon.ico",201)

    # GLOBAL FUNCTIONALITY
    def run(self):
        self.__root.mainloop()
    
    def notice(self, text):
        self.__send_text_to_console(text, "NOTICE")
        self.__console.see(END)
        self.__root.update_idletasks()

    def error(self, text, code):
        preffix = self.__evaluate_error_prefix(code)
        self.__send_text_to_console("Error #"+str(code).zfill(3)+preffix+text, "ERROR")
        self.__console.see(END)
        self.__root.update_idletasks()
    
    def fatal_error(self, text, code):
        preffix = self.__evaluate_error_prefix(code)
        self.__send_text_to_console("Error #"+str(code).zfill(3)+preffix+text, "ERROR")
        self.__console.see(END)
        self.__root.update_idletasks()
        self.pause()
        self.exit()
    
    def __evaluate_error_prefix(self, code):
        code = int(code)
        if code in range(0,100):
            preffix = " System: "
        if code in range(100,200):
            preffix = " Invalid input: "
        if code in range(200,300):
            preffix = " Missing file: "
        if code in range(300,400):
            preffix = " Error in file: "
        if code > 399:
            preffix = " "
        return preffix
    
    def abort(self):
        self.__send_text_to_console("Procedure aborted", "ERROR")
        self.__console.see(END)
        self.__root.update_idletasks()
    
    def restart(self):
        self.input("Press ENTER key to restart")
        self.progress_bar_value_set(0)
        self.display_menu()

    def exit(self):
        if self.__currently_displaying_database:
            self.__dbbox.destroy()
        self.__root.destroy()
        os._exit(1)
        sys.exit()

    def __generate_help(self):
        # get the program code
        generate = True
        try:
            file = open(self.__program_location, 'r')
            lines = file.readlines()
            file.close()
        except:
            generate = False
            
        if generate:
            ListOfErrors = {}
            ListOfErrors[100] = "Main Menu got invalid input"
            ListOfErrors[101] = "Form got invalid input [Non-Numerical value]"
            ListOfErrors[102] = "Form got invalid input [Invalid date format]"
            ListOfErrors[103] = "Form got invalid input [Invalid year format]"
            ListOfErrors[104] = "Form got invalid input [Invalid month format]"
            ListOfErrors[105] = "Form got invalid input [Invalid day format]"
            ListOfErrors[200] = "help.pdf"
            ListOfErrors[201] = "favicon.ico"
            ListOfErrors[202] = "settings.txt"
            ListOfErrors[203] = "#Script-Filename"
            ListOfErrors[204] = "#CSV-Filename"
            ListOfErrors[300] = "settings.txt. Missing setting: #Setting Name"
            ListOfErrors[301] = "#script. Invalid function in script file"

            # get all errors
            line_number = 0
            for line in lines:
                line_number += 1
                if "error" in line or "fatal_error" in line:
                    add_to_error_text = False
                    error_text = ""
                    add_to_error_number = False
                    error_number = ""
                    if "(" in line and ")" in line and "," in line:
                        for ch in line:
                            if not add_to_error_number:
                                if ch == "\"":
                                    add_to_error_text = not add_to_error_text
                                else:
                                    if add_to_error_text:
                                        error_text += ch
                            if ch == "," and not add_to_error_text:
                                add_to_error_number = True
                            else:
                                if add_to_error_number and not add_to_error_text:
                                    if ch in "0123456789":
                                        error_number += ch
                        try:
                            error_number = int(error_number)
                        except:
                            print(error_number)
                            print(error_text)
                            self.fatal_error("LINE #"+str(line_number)+". "+line.strip()+" Invalid code number!", 1)
                        if not error_number in ListOfErrors:
                            ListOfErrors[error_number] = error_text
                        else:
                            line = line.replace("\n", "").strip()
                            self.fatal_error("LINE #"+str(line_number)+". "+line+" This error code is not unique!", 2)
            # read the code
            txt = "<html>\n"
            txt += "<head>\n"
            txt += "<title>"+self.__title+"</title>\n"
            txt += '<link rel="icon" type="image/png" href="favicon.ico"></link>\n'
            txt += '<style>\n'
            txt += 'html{font-family:Arial; background-color:#40454d;}\n'
            txt += 'p{display:inline-block; line-height: 2;}\n'
            txt += '#container{background-color:#f2f4f7; margin: 50 50 50 50; padding:50 50 50 50;}\n'
            txt += '</style>\n'
            txt += "</head>\n"
            txt += "<body>\n"
            txt += "<div id='container'>\n"
            txt += "<h1>"+self.__title+"</h1>\n"
            txt += "<h4>Application Guide</h4>\n"
            part = 0
            i = 0
            j = 0
            for line in lines:
                if part == 0:
                    if "GENERAL INFORMATION" in line:
                        part += 1
                        i = 0
                        j = 0
                        txt += "<hr><h2>PART I: GENERAL INFORMATION</h2><p>\n"

                # PART I: GENERAL INFORMATION
                if part == 1:
                    if "##" in line:
                        i += 1
                        j = 0
                        line = line.replace("##", "")
                        line = line.strip()
                        txt += str(i)+". "+line+"<br>\n"
                    if "#-" in line:
                        j += 1
                        line = line.replace("#-", "")
                        line = line.strip()
                        txt += "&emsp;"+str(i)+"."+str(j)+". "+line+"<br>\n"
                    if "HOW TO USE" in line:
                        if i == 0:
                            txt += "<p>-N/A-</p>\n"
                        part += 1
                        i = 0
                        j = 0
                        txt += "</p><hr><h2>PART II: HOW TO USE</h2><p>\n"  

                # PART II: HOW TO USE
                if part == 2:
                    if "##" in line:
                        i += 1
                        j = 0
                        line = line.replace("##", "")
                        line = line.strip()
                        txt += str(i)+". "+line+"<br>\n"
                    if "#-" in line:
                        j += 1
                        line = line.replace("#-", "")
                        line = line.strip()
                        txt += "&emsp;"+str(i)+"."+str(j)+". "+line+"<br>\n"
                    if "MAIN MENU" in line:
                        if i == 0:
                            txt += "<p>-N/A-</p>\n"
                        part += 1
                        i = 0
                        j = 0
                        txt += "</p><hr><h2>PART III: MAIN MENU</h2><p>\n"      

                # PART III: MAIN MENU
                if part == 3:
                    if "##" in line:
                        i += 1
                        j = 0
                        line = line.replace("##", "")
                        line = line.strip()
                        txt += "<b>"+str(i)+". "+line+"</b><br>\n"
                    if "#-" in line:
                        j += 1
                        line = line.replace("#-", "")
                        line = line.strip()
                        txt += "&emsp;"+str(i)+"."+str(j)+". "+line+"<br>\n"
                    if "SCRIPT FUNCTIONS" in line:
                        if i == 0:
                            txt += "<p>-N/A-</p>\n"
                        part += 1
                        i = 0
                        j = 0
                        txt += "</p><hr><h2>PART IV: SCRIPT</h2><p>\n"     
                
                # PART IV: SCRIPT
                if part == 4:
                    if "FUN:" in line:
                        i += 1
                        line = line.replace("FUN:", "").replace("#", "")
                        line = line.strip()
                        txt += "<b>"+str(i)+". "+line+"</b><br>\n"
                        j = 0
                    if "ARG:" in line:
                        j += 1
                        line = line.replace("ARG:", "").replace("#", "")
                        line = line.strip()
                        txt += "&emsp;"+str(i)+"."+str(j)+". "+line+"<br>\n"
                    if "RTN:" in line:
                        j += 1
                        line = line.replace("RTN:", "Return Value:").replace("#", "")
                        line = line.strip()
                        txt += "&emsp;"+str(i)+"."+str(j)+". "+line+"<br>\n"
                    if "SETTINGS" in line:
                        if i == 0:
                            txt += "<p>-N/A-</p>\n"
                        part += 1
                        i = 0
                        j = 0
                        txt += "</p><hr><h2>PART V: SETTINGS</h2><p>\n"      
                
                # PART V: SETTINGS
                if part == 5:
                    if "-->" in line:
                        i += 1
                        line = line.replace("#", "")
                        line = line.split("-->")
                        key = line[0]
                        val = line[1]
                        key = key.strip()
                        val = val.strip()
                        txt += "<b>"+str(i)+". "+key+"</b> > "+val+"<br>\n"
                    if "RELATED FILES" in line:
                        if i == 0:
                            txt += "<p>-N/A-</p>\n"
                        part += 1
                        i = 0
                        j = 0
                        txt += "</p><hr><h2>PART VI: RELATED FILES</h2><p>\n"
                
                # PART VI: RELATED FILES
                if part == 6:
                    if "##" in line:
                        i += 1
                        j = 0
                        line = line.replace("##", "")
                        line = line.strip()
                        txt += "<b>"+str(i)+". "+line+"</b><br>\n"
                    if "#-" in line:
                        j += 1
                        line = line.replace("#-", "")
                        line = line.strip()
                        txt += "&emsp;"+str(i)+"."+str(j)+". "+line+"<br>\n"
            i += 1
            txt += "<b>"+str(i)+". settings.txt</b><br>\n"
            i += 1
            txt += "<b>"+str(i)+". help.html</b><br>\n"
            i += 1
            txt += "<b>"+str(i)+". favicon.ico</b>\n"
            txt += "</p><hr><h2>PART VII: ERRORS</h2><p>\n"
            od = collections.OrderedDict(sorted(ListOfErrors.items()))
            current_preffix = 0
            txt += "<b>ERROR #000-099</b> >System errors. Fix Application.py file<br>\n"
            for error_number, error_text in od.items():
                preffix = self.__evaluate_error_prefix(error_number)
                if preffix != current_preffix:
                    txt += "<br>\n"
                current_preffix = preffix
                txt += "<b>ERROR #"+str(error_number).zfill(3)+"</b> >"+preffix+error_text+"<br>\n"
            txt += "</div>\n"
            txt += "</body>\n"
            txt += "</html>\n"

            # TEST ISSUES
            if part < 6:
                if part == 0:
                    self.fatal_error("Missing comment: # GENERAL INFORMATION",3)
                elif part == 1:
                    self.fatal_error("Missing comment: # HOW TO USE",4)
                elif part == 2:
                    self.fatal_error("Missing comment: # MAIN MENU",5)
                elif part == 3:
                    self.fatal_error("Missing comment: # SCRIPT FUNCTIONS",6)
                elif part == 4:
                    self.fatal_error("Missing comment: # SETTINGS",7)
                elif part == 5:
                    self.fatal_error("Missing comment: # RELATED FILES",8)
            
            # save help file
            file = open("help.html", 'w')
            for line in txt:
                file.write(line)
            file.close()

    def help(self):
        if os.path.isfile("help.html"):
            os.popen("help.html")
        else:
            self.error("help.html", 200)
        self.restart()

    # CONSOLE
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

    # INPUT BAR
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
        ans = self.input(text+" (Y/N)") # get answer
        ans = ans.upper() # make sure its uppercase
        # take only the first letter
        if len(ans) > 0: 
            ans = ans[0]
        return ans == "Y"

    def pause(self):
        self.__input_button.wait_variable(self.__input_button_var)

    def __submit(self, event):
        self.__input_button_var.set(1)

    # PROGRESS BAR
    def progress_bar_value_set(self, percent):
        # set thg value of the progress bar
        self.__progress['value'] = percent
        self.__root.update_idletasks()
    
    def progress_bar_value_get(self):
        # returns thg value of the progress bar
        return self.__progress['value']
    
    # MAIN MENU
    def display_menu(self):
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
            self.main_menu["SETTINGS"] = self.__settings
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
            self.error(str(ans), 100)
            self.restart()

    # SETTINGS
    def get_setting(self, key):
        if key in self.__general_settings:
            return self.__general_settings[key]
        else:
            self.fatal_error("Missing setting vriable: "+key,300)

    def __load_settings(self):
        settings = "settings.txt"
        self.__general_settings = {}
        if os.path.isfile(settings):
            file = open(settings, 'r')
            lines = file.readlines()
            file.close()
            for line in lines:
                line = line.replace("\n","").strip()
                if " --> " in line:
                    line = line.split(" --> ")
                    self.__general_settings[line[0]] = line[1]
        else:
            self.fatal_error("Missing file: settings.txt",202)
    
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
            if self.question("Would you like to change the current settings? Y/N"):
                for key, value in self.__general_settings.items():
                    user_input = self.input(str(key)+" --> "+"[Leave empty to keep current value: "+str(value)+"]")
                    if user_input != "":
                        self.__general_settings[key] = user_input
        self.__write_settings()
        self.restart()

    # SCRIPT
    def script(self, file, functions):
        if os.path.isfile(file):
            f = open(file, 'r')
            lines = f.readlines()
            f.close()
            script = []
            for line in lines:
                originalline = line
                line = line.replace("\n", "").replace(")", "").strip()
                line = line.split("(")
                Function = line[0]
                if "," in line[1]:
                    line = line[1].split(",")
                    Args = line
                else:
                    if "()" in originalline:
                        Args = []
                    else:
                        Args = (line[1],)
                script.append((Function, Args))
            
            for x in script:
                key = x[0]
                value = x[1]
                if key in functions:
                    functions[key](value)
                else:
                    self.error(str(file)+" Invalid function name "+key, 301)
        else:
            self.error(file, 201)

    # DATABASE
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
            self.__dbbox.bind('<Double-Button>', self.__send_selected)
            if os.path.isfile(self.icon):
                self.__dbbox.iconbitmap(self.icon)
            else:
                self.fatal_error("Missing file favicon.ico",201)

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
    
    def __send_selected(self, event):
        text = self.__database_display_window.curselection()
        if text[0] > 0:
            self.cur.execute("SELECT name, type FROM pragma_table_info('"+self.__db_table+"')")
            fetched_values = self.cur.fetchall()
            headers_types = {}
            for line in fetched_values:
                if not line[0] in data:
                    headers_types[line[0]] = line[1]
            order_type = headers_types[self.__db_order_by]
            if order_type != "INT" and order_type != "FLOAT":
                self.cur.execute("SELECT * FROM "+self.__db_table+" ORDER BY '"+self.__db_order_by+"'")
            else:
                self.cur.execute("SELECT * FROM "+self.__db_table+" ORDER BY "+self.__db_order_by)
            fetched_values = self.cur.fetchall()
            data = fetched_values[text[self.__double_click_return_value]-1]
            self.__input.insert(END,data[self.__double_click_return_value])
    
    def set_database_double_click_return_value(self, index):
        self.__double_click_return_value = index

    def update_database(self):
        if self.__currently_displaying_database:
            # empty
            self.__database_display_window.delete(0, END)

            # get data
            data = []
            longest_column = {0:1} # column number: size
            self.con = sqlite3.connect(self.__database)
            self.cur = self.con.cursor()
            self.cur.execute("SELECT name, type FROM pragma_table_info('"+self.__db_table+"')")
            fetched_values = self.cur.fetchall()
            headers_types = {}
            for line in fetched_values:
                if not line[0] in data:
                    headers_types[line[0]] = line[1]
            order_type = headers_types[self.__db_order_by]
            if order_type != "INT" and order_type != "FLOAT":
                self.cur.execute("SELECT * FROM "+self.__db_table+" ORDER BY '"+self.__db_order_by+"'")
            else:
                self.cur.execute("SELECT * FROM "+self.__db_table+" ORDER BY "+self.__db_order_by)
            fetched_values = self.cur.fetchall()

            # get headers
            headers = [i[0] for i in self.cur.description]
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
                        if longest_column[i] < len(str(col)):
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
    
    def database_is_displayed(self):
        return self.__currently_displaying_database
    
    def form(self, fields):
        result = {}
        msg = "\nFORM RESULTS:\n"
        for key, value in fields.items():
            result[key] = value.default
            # get values
            if not value.disabled:
                # field types
                # text type
                # get input
                if value.type == TEXT:
                    # get input
                    result[key] = self.input("Insert "+value.name+" [Or leave empty for default value: "+value.default+"]") or value.default
                
                # number type
                if value.type == NUMBER:
                    # get input
                    result[key] = self.input("Insert "+value.name+" [Or leave empty for default value: "+str(value.default)+"]") or value.default
                    try:
                        if not "." in str(result[key]):
                            result[key] = int(result[key])
                        else:
                            result[key] = float(result[key])
                    except:
                        self.error(result[key], 101)
                        if not "." in str(value.default):
                            result[key] = int(value.default)
                        else:
                            result[key] = float(value.default)
                
                # date type
                if value.type == DATE:
                    # get input
                    result[key] = self.input("Insert "+value.name+" In format: YYY-MM-DD [Or leave empty for default value: "+value.default+"]") or value.default

                    # test date format
                    # YYYY-MM-DD
                    # 0123-45-67
                    result[key] = result[key].replace("-","")
                    result[key] = re.sub('[^0-9]','', result[key])
                    error = False

                    # check for errors
                    # string length
                    if len(result[key]) < 8:
                        self.error("Invalid date format "+result[key],102)
                        error = True

                    # year
                    if not error:
                        YYYY = int(result[key][0:4])
                        if not YYYY in range(0,10000):
                            self.error("Invalid year format: "+str(YYYY)+" acceptable range 0-9999",103)
                            error = True
                        YYYY = str(YYYY)
                        YYYY = YYYY.zfill(4)
                    
                    # month
                    if not error:
                        MM = int(result[key][4:6])
                        if not MM in range(1,13):
                            self.error("Invalid month format: "+str(MM)+" acceptable range 1-12",104)
                            error = True
                        MM = str(MM)
                        MM = MM.zfill(2)
                    
                    # date
                    if not error:
                        DD = int(result[key][6:8])
                        if not DD in range(1,32):
                            self.error("Invalid day format: "+str(DD)+" acceptable range 1-31",105)
                            error = True
                        DD = str(DD)
                        DD = DD.zfill(2)
                    
                    # result
                    if not error:
                        result[key] = YYYY+"-"+MM+"-"+DD
                    else:
                        result[key] = self.today()
                
                # file type
                if value.type == FILE:
                    # get input
                    self.print("Select "+value.name)
                    result[key] = self.load_file(value.default_directory, value.filetypes) or value.default
                    self.print("Selected: "+result[key])

                # files type
                if value.type == FILES:
                    # get input
                    self.print("Select "+value.name)
                    result[key] = self.load_files(value.default_directory, value.filetypes) or value.default
                    self.print("Selected: "+result[key])

                # dir type
                if value.type == DIRECTORY:
                    # get input
                    self.print("Select "+value.name)
                    result[key] = self.load_folder(value.default_directory) or value.default
                    self.print("Selected: "+result[key])
                
                # choose type
                if value.type == CHOOSE:
                    # get input
                    result[key] = self.choose("Choose "+value.name+" [Or leave empty for default value: "+value.default+"]", value.options, value.default)
            else:
                self.print(value.name+": "+str(value.default))
            
            msg += str(value.name)+": "+str(result[key])+"\n"
        
        # approve form submission
        msg += "Submit form?"
        if self.question(msg):
            return result
        else:
            return None
                

    # FILE MANAGMENT
    def save_file(self, content, initialdir, possibleTypes):
        # save a file
        defaultType = possibleTypes[0]
        file = fd.asksaveasfile(initialdir=initialdir, initialfile = 'Untitled', defaultextension=defaultType, filetypes=possibleTypes)
        if not file is None:
            self.print("Saved!")
            file.write(content)
            file.close()
        else:
            self.print("File not saved!")
    
    def load_file(self, initialdir, possibleTypes):
        # load a file
        file = fd.askopenfilename(initialdir=initialdir, filetypes=possibleTypes)
        return file

    def load_files(self, initialdir, possibleTypes):
        # load a directory
        files = fd.askopenfilenames(initialdir=initialdir, filetypes=possibleTypes)
        return files

    def load_folder(self, initialdir):
        # load a directory
        files = fd.askdirectory(initialdir=initialdir)
        return files

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
            self.fatal_error(file,204)

    # DATE AND TIME
    def today(self):
        # get today
        now = datetime.datetime.now()
        yyyy = str(now.year)
        mm = str(now.month).zfill(2)
        dd = str(now.day).zfill(2)
        return yyyy+"-"+mm+"-"+dd

class FIELD:
    def __init__(self, field_name, field_type, field_default_value):
        # given values
        self.name = field_name
        self.type = field_type
        self.default = field_default_value
        self.disabled = False

        # optional values
        self.filetypes = [("All Files","*.*")]
        self.default_directory = ""
        self.options = ("Y", "N")

TEXT = "TEXT"
NUMBER = "NUMBER"
DATE = "DATE"
FILE = "FILE"
FILES = "FILES"
DIRECTORY = "DIRECTORY"
CHOOSE = "CHOOSE"