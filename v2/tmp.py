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