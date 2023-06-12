from PersonalAssistant import *
import os

class main:
    def __init__(self):
        self.pa = PersonalAssistant("Test", "0.1")
        self.pa.main_menu["OPEN ONE FILE"] = self.open_one_file
        self.pa.main_menu["OPEN MANY FILES"] = self.open_many_files
        self.pa.main_menu["OPEN FOLDER"] = self.open_folder
        self.pa.main_menu["SAVE FILE"] = self.save_file
        self.pa.main_menu["SEE ALL FILES IN THE FOLDER"] = self.see_all_files_in_the_folder
        self.pa.main_menu["READ A SCRIPT"] = self.read_a_script
        self.pa.main_menu["GET DATE"] = self.get_date_stamp
        self.pa.main_menu["READ CSV FILE"] = self.read_csv_file
        self.pa.main_menu["GET A SETTINGS"] = self.get_a_setting
        self.pa.display_menu()
        self.pa.run()

    def open_one_file(self):
        initialdir = ""
        defaultType = ".txt"
        possibleTypes = [("All Files","*.*"), ("Text Documents","*.txt"), ("Python Document","*.py")]
        file = self.pa.load_file(initialdir, defaultType, possibleTypes)
        self.pa.print(file)
        os.popen(file)
        self.pa.restart()
    
    def open_many_files(self):
        initialdir = ""
        defaultType = ".txt"
        possibleTypes = [("All Files","*.*"), ("Text Documents","*.txt"), ("Python Document","*.py")]
        file = self.pa.load_files(initialdir, defaultType, possibleTypes)
        self.pa.print(file)
        self.pa.restart()

    def open_folder(self):
        initialdir = ""
        file = self.pa.load_folder(initialdir)
        self.pa.print(file)
        self.pa.restart()

    def save_file(self):
        initialdir = ""
        defaultType = ".txt"
        possibleTypes = [("All Files","*.*"), ("Text Documents","*.txt"), ("Python Document","*.py")]
        content = "Hello world!\nHow are you all doing today?"
        self.pa.save(content, initialdir, defaultType, possibleTypes)
        self.pa.restart()

    def see_all_files_in_the_folder(self):
        initialdir = ""
        folder = self.pa.load_folder("")
        # calculate work load
        workload = 0
        donesofar = 0
        for root, dirs, files in os.walk(folder):
            for file in files:
                workload += 1

        # load all files
        stop = False
        for root, dirs, files in os.walk(folder):
            for file in files:
                donesofar += 1
                self.pa.progress_bar_value_set((donesofar/workload)*100)
                self.pa.print(file)
                if donesofar % 100 == 0:
                    if self.pa.input("Continue? Y/N").upper()[0] != "Y":
                        stop = True
                        break
            if stop:
                break
        
        self.pa.restart()

    def read_a_script(self):
        self.pa.script("script.txt", {"F":self.f, "G":self.g})
        self.pa.restart()

    def get_date_stamp(self):
        self.pa.print(self.pa.today())
        self.pa.restart()

    def read_csv_file(self):
        initialdir = ""
        defaultType = ".csv"
        possibleTypes = [("Text Documents","*.csv",)]
        file = self.pa.read_csv(self.pa.load_file(initialdir, defaultType, possibleTypes))
        self.pa.print(file)
        self.pa.restart()
    
    def get_a_setting(self):
        self.pa.print(self.pa.get_setting("var1"))
        self.pa.restart()
    
    # script functions
    def f(self, arguments):
        a = int(arguments[0])
        b = int(arguments[1])
        self.pa.print("f(a,b) = "+str(a)+" + "+str(b)+" = "+str(a+b))
    
    def g(self, arguments):
        a = int(arguments[0])
        b = int(arguments[1])
        self.pa.print("g(a,b) = "+str(a)+" - "+str(b)+" = "+str(a-b))
main()