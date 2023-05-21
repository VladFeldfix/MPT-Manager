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
        self.product_part_number = product_part_number
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
                    self.pa.fatal_error("Invalid outlet: "+outlet, 2656313)
            
            Testcables_to_product = {} # {"10.2":"P5"}
            for line in testcables_to_product[1:]:
                braid = line[0]
                product = line[1]

                # make sure that the braid is unique
                if not braid in Testcables_to_product:
                    Testcables_to_product[braid] = product
                else:
                    self.pa.fatal_error("Test cable braid: "+braid+" is not unique")
            
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
            functions = {}
            functions["START"] = self.start
            functions["TEST_CONTACT"] = self.test_conductor
            functions["TEST_INSULATION"] = self.test_isolation
            functions["TEST_HIPOT"] = self.test_hipot
            functions["TEST_BUTTON"] = self.test_button
            functions["TEST_SWITCH"] = self.test_switch
            functions["TEST_ONOFF_SWITCH"] = self.test_onoffswitch
            functions["TEST_LED"] = self.test_led
            functions["TEST_COAX"] = self.test_coax_cable
            functions["TEST_RESISTOR"] = self.test_resistor
            functions["TEST_CAPACITOR"] = self.test_capacitor
            functions["TEST_DIMMER"] = self.test_dimmer
            functions["TEST_CNV"] = self.test_cnv
            functions["COMMENT"] = self.comment
            functions["END"] = self.end
            self.CODE = []
            self.pa.script(self.directory+"/"+product_part_number+"/script.txt", functions)

            # ----------------------------- creating an HTML file -----------------------------
            
            # calculate test cable sizes
            Testcables_sizes = {} # {"10": 50}
            for test_cable, obj_map in Maps.items():
                if not test_cable in Testcables_sizes:
                    if len(obj_map) % 50 != 0:
                        self.pa.fatal_error("Map for test cable #"+test_cable+" has invalid number of global points. Must be 50, 100, 150... 1200", 74745)
                    else:
                        Testcables_sizes[test_cable] = len(obj_map)
                else:
                    self.pa.fatal_error("Test cable "+test_cable+" is not unique", 999)

            # calculate Outlets_to_testcables # {"A1": "1"}
            Outlets_to_testcables = {}
            outlets = ("A1","B1","C1","A2","B2","C2","A3","B3","C3","A4","B4","C4","A5","B5","C5","A6","B6","C6","A7","B7","C7","A8","B8","C8")
            letters = "ABCDEFGHIJKLMNOPQRSTUVWX"
            for test_cable, outlet in Testcables_to_outlets.items():
                try:
                    size = int(Testcables_sizes[test_cable]) / 50
                    size = int(size)
                except:
                    self.pa.fatal_error("Test cable #"+test_cable+". Invalid number of global points", 453)
                if not size in range(1,25):
                    self.pa.fatal_error("Test cable #"+test_cable+". Invalid number of global points", 26564646456)
                else:
                    outlet_index = outlets.index(outlet)
                    if size == 1:
                        if not outlet in Outlets_to_testcables:
                            Outlets_to_testcables[outlet] = test_cable
                        else:
                            self.pa.fatal_error("Overlapping test cable plugs "+test_cable+" and "+Outlets_to_testcables[outlet], 37563)
                    else:
                        for i in range(size):
                            o = outlets[outlet_index + i]
                            t = test_cable+letters[i]
                            if not o in Outlets_to_testcables:
                                Outlets_to_testcables[o] = t
                            else:
                                self.pa.fatal_error("Overlapping test cable plugs "+t+" and "+Outlets_to_testcables[o], 234562736582634)
            htmlfile = open(self.directory+"/"+product_part_number+"/"+product_part_number+".html", 'w')
            letters = ('A', 'B', 'C')
            outlets = (("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"),("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"),("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"))
            htmlfile.write("<html>\n")
            htmlfile.write("<html>\n")
            htmlfile.write("<head>\n")
            htmlfile.write("<link rel = 'stylesheet' type = 'text/css' href = '../__HTML__/style.css'</link>\n")
            htmlfile.write("</head>\n")
            htmlfile.write("<body>\n")
            htmlfile.write("<div id='content'>\n")
            htmlfile.write("<h1>"+product_part_number+"</h1>\n")
            htmlfile.write("<table>\n")
            for row in range(3):
                htmlfile.write("<tr>\n")
                for out in outlets[row]:
                    if out in Outlets_to_testcables:
                        htmlfile.write("<td class='plug_name'>"+Outlets_to_testcables[out]+"</td>\n")
                    else:
                        htmlfile.write("<td class='plug_name'>_</td>\n")
                htmlfile.write("</tr>\n")
                htmlfile.write('<tr>\n')
                for x in range(1,9):
                    htmlfile.write('<td class="outlet_name">'+letters[row]+str(x)+'</td>\n')
                htmlfile.write('</tr>\n')
            htmlfile.write("</table>\n")
            for test_cable, product in Testcables_to_product.items(): #"10.2":"P5"
                htmlfile.write('<p>'+test_cable+' <img src="../__HTML__/plug.bmp"> '+product+'</p>\n')
            htmlfile.write("</div>\n")
            htmlfile.write("</body>\n")
            htmlfile.write("</html>\n")
            htmlfile.close()

        # if there was an error abbort mission
        if error:
            self.pa.abort()

        # restart
        self.pa.restart()

    # SCRIPT FUNCTIONS
    def start(self, arguments):
        # get variables
        PARTNUMBER = arguments[0]
        PRODUCT_DESCRIPTION = arguments[1]
        DRAWING_PN = arguments[2]
        DRAWING_REV = arguments[3]

        # generate code
        self.write("/************************************")
        self.write("")
        self.write("PCBA Part Number: "+PARTNUMBER)
        self.write("Written by: Evgeny Azov from: FLEX For RAFAEL R&D")
        self.write("POC on Rafael:FullSurname.FirstName'sFirstLetter.UnitNumber")
        self.write("Machine Type: MPT5000")
        self.write("Machine Software Version: 4.4.6.60")
        self.write("Date: "+self.pa.today())
        self.write("SW part Number: "+ PARTNUMBER)
        self.write("According to TRD No.: PS-39-756948 rev.: L")
        self.write("")
        self.write("************************************/")
        self.write('//GET HTML')
        self.write('LoadHTML("'+PARTNUMBER+'.html");')
        self.write('//INFO')
        self.write("PrintLn (4,time); Print(4,"   ");Print(4,date);")
        self.write('PrintLn (4," *****  Flex  *****  ");')
        self.write('PrintLn (4," Customer: RAFAEL    ");')
        self.write('PrintLn (4," Ass-y name: '+PRODUCT_DESCRIPTION+' ");')
        self.write('PrintLn (4," Ass-y PN: '+PARTNUMBER+' ");')
        self.write('PrintLn (4," Print PN: '+PARTNUMBER+' ");')
        self.write('PrintLn (4," Prog name: '+PARTNUMBER+' ");')
        self.write('PrintLn (4," Wire Diagram: '+DRAWING_PN+' REV.: '+DRAWING_REV+' ");')
        self.write('PrintLn (4," TRD: PS-39-756948 rev.: L");')
        self.write('//GET OPERATOR NAME AND SERIAL NUMBER')
        self.write('PrintLn (4,"");')
        self.write('Print(CON+DSK,"Operator Name: ");')
        self.write('Input("Enter Operator Name: ");')
        self.write('PrintLn(CON+DSK, TEXT);')
        self.write('PrintLn (4,"");')
        self.write('SetPrintLog(ON =ALL,CON);')
        self.write('Print(CON+DSK,"Serial Number: ");')
        self.write('Input("Enter Serial Number: ");')
        self.write('PrintLn(CON+DSK, TEXT);')
        self.write('PrintLn (4,"");')
        self.write('SetPrintLog(ON =ALL,CON);')
        self.write('//LOAD CALIBRATION FILE')
        self.write('AdapterCal("C:/MPT/Systems.cal");')

    def test_conductor(self, arguments):
        self.write('//TEST CONDUCTOR 2-wire')
        self.write('PrintLn (4,"TEST CONDUCTOR");')
        self.write('PrintLn (4," - 2 wire -");')
        self.write('SetConductor(HC, Pass < 1 Ohm, I = 1000 mA, V = 5 Volts);')
        self.write('Continuity(all);')

    def test_isolation(self, arguments):
        self.write('//TEST INSULATION')
        self.write('PrintLn (4,"TEST INSULATION");')
        self.write('SetInsulation(LV, Pass > 100 KOhms, I = Auto);')
        self.write('Insulation(all);')

    def test_hipot(self, arguments):
        self.write('//TEST HI-POT')
        self.write('If(PASSED){')
        self.write('\tPrompt("WARNING! Hi voltage test is about to start. Close the glass dome before continuation");')
        self.write('\tPrintLn (4,"TEST  HiPot DC");')
        self.write('\tSetHiPot(DC, V = 500 Volts, R >100 MOhm,Dwell = 1S, RampUpRate=1000);')
        self.write('\tHiPotDC(ALL);')
        self.write('}')

    def test_button(self, arguments):
        BTNNAME = arguments[0]
        NCNO = arguments[1]
        POINTS = arguments[2]
        POINTS = POINTS.replace("[","(").replace("]","),").replace("-",",")
        tmp = POINTS.replace("(","").replace(")","")
        tmp = tmp.split(",")
        POINT1 = tmp[0]
        POINT2 = tmp[1]

        self.write('//TEST BUTTON')
        self.write('PrintLn (4,"TEST BUTTON '+BTNNAME+'");')
        if NCNO == "NO":
            self.write('PrintLn (CON+DSK, "PRESS AND RELEASE BUTTON '+BTNNAME+'");')
            self.write('WaitForCont('+POINT1+','+POINT2+');')
            self.write('Continuity('+POINTS+');')
            self.write('WaitForNoCont('+POINT1+','+POINT2+');')
        elif NCNO == "NC":
            self.write('PrintLn (CON+DSK, "PRESS AND RELEASE BUTTON '+BTNNAME+'");')
            self.write('WaitForNoCont('+POINT1+','+POINT2+');')
            self.write('Insulation('+POINTS+');')
            self.write('WaitForNoCont('+POINT1+','+POINT2+');')
        elif NCNO == "SWITCH-NO":
            self.write('PrintLn (CON+DSK, "PRESS BUTTON '+BTNNAME+'");')
            self.write('WaitForCont('+POINT1+','+POINT2+');')
            self.write('Continuity('+POINTS+');')
            self.write('PrintLn (CON+DSK, "PRESS BUTTON '+BTNNAME+' AGAIN");')
            self.write('WaitForNoCont('+POINT1+','+POINT2+');')
        elif NCNO == "SWITCH-NC":
            self.write('PrintLn (CON+DSK, "PRESS BUTTON '+BTNNAME+'");')
            self.write('WaitForNoCont('+POINT1+','+POINT2+');')
            self.write('Insulation('+POINTS+');')
            self.write('PrintLn (CON+DSK, "PRESS BUTTON '+BTNNAME+' AGAIN");')
            self.write('WaitForNoCont('+POINT1+','+POINT2+');')

    def test_switch(self, arguments):
        SWNAME = arguments[0]
        POSITION = arguments[1]
        POINTS = arguments[2]
        POINTS = POINTS.replace("[","(").replace("]","),").replace("-",",")
        tmp = POINTS.replace("(","").replace(")","")
        tmp = tmp.split(",")
        POINT1 = tmp[0]
        POINT2 = tmp[1]
        self.write('//TEST SWITCH')
        self.write('PrintLn (4,"TEST SWITCH '+SWNAME+'");')
        self.write('PrintLn (CON+DSK, "SET SWITCH '+SWNAME+' TO POSITION '+POSITION+'");')
        self.write('WaitForCont('+POINT1+','+POINT2+');')
        self.write('Continuity('+POINTS+');')
    
    def test_onoffswitch(self, arguments):
        SWNAME = arguments[0]
        POINTS = arguments[1]
        POINTS = POINTS.replace("[","(").replace("]","),").replace("-",",")
        tmp = POINTS.replace("(","").replace(")","")
        tmp = tmp.split(",")
        POINT1 = tmp[0]
        POINT2 = tmp[1]
        self.write('//TEST SWITCH')
        self.write('PrintLn (4,"TEST SWITCH '+SWNAME+' ON");')
        self.write('PrintLn (CON+DSK, "SET SWITCH '+SWNAME+' TO POSITION ON");')
        self.write('WaitForCont('+POINT1+','+POINT2+');')
        self.write('Continuity('+POINTS+');')
        self.write('PrintLn (4,"TEST SWITCH '+SWNAME+' OFF");')
        self.write('PrintLn (CON+DSK, "SET SWITCH '+SWNAME+' TO POSITION OFF");')
        self.write('WaitForNoCont('+POINT1+','+POINT2+');')

    def test_led(self, arguments):
        LEDNAME = arguments[0]
        NET1 = arguments[1]
        NET2 = arguments[2]
        COLOR = arguments[3]

        self.write('//TEST LED')
        self.write('PrintLn (4,"TEST LED '+LEDNAME+'");')
        self.write('SetPS(V = 5 Volts, I = 0.01 Amps);')
        self.write('PowerOn(('+NET1+'),('+NET2+'));')
        self.write('Confirm("IS LED '+LEDNAME+' '+COLOR+'?");')
        self.write('PSV();')
        self.write('PSI();')
        self.write('PowerOff();')

    def test_coax_cable(self, arguments):
        COAXNAME = arguments[0]
        SIGNAL = arguments[1]
        BRAID = arguments[2]

        SIGNAL = SIGNAL.split("-")
        BRAID = BRAID.split("-")
        self.write('//TEST COAX CABLE')
        self.write('PrintLn (4,"TEST COAX CABLE '+COAXNAME+'");')
        self.write('Lua(')
        self.write('\t -- Test Signal')
        self.write('\tprinttodevices(DSK + CON, "\n")')
        self.write('\t ClrAllTest(false)')
        self.write('\t ClrAllCom(false)')
        self.write('\t SetTest(false,"'+SIGNAL[0]+'")')
        self.write('\t SetCom(false,"'+SIGNAL[1]+'")')
        self.write('\t printtodevices(DSK + CON, "Measure signal resistance")')
        self.write('\t DoContinuity()')
        self.write('\t signal_resistance = lastresmeasurement')
        self.write('\t -- Test braid')
        self.write('\t ClrAllTest(false)')
        self.write('\t ClrAllCom(false)')
        self.write('\t SetTest(false,"'+BRAID[0]+'")')
        self.write('\t SetCom(false,"'+BRAID[1]+'")')
        self.write('\t printtodevices(DSK + CON, "Measure braid resistance")')
        self.write('\t DoContinuity()')
        self.write('\t braid_resistance = lastresmeasurement')
        self.write('\t -- Compare')
        self.write('\t if signal_resistance > braid_resistance then')
        self.write('\t \t printtodevices(DSK + CON, signal_resistance, " > " ,braid_resistance)')
        self.write('\t \t printtodevices(DSK + CON, "PASS")')
        self.write('\t else')
        self.write('\t \t printtodevices(DSK + CON, "FAIL")')
        self.write('\t \t SetFailedFlag()')
        self.write('\t end')
        self.write('\tprinttodevices(DSK + CON, "\n\n")')
        self.write(')')

    def test_resistor(self, arguments):
        RESNAME = arguments[0]
        OHM = arguments[1]
        NET1 = arguments[2]
        NET2 = arguments[3]

        self.write('//TEST RESISTOR')
        self.write('PrintLn (4,"TEST '+RESNAME+' ('+OHM+'Ohm)");')
        self.write('PrintLn (4," - 2 wire -");')
        self.write('SetResistance(LV, Pass = '+OHM+' Ohms +- 2%, I = Auto);')
        self.write('Resistor ('+NET1+', '+NET2+');')
        
    def test_capacitor(self, arguments):
        CAPNAME = arguments[0]
        MIN = arguments[1]
        MAX = arguments[2]
        NET1 = arguments[3]
        NET2 = arguments[4]
        DICHARGE = arguments[5]

        if DICHARGE == "Y":
            self.write('//DISCHARGE CAPACITOR')
            self.write('ClrAllTestCom();')
            self.write('SetCom('+NET1+', '+NET2+');')
            self.write('Delay(500);')
            self.write('ClrAllTestCom();')

        self.write('//TEST CAPACITOR')
        self.write('PrintLn (4,"TEST CAPACITOR '+CAPNAME+'");')
        self.write('SetCAP(Pass = '+MIN+' pF, '+MAX+' pF);')
        self.write('Cap('+NET1+', '+NET2+');')

    def test_dimmer(self, arguments): # TEST_DIMMER POT1 106000 P3.11 P1.34
        DIMNAME = arguments[0]
        OHM = arguments[1]
        POINT_A = arguments[2]
        POINT_B = arguments[3]

        self.write('//TEST DIMMER')
        self.write('PrintLn (4,"TEST DIMMER '+DIMNAME+'");')
        self.write('PrintLn (4," - 2 wire -");')
        self.write('SetResistance(LV, Pass = '+OHM+' Ohms +- 2%, I = Auto);')
        self.write('Prompt("TURN DIMMER '+DIMNAME+' COUNTERCLOCKWISE ALL THE WAY TO THE END");')
        self.write('Resistor('+POINT_A+','+POINT_B+');')
    
    def test_cnv(self, arguments):
        CNV_NAME = arguments[0]
        _24vMIN = arguments[1]
        _24vMAX = arguments[2]
        _5vMIN = arguments[3]
        _5vMAX = arguments[4]
        POINT_1 = arguments[5]
        POINT_2 = arguments[6]
        POINT_3 = arguments[7]
        POINT_4 = arguments[8]

        self.write('//TEST CNV')
        self.write('PrintLn (4," ");')
        self.write('PrintLn (4,"TEST '+CNV_NAME+'");')
        self.write('SetResistance(5v, Pass = '+_24vMIN+', '+_24vMAX+', I = Auto);')
        self.write('Resistor ('+POINT_1+', '+POINT_2+'); //24v')
        self.write('SetResistance(5v, Pass = '+_5vMIN+', '+_5vMAX+', I = Auto);')
        self.write('Resistor ('+POINT_3+', '+POINT_4+');  //5v')

    def end(self, arguments):
        self.write('//TEST RESULT')
        self.write('PrintLn (4,"");')
        self.write('PrintLn (4,"TEST RESULT");')
        self.save_code()

    def comment(self,arguments):
        comment_text = arguments[0]
        self.write("//"+comment_text)
        """
        HEADER = arguments[0]
        lenOfline = 100-len(HEADER)
        halfALine = int(lenOfline/2)
        text = "//"+("#"*halfALine)+"  "+HEADER+"  "+("#"*halfALine)
        self.write(text)
        """
    
    def write(self, text):
        self.CODE.append(text)
    
    def save_code(self):
        product_part_number = self.product_part_number
        file = open(self.directory+"/"+product_part_number+"/"+product_part_number+".txt", 'w')
        for line in self.CODE:
            if "//" in line:
                self.pa.print("")
                file.write("\n")
            self.pa.print(line)
            file.write(line+"\n")
        file.close()
# SETTINGS
# RELATED FILES
# ERRORS
main()