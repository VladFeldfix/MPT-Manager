from SmartConsole import *
import os

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
        self.product_part_number = part_number
        self.path = path

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
            OutletsToTestcables = {} # { Outlet: BraidMptSide }
            TestcablesToProduct = {} # { BraidProductSide: ProductPlug }
            Maps = {}                # { BraidMptSide: [ GlobalPoint, PinName, FourWire ] }
            FourWires = {}           # { BraidProductSide: 1 or 2 }

            MappedNetNumbers = [] # [ 1, 2, 3 ... ]
            UsedNetNames = []     # [ Net1_Power, Net2_Rtn ... ]
            NetLocations = {}     # { NetNumber: NetLocation }
            TestCableSizes = {}   # { BraidMptSide: 50, 100, 150 ... }

            csv_file = []   # [(ProductPlug, PinName, GlobalPoint, NetNumber, NetLocation, NetName, FourWire), ]
            EmptyNets = 999

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
            netlist = self.sc.load_csv(path+"/netlist.csv")                                # CONNAME    PINNAME   NETNUM
            netnames = self.sc.load_csv(path+"/netnames.csv")                              # NETNUM     NETNAME
            testcables_to_outlets = self.sc.load_csv(path+"/testcables_to_outlets.csv")    # TESTCABLE  OUTLET
            testcables_to_product = self.sc.load_csv(path+"/testcables_to_product.csv")    # TESTCABLE  PRODUCT

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
                BraidProductSide = row[0]
                ProductPlug = row[1]

                # test each values
                if BraidProductSide == "":
                    self.sc.fatal_error("in file: "+path+"/testcables_to_product.csv\nMissing test cable number")
                
                BraidMptSide = BraidProductSide.split(".")
                BraidMptSide = BraidMptSide[0]
                try:
                    BraidMptSide = int(BraidMptSide)
                except:
                    self.sc.fatal_error("in file: "+path+"/testcables_to_product.csv\nTest cable number: "+BraidProductSide+" is not a valid value")
                if not BraidMptSide in TestcablesToOutlets:
                    self.sc.fatal_error("in file: "+path+"/testcables_to_product.csv\nTest cable number: "+BraidMptSide+" is not mapped in testcables_to_outlets.csv")

                # add to dictionary
                if not BraidProductSide in TestcablesToProduct:
                    TestcablesToProduct[BraidProductSide] = ProductPlug
                else:
                    self.sc.fatal_error("in file: "+path+"/testcables_to_product.csv\nTest cable number: "+BraidProductSide+" is not unique")

            # LOAD MAPS
            for BraidMptSide, Outlet in TestcablesToOutlets.items(): # Maps = { BraidMptSide: [ GlobalPoint, BraidProductSide, PinName ] }
                MapPath = self.maps+"/"+str(BraidMptSide)+".csv"
                MapCsv = self.sc.load_csv(MapPath)
                for row in MapCsv[1:]:
                    # get values
                    GlobalPoint = row[0]
                    if row[1] != "":
                        BraidProductSide = str(BraidMptSide)+"."+row[1]
                        PinName = row[2]

                        # test each values
                        if GlobalPoint == "":
                            self.sc.fatal_error("in file: "+MapPath+"\nMissing global point")
                        try:
                            GlobalPoint = int(GlobalPoint)
                        except:
                            self.sc.fatal_error("in file: "+MapPath+"\nGlobal point: "+GlobalPoint+" is not a numerical value")
                        
                        if PinName == "":
                            self.sc.fatal_error("in file: "+MapPath+"\nMissing pin name")

                        # add to dictionary
                        if not BraidMptSide in Maps:
                            Maps[BraidMptSide] = [[GlobalPoint, BraidProductSide, PinName]]
                        else:
                            Maps[BraidMptSide].append([GlobalPoint, BraidProductSide, PinName])
                    
                    if not BraidMptSide in TestCableSizes:
                        TestCableSizes[BraidMptSide] = 1
                    else:
                        TestCableSizes[BraidMptSide] += 1
            
            for BraidMptSide, Qty in TestCableSizes.items():
                if Qty % 50 != 0:
                    self.sc.fatal_error("Map for test cable #"+str(BraidMptSide)+" has invalid number of global points. Must be 50, 100, 150... 1200")

            # fourwire detection
            for BraidMptSide, MapRows in Maps.items():
                for MapRow in MapRows:
                    PinName = MapRow[2]
                    BraidProductSide = MapRow[1]
                    if not BraidProductSide+"."+PinName in FourWires:
                        FourWires[BraidProductSide+"."+PinName] = 1
                    else:
                        if FourWires[BraidProductSide+"."+PinName] == 1:
                            FourWires[BraidProductSide+"."+PinName] = 2
                        else:
                            self.sc.fatal_error("in file: "+self.maps+"/"+str(BraidMptSide)+".csv\nPoint "+BraidProductSide+" appears more than twice!")

            # CREATE CSV FILE
            write = True
            self.sc.print("----------------------------------- CSV File --------------------------------------")
            for BraidMptSide, MapRows in Maps.items(): # # Maps = { BraidMptSide: [ GlobalPoint, BraidProductSide, PinName ] }
                for MapRow in MapRows:
                    GlobalPoint = MapRow[0]
                    BraidProductSide = MapRow[1]
                    if BraidProductSide in TestcablesToProduct:
                        ProductPlug = TestcablesToProduct[BraidProductSide]
                        PinName = MapRow[2]
                        GlobalPoint = MapRow[0] + Outlets[TestcablesToOutlets[BraidMptSide]]
                        if ProductPlug+"."+PinName in NetList:
                            NetNumber = NetList[ProductPlug+"."+PinName]
                            NetName = NetNames[NetNumber]
                        else:
                            EmptyNets += 1
                            NetNumber = EmptyNets
                            NetName = "NC_"+ProductPlug+"."+PinName
                    
                        FourWire = FourWires[BraidProductSide+"."+PinName]
                        if not NetNumber in NetLocations:
                            NetLocations[NetNumber] = 1
                        else:
                            if FourWire == 1:
                                NetLocations[NetNumber] += 1
                            else:
                                if write:
                                    NetLocations[NetNumber] += 1
                        NetLocation = NetLocations[NetNumber]

                        if FourWire == 1:
                            write = True
                        else:
                            write = not write
                            GlobalPoint -= 1
                        
                        if write:
                            csv_file.append((ProductPlug, PinName, GlobalPoint, NetNumber, NetLocation, NetName, FourWire))
                            self.sc.print(str(ProductPlug)+", "+str(PinName)+", "+str(GlobalPoint)+", "+str(NetNumber)+", "+str(NetLocation)+", "+str(NetName)+", "+str(FourWire))

            # RUN SCRIPT
            self.sc.print("\n----------------------------------- TXT File --------------------------------------")
            functions = {}
            functions["START"] = (self.start, ("PARTNUMBER", "PRODUCT_DESCRIPTION", "DRAWING_PN", "DRAWING_REV"))
            functions["TEST_CONTACT"] = (self.test_conductor, ())
            functions["TEST_INSULATION"] = (self.test_isolation, ())
            functions["TEST_HIPOT"] = (self.test_hipot, ())
            functions["TEST_BUTTON"] = (self.test_button, ("BTNNAME", "NCNO", "POINTS"))
            functions["TEST_SWITCH"] = (self.test_switch, ("SWNAME", "POSITION", "POINTS"))
            functions["TEST_ONOFF_SWITCH"] = (self.test_onoffswitch, ("SWNAME", "POINTS"))
            functions["TEST_LED"] = (self.test_led, ("LEDNAME", "NET1", "NET2", "COLOR"))
            functions["TEST_COAX"] = (self.test_coax_cable, ("COAXNAME", "SIGNAL", "BRAID"))
            functions["TEST_RESISTOR"] = (self.test_resistor, ("RESNAME", "OHM", "NET1", "NET2"))
            functions["TEST_CAPACITOR"] = (self.test_capacitor, ("CAPNAME", "MIN", "MAX", "NET1", "NET2", "DICHARGE"))
            functions["TEST_DIMMER"] = (self.test_dimmer, ("DIMNAME", "OHM", "POINT_A", "POINT_B"))
            functions["TEST_CNV"] = (self.test_cnv, ("CNV_NAME", "_24vMIN", "_24vMAX", "_5vMIN", "_5vMAX", "POINT_1", "POINT_2", "POINT_3", "POINT_4"))
            functions["END"] = (self.end, ())
            self.Script = []
            self.sc.run_script(path+"/script.txt", functions)

            # CREATE AN HTML FILE
            # create OutletsToTestcables
            outlets = ("A1","B1","C1","A2","B2","C2","A3","B3","C3","A4","B4","C4","A5","B5","C5","A6","B6","C6","A7","B7","C7","A8","B8","C8")
            letters = "ABCDEFGHIJKLMNOPQRSTUVWX"
            for BraidMptSide, Outlet in TestcablesToOutlets.items():
                try:
                    size = int(TestCableSizes[BraidMptSide]) / 50
                    size = int(size)
                except:
                    self.sc.fatal_error("in file: "+self.maps+"/"+str(BraidMptSide)+".csv\nInvalid number of global points")
                if not size in range(1,25):
                    self.sc.fatal_error("in file: "+self.maps+"/"+str(BraidMptSide)+".csv\nInvalid number of global points")
                else:
                    outlet_index = outlets.index(Outlet)
                    if size == 1:
                        if not Outlet in OutletsToTestcables:
                            OutletsToTestcables[Outlet] = BraidMptSide
                        else:
                            self.sc.fatal_error("Overlapping test cable plugs "+str(BraidMptSide)+" and "+OutletsToTestcables[Outlet])
                    else:
                        for i in range(size):
                            o = outlets[outlet_index + i]
                            t = str(BraidMptSide)+letters[i]
                            if not o in OutletsToTestcables:
                                OutletsToTestcables[o] = t
                            else:
                                self.sc.fatal_error("Overlapping test cable plugs "+t+" and "+OutletsToTestcables[o])

            # create htmlfile
            outlets = (("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"),("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"),("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"))
            htmlfile = open(path+"/"+part_number+".html", 'w')
            htmlfile.write("<html>\n")
            htmlfile.write("<head>\n")
            htmlfile.write("<link rel = 'stylesheet' type = 'text/css' href = '../__HTML__/style.css'</link>\n")
            htmlfile.write("</head>\n")
            htmlfile.write("<div id='content'>\n")
            htmlfile.write("<h1>"+part_number+"</h1>\n")
            htmlfile.write("<table>\n")
            
            for row in range(3):
                htmlfile.write("<tr>\n")
                for out in outlets[row]:
                    if out in OutletsToTestcables:
                        htmlfile.write("<td class='plug_name'>"+str(OutletsToTestcables[out])+"</td>\n")
                    else:
                        htmlfile.write("<td class='plug_name'>_</td>\n")
                htmlfile.write("</tr>\n")
                htmlfile.write('<tr>\n')
                for x in range(1,9):
                    htmlfile.write('<td class="outlet_name">'+letters[row]+str(x)+'</td>\n')
                htmlfile.write('</tr>\n')
            htmlfile.write("</table>\n")
            
            for BraidProductSide, ProductPlug in TestcablesToProduct.items(): #"10.2":"P5"
                htmlfile.write('<p>'+str(BraidProductSide)+' <img src="../__HTML__/plug.bmp"> '+str(ProductPlug)+'</p>\n')
            htmlfile.write("</div>\n")
            htmlfile.write("</body>\n")
            htmlfile.write("</html>\n")
            htmlfile.close()
        
        # SAVE CSV FILE
        self.sc.save_csv(path+"/"+part_number+".csv", csv_file)
        
        # restart
        self.sc.restart()

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
        self.write("Date: "+self.sc.today())
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
    
    def write(self, text):
        self.Script.append(text)
    
    def save_code(self):
        file = open(self.path+"/"+self.product_part_number+".txt", 'w')
        for line in self.Script:
            if "//" in line:
                self.sc.print("")
                file.write("\n")
            self.sc.print(line)
            file.write(line+"\n")
        file.close()

main()