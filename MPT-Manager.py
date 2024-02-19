# Download SmartConsole.py from: https://github.com/VladFeldfix/Smart-Console/blob/main/SmartConsole.py
from SmartConsole import *
import os
import shutil
from Constructor import Const as Const

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

        # add external constructor
        self.constructor = Const(self.programs, self.maps)
        # display main menu
        self.sc.start()
    
    def runMPT5000L(self):
        Machine = "runMPT5000L"
        self.run(Machine)

    def runMPT5000(self):
        Machine = "runMPT5000"
        self.run(Machine)
    
    def run(self, Machine):
        # get part_number
        part_number = self.sc.input("Insert PART NUMBER [Without R-]").upper()
        path = self.programs+"/"+part_number
        self.product_part_number = part_number
        self.path = path

        # for new folder
        if not os.path.isdir(path):
            if self.sc.question("No such folder: "+path+"\nWould you like to create a new folder?"):
                os.makedirs(path)
                if not os.path.isfile(path+"/netlist.csv"):
                    file = open(path+"/netlist.csv", 'w')
                    file.write("CONNAME,PINNAME,NETNUM")
                    file.close()
                if not os.path.isfile(path+"/netnames.csv"):
                    file = open(path+"/netnames.csv", 'w')
                    file.write("NETNUM,NETNAME")
                    file.close()
                if not os.path.isfile(path+"/testcables_to_outlets.csv"):
                    file = open(path+"/testcables_to_outlets.csv", 'w')
                    file.write("TESTCABLE,OUTLET")
                    file.close()
                if not os.path.isfile(path+"/testcables_to_product.csv"):
                    file = open(path+"/testcables_to_product.csv", 'w')
                    file.write("TESTCABLE,PRODUCT,PARTNUMBER")
                    file.close()
                if not os.path.isfile(path+"/script.txt"):
                    file = open(path+"/script.txt", 'w')
                    file.write("START("+part_number+", Description , Drawing , Drawing_Rev )\n")
                    file.write("TEST_CONTACT()\n")
                    file.write("TEST_INSULATION()\n")
                    file.write("TEST_HIPOT()\n")
                    file.write("END()\n")
                    file.close()
                self.sc.print("Fill all the files and come back here to generate an MPT program")
                self.sc.open_folder(path)
                self.sc.restart()
                return
            else:
                self.sc.print("Mission aborted")
                self.sc.restart()
                return
        # if an exsiting folder
        else:
            self.constructor.read_data(part_number)
            self.constructor.generate_program(Machine)
            self.sc.restart()
            return

main()