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
            # SET VARIABLES
            Outlet = ""             # Outlet > A1, B1, C1 - C8
            GlobalPoint = ""        # GlobalPoint > 1-1250
            BraidMptSide = ""       # BraidMptSide > 1, 2, 3 ...
            BraidProductSide = ""   # BraidProductSide > 1.1, 1.2, 1.3 ...
            ProductPlug = ""        # ProductPlug > P1, J5 ....
            PinName= ""             # PinName > 1, 2, 3, a_, b_, c_, A, B, C, BODY ...
            NetNumber = ""          # NetNumber > 1, 2, 3 ...
            NetName = ""            # NetName > Net1_Power, Net2_Rtn ...
            NetLocation = ""        # NetLocation > 1, 2, 3 ...
            FourWire = ""           # FourWire > 1-2
            
            NetList = {}             # { ProductPlug.PinName: NetNumber ) }
            NetNames = {}            # { NetNumber: NetName }
            TestcablesToOutlets = {} # { BraidMptSide: Outlet }
            TestcablesToProduct = {} # { BraidMptSide: ProductPlug }

            MappedNetNumbers = [] # [1, 2, 3 ...]
            UsedNetNames = []     # [Net1_Power, Net2_Rtn ...]

            Outlets = {}
            Outlets["A1"] = 0
            Outlets["B1"] = 50
            Outlets["C1"] = 100
            Outlets["A2"] = 150
            Outlets["B2"] = 200
            Outlets["C2"] = 250
            Outlets["A3"] = 300
            Outlets["B3"] = 350
            Outlets["C3"] = 400
            Outlets["A4"] = 450
            Outlets["B4"] = 500
            Outlets["C4"] = 550
            Outlets["A5"] = 600
            Outlets["B5"] = 650
            Outlets["C5"] = 700
            Outlets["A6"] = 750
            Outlets["B6"] = 800
            Outlets["C6"] = 850
            Outlets["A7"] = 900
            Outlets["B7"] = 950
            Outlets["C7"] = 1000
            Outlets["A8"] = 1050
            Outlets["B8"] = 1100
            Outlets["C8"] = 1150

            # LOAD CSV FILES
            netlist = self.sc.load_csv(path+"/netlist.csv")                                     # CONNAME    PINNAME   NETNUM
            netnames = self.sc.load_csv(path+"/netnames.csv")                                   # NETNUM     NETNAME
            testcables_to_outlets = self.sc.load_csv(path+"/testcables_to_outlets.csv", 'r')    # TESTCABLE  OUTLET
            testcables_to_product = self.sc.load_csv(path+"/testcables_to_product.csv", 'r')    # TESTCABLE  PRODUCT

            # TEST LOADED CSV FILES
            # netlist
            for row in netlist[1:]:
                # get values
                ProductPlug = row[0]
                PinName = row[1]
                NetNumber = row[2]

                # test each values
                if ProductPlug == "":
                    self.sc.fatal_error("in file: "+path+"/netlist.csv\nMissing connector name")
                
                if PinName == "":
                    self.sc.fatal_error("in file: "+path+"/netlist.csv\nMissing pin name")
                
                if NetNumber == "":
                    self.sc.fatal_error("in file: "+path+"/netlist.csv\nMissing net number")
                try:
                    NetNumber = int(NetNumber)
                except:
                    self.sc.fatal_error("in file: "+path+"/netlist.csv\nNet number: "+NetNumber+" is not a numerical value")

                # add to dictionary
                if not ProductPlug+"."+PinName in NetList:
                    NetList[ProductPlug+"."+PinName] = NetNumber
                    MappedNetNumbers.append(NetNumber)
                else:
                    self.sc.fatal_error("in file: "+path+"/netlist.csv\nLocation: "+ProductPlug+"."+PinName+" is not unique")

            # netnames
            for row in netnames[1:]:
                # get values
                NetNumber = row[0]
                NetName = row[1]

                # test each values
                if NetNumber == "":
                    self.sc.fatal_error("in file: "+path+"/netnames.csv\nMissing net number")
                try:
                    NetNumber = int(NetNumber)
                except:
                    self.sc.fatal_error("in file: "+path+"/netnames.csv\nNet number: "+NetNumber+" is not a numerical value")
                if not NetNumber in MappedNetNumbers:
                    self.sc.fatal_error("in file: "+path+"/netnames.csv\nNet number: "+NetNumber+" is mapped in netlist.csv")
                
                if NetName == "":
                    self.sc.fatal_error("in file: "+path+"/netnames.csv\nMissing net name")
                if NetName in UsedNetNames:
                    self.sc.fatal_error("in file: "+path+"/netnames.csv\nNet name: "+NetName+" is not unique")
                else:
                    UsedNetNames.append(NetName)
                
                # add to dictionary
                if not NetNumber in NetNames:
                    NetNames[NetNumber] = NetName
                else:
                    self.sc.fatal_error("in file: "+path+"/netnames.csv\nNet number: "+NetNumber+" is not unique")

            # testcables_to_outlets
            for row in testcables_to_outlets[1:]:
                # get values
                BraidMptSide = row[0]
                Outlet = row[1]

                # test each values
                if BraidMptSide == "":
                    self.sc.fatal_error("in file: "+path+"/testcables_to_outlets.csv\nMissing test cable number")
                try:
                    BraidMptSide = int(BraidMptSide)
                except:
                    self.sc.fatal_error("in file: "+path+"/testcables_to_outlets.csv\nTest cable number: "+BraidMptSide+" is not a numerical value")
                
                if not Outlet in Outlets:
                    self.sc.fatal_error("in file: "+path+"/testcables_to_outlets.csv\nInvalid outlet number: "+Outlet)

                # add to dictionary
                if not BraidMptSide in TestcablesToOutlets:
                    TestcablesToOutlets[BraidMptSide] = Outlet
                else:
                    self.sc.fatal_error("in file: "+path+"/testcables_to_outlets.csv\nTest cable number: "+BraidMptSide+" is not unique")

            # testcables_to_product
            for row in testcables_to_product[1:]:
                # get values
                BraidMptSide = row[0]
                ProductPlug = row[1]

                # test each values
                if BraidMptSide == "":
                    self.sc.fatal_error("in file: "+path+"/testcables_to_product.csv\nMissing test cable number")
                try:
                    BraidMptSide = int(BraidMptSide)
                except:
                    self.sc.fatal_error("in file: "+path+"/testcables_to_product.csv\nTest cable number: "+BraidMptSide+" is not a numerical value")
                if not BraidMptSide in TestcablesToOutlets:
                    self.sc.fatal_error("in file: "+path+"/testcables_to_product.csv\nTest cable number: "+BraidMptSide+" is mapped in testcables_to_outlets.csv")

                # add to dictionary
                if not BraidMptSide in TestcablesToProduct:
                    TestcablesToProduct[BraidMptSide] = ProductPlug
                else:
                    self.sc.fatal_error("in file: "+path+"/testcables_to_product.csv\nTest cable number: "+BraidMptSide+" is not unique")
            """
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
        """
        # restart
        self.sc.restart()

main()