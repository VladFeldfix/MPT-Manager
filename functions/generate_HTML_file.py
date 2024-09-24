from SmartConsole import SmartConsole

sc = SmartConsole("NA", "NA")

def GenerateHTMLfile(Path, Data, Part_Number, Maps, Size, machine):
    Result = ""
    ABC = "ABCDEFGHIJKLMNOPQRSTUVWX"
    OutletSize = Size[0] # 50
    OutletsPerCard = Size[1] # 3
    SwitchCards = Size[2] # 8
    OutletsToTestcables = {} # {A1: R1_045, A2: R1_046}
    TestCablesSize = {} # {R1_045: 50, R1_046: 150}
    TestCablesToProducts = {} # {R1_045_1: P2, R1_046_2: P1}

    # create OutletsToTestcables
    for line in Data[2][1:]:
        OutletsToTestcables[line[1]] = line[0]
    
    # create TestCablesSize
    for TestCable in OutletsToTestcables.values():
        Map = sc.load_csv(Maps+"/"+TestCable+".csv")
        TestCableSize = len(Map)-1
        if TestCableSize % OutletSize != 0:
            sc.fatal_error("Invalid number of global points in "+TestCable+"\nGiven: "+str(TestCableSize)+"\nShould be: "+str(OutletSize))
        else:
            TestCablesSize[TestCable] = TestCableSize
    
    # create TestCablesToProducts
    for line in Data[3][1:]:
        TestCablesToProducts[line[0]] = line[1]
    
    # generate outlets
    # outlets = ("A1","B1","C1","A2","B2","C2","A3","B3","C3","A4","B4","C4","A5","B5","C5","A6","B6","C6","A7","B7","C7","A8","B8","C8")
    outlets = []
    for switch in range(SwitchCards): # 3
        for outlet in range(OutletsPerCard): # 8
            outlets.append(ABC[outlet]+str(switch+1))
    
    # correct OutletsToTestcables considering to cable size
    newOutletsToTestcables = {}
    for Outlet, TestCable in OutletsToTestcables.items():
        if TestCablesSize[TestCable] > OutletSize:
            actual_size = TestCablesSize[TestCable] / OutletSize
            actual_size = int(actual_size)
            outlet_index = outlets.index(Outlet)
            for i in range(actual_size):
                additional_letter = ABC[i]
                newOutletsToTestcables[outlets[outlet_index+i]] = TestCable+additional_letter
        else:
            newOutletsToTestcables[Outlet] = TestCable
    OutletsToTestcables = newOutletsToTestcables
    
    # generate outlets
    # outlets = (("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"),("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"),("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"))
    outlets = []
    for outlet in range(OutletsPerCard): # 3
        new_line = []
        for switch in range(SwitchCards): # 8
            new_line.append(ABC[outlet]+str(switch+1))
        outlets.append(new_line)

    # generate HTML file
    if machine == "MPT5000L":
        csslocation = "../__HTML__"
    else:
        csslocation = ".css/"
    htmlfile = open(Path+"/"+Part_Number+".html", 'w')
    htmlfile.write("<html>\n")
    htmlfile.write("<head>\n")
    htmlfile.write("<link rel = 'stylesheet' type = 'text/css' href = '"+csslocation+"/style.css'></link>\n")
    htmlfile.write("</head>\n")
    htmlfile.write("<div id='content'>\n")
    htmlfile.write("<h1>"+Part_Number+"</h1>\n")
    htmlfile.write("<table>\n")
    for row in range(3):
        htmlfile.write("<tr>\n")
        for out in outlets[row]:
            if out in OutletsToTestcables:
                X = str(OutletsToTestcables[out])
                X = X.replace("R1_00","")
                X = X.replace("R1_0","")
                X = X.replace("R1_","")
                X = X.replace("R2_00","-")
                X = X.replace("R2_0","-")
                X = X.replace("R2_","-")
                htmlfile.write("<td class='plug_name'>"+str(X)+"</td>\n")
            else:
                htmlfile.write("<td class='plug_name'>_</td>\n")
        htmlfile.write("</tr>\n")
        htmlfile.write('<tr>\n')
        for x in range(SwitchCards):
            htmlfile.write('<td class="outlet_name">'+ABC[row]+str(x+1)+'</td>\n')
        htmlfile.write('</tr>\n')
    htmlfile.write("</table>\n")
    
    for BraidProductSide, ProductPlug in TestCablesToProducts.items(): #"10.2":"P5"
        BraidProductSide = str(BraidProductSide)
        BraidProductSide = BraidProductSide.replace("R1_00","")
        BraidProductSide = BraidProductSide.replace("R1_0","")
        BraidProductSide = BraidProductSide.replace("R1_","")
        BraidProductSide = BraidProductSide.replace("R2_00","-")
        BraidProductSide = BraidProductSide.replace("R2_0","-")
        BraidProductSide = BraidProductSide.replace("R2_","-")
        htmlfile.write('<p>'+BraidProductSide+' <img src="'+csslocation+'/plug.bmp"> '+str(ProductPlug)+'</p>\n')
    htmlfile.write("</div>\n")
    htmlfile.write("</body>\n")
    htmlfile.write("</html>\n")
    htmlfile.close()