# Download SmartConsole.py from: https://github.com/VladFeldfix/Smart-Console/blob/main/SmartConsole.py
from SmartConsole import *
import os
from functions.create_new_product import CreateNewProduct
from functions.gather_data import GatherData
from functions.create_netlist import CreateNetlist
from functions.create_script import CreateScript
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
            Netlist = CreateNetlist(Data, self.maps) # generate csv file
            Script = CreateScript(path, self.software_rev, part_number, Machine)
            
            # for each machine something else
            if Machine == "MPT5000L":
                # create CSV file
                path_to_csv_file = path+"/"+part_number+".csv"
                csv_file = open(path_to_csv_file, 'w')
                for line in Netlist:
                    csv_file.write(line+"\n")
                csv_file.close()

                # create TXT file
                path_to_txt_file = path+"/"+part_number+".txt"
                file = open(path_to_txt_file, 'w')
                file.write(Script)
                file.close()

                # for html
                Size = (50, 3, 8)

            elif Machine == "MPT5000":
                 # generate mpt_product file
                self.sc.print("Generating MPT_PRODUCT file...")
                GenerateMPTPRODUCTfile(Data, Script)

                # for html
                Size = (50, 3, 10)
            
            self.sc.print("Generating HTML file for machine: "+Machine+"...")
            GenerateHTMLfile(path, Data, part_number, self.maps, Size) # generate html file
        # done
        self.sc.restart()
main()