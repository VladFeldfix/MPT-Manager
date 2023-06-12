import tkinter
from tkinter import *
import sys
import os

class SmartConsole:
    def __init__(self, program_name, rev):
        # GUI setup
        title = program_name+" v"+rev

        # main window
        self.__root = tkinter.Tk()
        self.__root.geometry("1000x600")
        self.__root.minsize(640,480)
        self.__root.title(title)
        self.__root.protocol("WM_DELETE_WINDOW", self.exit)
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)

        # console frmae
        frame = LabelFrame(self.__root, text=title+" [SmartConsole v1.0]")
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
        self.__console.tag_configure("FATAL_ERROR", foreground="#e82e2e", background="#f5d3d3")
        self.__console.tag_configure("INPUT", foreground="#2d362a", background="#619c46")
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

    # OUTPUT
    def print(self, text):
        # prints the given text to the console
        self.__send_text_to_console(text, "PRINT")
        self.__console.see(END)
        self.__root.update_idletasks()

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
        self.__send_text_to_console("Error #"+str(code).zfill(3)+preffix+text, "FATAL_ERROR")
        self.__console.see(END)
        self.__root.update_idletasks()
        self.pause()
        self.exit()

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

    # INPUT
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

    def __submit(self, event):
        self.__input_button_var.set(1)

    # CODE FLOW
    def abort(self):
        self.__send_text_to_console("Procedure aborted", "ABORT")
        self.__console.see(END)
        self.__root.update_idletasks()

    def restart(self):
        self.input("Press ENTER key to restart")
        self.progress_bar_value_set(0)
        self.display_menu()

    def pause(self):
        self.__input_button.wait_variable(self.__input_button_var)

    def exit(self):
        if self.__currently_displaying_database:
            self.__dbbox.destroy()
        self.__root.destroy()
        os._exit(1)
        sys.exit()

    # FILES

    # SETTINGS

    # GLOBAL FUNCTIONS
    def run(self):
        self.__root.mainloop()

    def exit(self):
        self.__root.destroy()
        os._exit(1)
        sys.exit()
    
    def pause(self):
        self.__input_button.wait_variable(self.__input_button_var)

    def __submit(self, event):
        self.__input_button_var.set(1)