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
                self.pa.fatal_error(path, 205)

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
            self.pa.error("Invalid PRODUCT PART NUMBER", 106)
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
                    self.pa.fatal_error("Point: "+point+" is not unique",302)
            
            Netnumbers = {} # {"6": "RS434_P5V_RTN"}
            Netnames = {} # {"RS434_P5V_RTN": "6"}
            for line in netnames[1:]:
                net_number = line[0]
                net_name = line[1]
                
                # make sure that the net number is unique
                if not net_number in Netnumbers:
                    Netnumbers[net_number] = net_name
                else:
                    self.pa.fatal_error("Net number: "+net_number+" is not unique",303)
                
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
            Maps = {} # {"10": [[GLOBAL_POINT	BRAID_ID	PIN	BRIAD	PLUG_PART_NUMBER	FLEX_PLUG_PART_NUMBER	PIN_TYPE], ...]}
            for test_cable, outlet in Testcables_to_outlets.items():
                if not test_cable in Maps:
                    Maps[test_cable] = self.pa.read_csv(self.maps_location+"/"+test_cable+".csv")[1:]

            # make csv file from maps
            emptyNets = 999
            netLocations = {}
            for test_cable, obj_map in Maps.items():
                i = 0
                doNext = True
                for row in obj_map:
                    # not every row is a valid row. so the first thing to do is to test if the row is valid
                    if len(row) >= 3:
                        # to build a line in the csv file each of the following variables must be calculated
                        # plugName, Pin, globalPoint, netNumber, netLocation, netName, fourWire

                        # plugName
                        # variable test_cable is a number. we must match the number of the test cable to the connector it is attached to
                        # to do that we must go to Testcables_to_product dictionary and find the plug name
                        # the plug name is the test_cable.braid_number
                        # if the plug is not in the dictionary it is irelevant and this line should be ignored
                        braid_number = row[1]
                        braidId = test_cable+"."+braid_number # 10.2
                        if braidId in Testcables_to_product:
                            # Pin
                            Pin = row[2]

                            # globalPoint
                            # the global point is calculated by getting the global point from the map + the outlet number
                            try:
                                globalPoint = int(row[0])
                            except:
                                self.pa.fatal_error("Invalid global point: "+str(globalPoint)+" in file: "+str(test_cable)+".csv")
                            if test_cable in Testcables_to_outlets:
                                if Testcables_to_outlets[test_cable] in Outlets:
                                    globalPoint += Outlets[Testcables_to_outlets[test_cable]]
                                else:
                                    self.pa.fatal_error("Invalid outlet: "+Testcables_to_outlets[test_cable])
                            else:
                                self.pa.fatal_error("Unmapped plug: "+test_cable)

                            # netNumber
                            # the net number can be either a number from 1-999 for used nets or 1000+ for empty nets
                            plugName = Testcables_to_product[braidId]
                            if plugName+"."+Pin in Netlist:
                                try:
                                    netNumber = int(Netlist[plugName+"."+Pin]) # P5.10 = "6"
                                except:
                                    self.pa.fatal_error("Invalid net number "+str(netNumber))
                            else:
                                emptyNets += 1
                                netNumber = emptyNets

                            # netLocation and fourWire
                            # the net location is the last location + 1 if the cable is not fourwire
                            # the first step is to identify the pin as two or fourwire
                            # to do that test the next elemt and the previous element
                            fourWire = "1"

                            # test next element
                            if i != len(obj_map)-1:
                                curr_element = row[1]+"."+row[2]
                                next_element = obj_map[i+1][1]+"."+obj_map[i+1][2]
                                if curr_element == next_element:
                                    fourWire = "2"

                            # test prev row
                            if i > 0:
                                curr_element = row[1]+"."+row[2]
                                prev_element = obj_map[i-1][1]+"."+obj_map[i-1][2]
                                if curr_element == prev_element:
                                    fourWire = "2"
                                
                            if not netNumber in netLocations:
                                netLocations[netNumber] = 1
                            else:
                                if doNext:
                                    netLocations[netNumber] += 1
                            netLocation = netLocations[netNumber]
                            lastBraidId = braidId

                            # netName
                            # get the net name from Netnumbers
                            if netNumber < 1000:
                                if str(netNumber) in Netnumbers:
                                    netName = Netnumbers[str(netNumber)]
                                else:
                                    self.pa.fatal_error("Unnamed net number: "+str(netNumber))
                            else:
                                netName = "NC_"+plugName+"."+Pin
                            
                            # write to csv if it is not the second wire of a fourWire
                            if fourWire == "2":
                                doNext = not doNext
                            if doNext:
                                csv.append((plugName, Pin, globalPoint, netNumber, netLocation, netName, fourWire))
                    i += 1
            # write result to csv file
            file = open(self.directory+"/"+product_part_number+"/"+product_part_number+".csv", 'w')
            for row in csv:
                text = str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+","+str(row[6])+"\n"
                self.pa.print(text.replace("\n", ''))
                file.write(text)
            file.close()

            # ----------------------------- creating an TXT file ----------------------------- 


            # ----------------------------- creating an HTML file ----------------------------- 



        # if there was an error abbort mission
        if error:
            self.pa.abort()

        # restart
        self.pa.restart()

# SCRIPT FUNCTIONS
# SETTINGS
# RELATED FILES
# ERRORS
main()