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
            # load files
            netlist = self.sc.load_csv(path+"/netlist.csv")
            netnames = self.sc.load_csv(path+"/netnames.csv")
            testcables_to_outlets = self.sc.load_csv(path+"/testcables_to_outlets.csv", 'r')
            testcables_to_product = self.sc.load_csv(path+"/testcables_to_product.csv", 'r')

            # test loaded files for errors
            # netlist
            Netlist = {} # {ConnectorName.PinName: NetNumber} e.g. {P1.25: 17}
            for row in netlist[1:]:
                ConnectorName = row[0]
                PinName = row[1]
                NetNumber = row[2]
                ConnectorNameAndPin = ConnectorName+"."+PinName
                if ConnectorName == "":
                    self.sc.fatal_error("in file: "+path+"/netlist.csv\nMissing connector name")
                    return
                if PinName == "":
                    self.sc.fatal_error("in file: "+path+"/netlist.csv\nMissing pin name")
                    return
                if NetNumber == "":
                    self.sc.fatal_error("in file: "+path+"/netlist.csv\nMissing net number")
                    return
                try:
                    NetNumber = int(NetNumber)
                except:
                    self.sc.fatal_error("in file: "+path+"/netlist.csv\nNet number: "+NetNumber+" is a numerical value")
                    return
                if not ConnectorNameAndPin in Netlist:
                    Netlist[ConnectorNameAndPin] = NetNumber
                else:
                    self.sc.fatal_error("in file: "+path+"/netlist.csv\nLocation: "+ConnectorNameAndPin+" is not unique")
                    return
            
            # netnames
            NetNames = {} # {1: NET1_POWER}
            used_names = []
            for row in netnames[1:]:
                NetNumber = row[0]
                NetName = row[1]
                if not NetNumber in NetNames:
                    NetNames[NetNumber] = NetName
                else:
                    self.sc.fatal_error("in file: "+path+"/netnames.csv\nNet number: "+NetNumber+" is not unique")
                    return
                if not NetName in used_names:
                    used_names.append(NetName)
                else:
                    self.sc.fatal_error("in file: "+path+"/netnames.csv\nNet name: "+NetName+" is not unique")
                    return

            # testcables_to_outlets
            TestcablesToOutlets = {} # {57A: A1}
            for row in testcables_to_outlets[1:]:
                TestCable = row[0]
                Outlet = row[1]
                if not TestCable in TestcablesToOutlets:
                    TestcablesToOutlets[TestCable] = Outlet
                else:
                    self.sc.fatal_error("in file: "+path+"/testcables_to_outlets.csv\nTest cable: "+TestCable+" is not unique")
                    return
                if not Outlet in Outlets:
                    self.sc.fatal_error("in file: "+path+"/testcables_to_outlets.csv\nIvalid outlet: "+Outlet)
                    return

            # testcables_to_product
            TestcablesToProduct = {} # {57.1: P2}
            for row in testcables_to_product[1:]:
                TestCable = row[0]
                ConnectorName = row[1]
                if not TestCable in TestcablesToProduct:
                    TestcablesToProduct[TestCable] = ConnectorName
                    

            # load maps
            maps = {}

            # create csv file
            csv_file = []
            for GlobalPoint, data in maps.items():
                # maps -> { GlobalPoint: (TestCable 57, PinName 10, FourWire 1) }
                # ConnectorName
                ConnectorName = ""

                # PinName
                PinName = ""

                # GlobalPoint
                GlobalPoint = ""

                # NetNumber
                NetNumber = ""

                # NetLocation
                NetLocation = ""

                # NetName
                NetName = ""

                # FourWire
                FourWire = ""
                
                # add new line
                csv_file.append((ConnectorName, PinName, GlobalPoint, NetNumber, NetLocation, NetName, FourWire))
            
            # save scv file
            self.sc.save_csv(path+"/"+part_number+".csv", csv_file)

            # run script
            self.sc.run_script(path+"/script.txt", functions)

        # restart
        self.sc.restart()

main()