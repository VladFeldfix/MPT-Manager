from SmartConsole import *
import os
import subprocess

class main:
    # constructor
    def __init__(self):
        # load smart console
        self.sc = SmartConsole("MPT Manager", "2.0")

        # set-up main memu
        self.sc.main_menu["RUN"] = self.run

        # get settings
        self.programs = self.sc.get_setting("Programs location")
        self.maps = self.sc.get_setting("Maps location")

        # test all paths
        self.sc.test_path(self.programs)
        self.sc.test_path(self.maps)

        # display main menu
        self.sc.start()
    
    def run(self):
        # get part_number
        part_number = self.sc.input("Insert PART NUMBER").upper()
        path = self.programs+"/"+part_number

        # for new folder
        if not os.path.isdir(path):
            if self.sc.question("No such folder: "+path+"\nWould you like to create a new folder?"):
                os.makedirs(path)
                file = open(path+"/netlist.csv", 'w')
                file.write("CONNAME,PINNAME,NETNUM")
                file.close()
                file = open(path+"/netnames.csv", 'w')
                file.write("NETNUM,NETNAME")
                file.close()
                file = open(path+"/testcables_to_outlets.csv", 'w')
                file.write("TESTCABLE,OUTLET")
                file.close()
                file = open(path+"/testcables_to_product.csv", 'w')
                file.write("TESTCABLE,PRODUCT")
                file.close()
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
            # load netlist
            file = open(path+"/netlist.csv", 'r')
            lines = file.readlines()
            file.close()

            # netnames
            file = open(path+"/netnames.csv", 'r')
            lines = file.readlines()
            file.close()

            # testcables_to_outlets
            file = open(path+"/testcables_to_outlets.csv", 'r')
            lines = file.readlines()
            file.close()

            # testcables_to_product
            file = open(path+"/testcables_to_product.csv", 'r')
            lines = file.readlines()
            file.close()

            # load maps


            # load script
            file = open(path+"/script.txt", 'r')
            lines = file.readlines()
            file.close()

        # restart
        self.sc.restart()

main()