# GENERAL INFORMATION

# HOW TO USE
## Download the application
## Set all the settings according to PART V
## Run App_Name.exe file

from PersonalAssistant import *
from PersonalAssistant import FIELD
import os

class main:
    def __init__(self):
        # set up Personal Assistant
        self.pa = PersonalAssistant(__file__, "MPT-Manager", "1.0")

        # load settings
        self.directory = self.pa.get_setting("MPT Programs")
        self.maps_location = self.pa.get_setting("Maps Location")
        settings_list = (self.directory, self.maps_location)

        # check all locations
        for path in settings_list:
            if (not os.path.isdir(path)) and (not os.path.isfile(path)):
                self.pa.fatal_error("Missing: "+path)

        # MAIN MENU
        self.pa.main_menu["CREATE A NEW MPT PROGRAM"] = self.run
        self.pa.display_menu()

        # run GUI
        self.pa.run()
    
    def run(self):
        error = False
        # get product part number
        product_part_number = self.pa.input("Insert PRODUCT PART NUMBER").upper()
        if product_part_number == "":
            self.pa.error("Invalid PRODUCT PART NUMBER")
            error = True
        
        # crtate folder
        cmd = self.directory+"/"+product_part_number
        if not os.path.isdir(cmd):
            if self.pa.question("Make new folder: "+cmd+" ?"):
                # create new folder
                os.makedirs(cmd)
            else:
                # new folder was not created
                error = True

        # create script file
        if not error:
            cmd = self.directory+"/"+product_part_number+"/script.txt"
            if not os.path.isfile(cmd):
                fields = {}
                fields["part"] = FIELD("PRODUCT PART NUMBER", TEXT, product_part_number)
                fields["part"].disabled = True
                fields["desc"] = FIELD("PRODUCT DESCRIPTION", TEXT, "No description")
                fields["drwg"] = FIELD("DRAWING PART NUMBER", TEXT, "No drawing")
                fields["drev"] = FIELD("DRAWING REV.", TEXT, "00")
                submit = self.pa.form(fields)
                if submit:
                    # read form info
                    product_part_number = submit["part"]
                    product_description = submit["desc"]
                    drawing = submit["drwg"]
                    drawing_rev = submit["drev"]

                    # create script file
                    file = open(cmd, 'w')
                    file.write("START("+product_part_number+","+product_description+","+drawing+","+drawing_rev+")\n")
                    file.write("TEST_CONTACT()\n")
                    file.write("TEST_INSULATION()\n")
                    file.write("TEST_HIPOT()\n")
                    file.write("END()")
                    file.close()
                    os.popen(cmd)
                    self.pa.input("Please fill the script file and press ENTER to continue")
                else:
                    error = True
        
        # create netlist.csv
        if not error:
            cmd = self.directory+"/"+product_part_number+"/netlist.csv"
            if not os.path.isfile(cmd):
                file = open(cmd, 'w')
                file.write("CONNAME,PINNAME,NETNUM")
                file.close()
                os.popen(cmd)
                self.pa.input("Please fill the netlist file and press ENTER to continue")

        # create netnames.csv
        if not error:
            cmd = self.directory+"/"+product_part_number+"/netnames.csv"
            if not os.path.isfile(cmd):
                file = open(cmd, 'w')
                file.write("NETNUM,NETNAME")
                file.close()
                os.popen(cmd)
                self.pa.input("Please fill the netnames file and press ENTER to continue")
        
        # create testcables_to_outlets.csv
        if not error:
            cmd = self.directory+"/"+product_part_number+"/testcables_to_outlets.csv"
            if not os.path.isfile(cmd):
                file = open(cmd, 'w')
                file.write("TESTCABLE,OUTLET")
                file.close()
                os.popen(cmd)
                self.pa.input("Please fill the testcables_to_outlets file and press ENTER to continue")
        
        # create testcables_to_product.csv
        if not error:
            cmd = self.directory+"/"+product_part_number+"/testcables_to_product.csv"
            if not os.path.isfile(cmd):
                file = open(cmd, 'w')
                file.write("TESTCABLE,PRODUCT")
                file.close()
                os.popen(cmd)
                self.pa.input("Please fill the testcables_to_product file and press ENTER to continue")
        
        # MAKE MPT PROGRAM
        if not error:
            self.pa.input("Make sure that all files are filled correctly and press ENTER to create the MPT program")

            # ----------------------------- creating a CSV file ----------------------------- 
            csv = []
            Outlets = {'A1':0,'B1':50,'C1':100,'A2':150,'B2':200,'C2':250,'A3':300,'B3':350,'C3':400,'A4':450,'B4':500,'C4':550,'A5':600,'B5':650,'C5':700,'A6':750,'B6':800,'C6':850,'A7':900,'B7':950,'C7':1000,'A8':1050,'B8':1100,'C8':1150}
            
            # load resources
            # load netlist tables
            netlist = self.pa.read_csv(self.directory+"/"+product_part_number+"/netlist.csv")
            netnames = self.pa.read_csv(self.directory+"/"+product_part_number+"/netnames.csv")
            testcables_to_outlets = self.pa.read_csv(self.directory+"/"+product_part_number+"/testcables_to_outlets.csv")
            testcables_to_product = self.pa.read_csv(self.directory+"/"+product_part_number+"/testcables_to_product.csv")

            # make them into dictionaries
            Netlist = {} # {"P5.10": "6"}
            for line in netlist[1:]:
                plug_name = line[0]
                pin = line[1]
                net_number = line[2]
                point = plug_name+"."+pin

                # make sure that the point is unique
                if not point in Netlist:
                    Netlist[point] = net_number
                else:
                    self.pa.fatal_error("Point: "+point+" is not unique")
            
            Netnumbers = {} # {"6": "RS434_P5V_RTN"}
            Netnames = {} # {"RS434_P5V_RTN": "6"}
            for line in netnames[1:]:
                net_number = line[0]
                net_name = line[1]
                
                # make sure that the net number is unique
                if not net_number in Netnumbers:
                    Netnumbers[net_number] = net_name
                else:
                    self.pa.fatal_error("Net number: "+net_number+" is not unique")
                
                # make sure that the net name is unique
                if not net_name in Netnames:
                    Netnames[net_name] = net_number
                else:
                    self.pa.fatal_error("Net name: "+net_name+" is not unique")
            
            Testcables_to_outlets = {} # {"10": "A1"}
            for line in testcables_to_outlets[1:]:
                test_cable = line[0]
                outlet = line[1]

                # make sure that the test_cable is unique
                if not test_cable in Testcables_to_outlets:
                    Testcables_to_outlets[test_cable] = outlet
                else:
                    self.pa.fatal_error("Test cable: "+test_cable+" is not unique")
                
                # make sure that the outlet is valid
                if not outlet in Outlets:
                    self.pa.fatal_error("Invalid outlet: "+outlet)
            
            Testcables_to_product = {} # {"10.2":"P5"}
            for line in testcables_to_product[1:]:
                braid = line[0]
                product = line[1]

                # make sure that the braid is unique
                if not braid in Testcables_to_product:
                    Testcables_to_product[braid] = product
                else:
                    self.pa.fatal_error("Test cable braid: "+braid+" is not unique")
                
                # make sure that the outlet is valid
                if not outlet in Outlets:
                    self.pa.fatal_error("Invalid outlet: "+outlet)
            
            # load all maps
            maps = {} # {"10": [[GLOBAL_POINT	BRAID_ID	PIN	BRIAD	PLUG_PART_NUMBER	FLEX_PLUG_PART_NUMBER	PIN_TYPE], ...]}
            for test_cable, outlet in Testcables_to_outlets.items():
                if not test_cable in maps:
                    maps[test_cable] = self.pa.read_csv(self.maps_location+"/"+test_cable+".csv")

            # make csv file from maps
            for test_cable, obj_map in maps.items():
                currentBraidPin = ""
                for row in obj_map:
                    # calculate variables
                    NetLocations = {} # {net number: net size}
                    # plug
                    if len(row) >= 3:
                        braidNumber = row[1]
                        testCable_braid = test_cable+"."+braidNumber # P5.10
                        if testCable_braid in Testcables_to_product:
                            plug = Testcables_to_product[testCable_braid] # P5

                            # pin
                            pin = row[2]

                            # globalPoint
                            globalPoint = int(row[0])
                            globalPoint += Outlets[Testcables_to_outlets[test_cable]]

                            # netNumber
                            netNumber = Netlist[testCable_braid]

                            # netLocation
                            if not netNumber in NetLocations:
                                NetLocations[netNumber] = 1
                            else:
                                if testCable_braid != currentBraidPin:
                                    NetLocations[netNumber] += 1
                            netLocation = str(NetLocations[netNumber])

                            # netName
                            netName = Netnumbers[netNumber]

                            # fourWire
                            if testCable_braid == currentBraidPin:
                                fourWire = "2"
                            else:
                                fourWire = "1"
                            currentBraidPin = testCable_braid
                            csv.append((plug, pin, globalPoint, netNumber, netLocation, netName, fourWire))
            
            # write result to csv file
            file = open(self.directory+"/"+product_part_number+"/"+product_part_number+".csv", 'w')
            for row in csv:
                text = row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5]+","+row[6]+"\n"
                self.pa.print(text)
                file.write(text)
            file.close()

            # ----------------------------- creating an TXT file ----------------------------- 


            # ----------------------------- creating an HTML file ----------------------------- 



        # if there was an error abbort mission
        if error:
            self.pa.error("Mission aborted")

        # restart
        self.pa.restart()

# SCRIPT FUNCTIONS
# SETTINGS
# RELATED FILES

main()