# Download SmartConsole.py from: https://github.com/VladFeldfix/Smart-Console/blob/main/SmartConsole.py
from SmartConsole import *
import os
from functions.create_new_product import CreateNewProduct
from functions.gather_data import GatherData
from functions.generate_CSV_file import GenerateCSVfile
from functions.generate_TXT_file import GenerateTXTfile
from functions.generate_MPTPRODUCT_file import GenerateMPTPRODUCTfile
from functions.generate_HTML_file import GenerateHTMLfile

class main:
    # constructor
    def __init__(self):
        # load smart console
        self.software_rev = "2.0"
        self.sc = SmartConsole("MPT Manager", self.software_rev)

        # set-up main memu
        self.sc.add_main_menu_item("RUN MPT-5000 L", self.runMPT5000L)
        self.sc.add_main_menu_item("RUN MPT-5000", self.runMPT5000)

        # get settings
        self.programs = self.sc.get_setting("Programs location")
        self.maps = self.sc.get_setting("Maps location")

        # test all paths
        self.sc.test_path(self.programs)
        self.sc.test_path(self.maps)

        # display main menu
        self.sc.start()
    
    def runMPT5000L(self):
        Machine = "MPT5000L"
        self.run(Machine)

    def runMPT5000(self):
        Machine = "MPT5000"
        self.run(Machine)
    
    def run(self, Machine):
        # get product name
        part_number = self.sc.input("Insert PART NUMBER [Without R-]").upper()
        path = self.programs+"/"+part_number
        
        # test if product exists. if not, create a new folder and add basic 5 files
        if not os.path.isdir(path):
            if self.sc.question("No such folder: "+path+"\nWould you like to create a new folder?"):
                CreateNewProduct(path, part_number)
            else:
                self.sc.print("Mission aborted")
                self.sc.restart()
                return
        # else, start generating program
        else:
            Data = GatherData(path) # gather data
            if Machine == "MPT5000L":
                GenerateCSVfile(Data, self.maps) # generate csv file
                GenerateTXTfile(Data) # generate txt file

            elif Machine == "MPT5000":
                GenerateMPTPRODUCTfile(Data) # generate mpt_product file
            GenerateHTMLfile(Data, Machine) # generate html file


main()