from SmartConsole import SmartConsole
from functions.outlets import GetOutletStart
sc = SmartConsole("NA", "NA")

# a csv file is built in the folowing format:
# PLUG, PIN, GLOBAL, NET, NET_LOC, NET_NAME, KELVIN
def CreateNetlist(data, path_to_test_cables):
    # unpack data
    netlist = data[0]
    netnames = data[1]
    testcables_to_outlets = data[2]
    testcables_to_product = data[3]
    
    # gather point_net
    point_net = {} # {P1.1 : 5}
    for line in netlist[1:]:
        if not line[0]+"."+line[1] in point_net:
            point_net[line[0]+"."+line[1]] = line[2]
        else:
            sc.fatal_error(line[0]+"."+line[1]+" is not unique!")
    
    # gather net names
    net_netname = {} # {1: netname}
    for line in netnames[1:]:
        if not line[0] in net_netname:
            net_netname[line[0]] = line[1]
        else:
            sc.fatal_error(line[0]+" is not unique!")

    # gather testcable_plug
    testcable_plugs = {} # {R1_157: P2}
    for line in testcables_to_product[1:]:
        if not line[0] in testcable_plugs:
            testcable_plugs[line[0]] = line[1]
        else:
            sc.fatal_error(line[0]+" is not unique!")

    # gather testcable_outletNmap
    testcable_outletNmap = {} # {R1_015: (A1, [[global_pin, test_cable_product_side, pin],])}
    for testcable_outlet in testcables_to_outlets[1:]:
        testcable = testcable_outlet[0]
        outlet = testcable_outlet[1]
        path_to_testcable = path_to_test_cables+"/"+testcable+".csv"
        sc.test_path(path_to_testcable)
        if not testcable in testcable_outletNmap:
            testcable_outletNmap[testcable] = (outlet, sc.load_csv(path_to_testcable))
        else:
            sc.fatal_error(testcable+" is not unique!")
    
    # generate csv data
    # PLUG, PIN, GLOBAL, NET, NET_LOC, NET_NAME, KELVIN
    csv_data = []
    empty_nets = 1000
    nets = {}
    prev_pin = None
    used_global_points = []
    for testcable_outlet_mapp in testcable_outletNmap.items():
        testcable = testcable_outlet_mapp[0]
        outlet = testcable_outlet_mapp[1][0]
        mapp = testcable_outlet_mapp[1][1]
        for line in mapp[1:]:
            global_point = line[0]
            #print(global_point)
            if len(line) > 1:
                testcable_plug = line[1]
                #print("testcable_plug: ",testcable_plug)
                #print("testcable_testcable_plug: ",testcable+"_"+testcable_plug)
                if testcable+"_"+testcable_plug in testcable_plugs:
                    PLUG = testcable_plugs[testcable+"_"+testcable_plug]
                    PIN = line[2]
                    GLOBAL = int(global_point) + int(GetOutletStart(outlet))
                    if PLUG+"."+PIN in point_net:
                        NET = point_net[PLUG+"."+PIN]
                        NET_NAME = net_netname[NET]
                    else:
                        NET = empty_nets
                        empty_nets += 1
                        NET_NAME = "NC_"+PLUG+"."+PIN
                    if not NET in nets:
                        nets[NET] = [1,NET_NAME]
                    else:
                        if prev_pin != PLUG+"."+PIN:
                            nets[NET][0] += 1
                    if NET in nets:
                        NET_LOC = nets[NET][0]
                    else:
                        sc.fatal_error("Unnamed net number: "+NET)
                    #print(str(PLUG)+","+str(PIN)+","+str(GLOBAL)+","+str(NET)+","+str(NET_LOC)+","+str(NET_NAME)+","+"1")
                    if not GLOBAL in used_global_points:
                        if prev_pin != PLUG+"."+PIN:
                            csv_data.append(str(PLUG)+","+str(PIN)+","+str(GLOBAL)+","+str(NET)+","+str(NET_LOC)+","+str(NET_NAME)+","+"1")
                            used_global_points.append(GLOBAL)
                        else:
                            csv_data.pop()
                            #NET_LOC -= 1
                            csv_data.append(str(PLUG)+","+str(PIN)+","+str(GLOBAL-1)+","+str(NET)+","+str(NET_LOC)+","+str(NET_NAME)+","+"2")
                            used_global_points.append(GLOBAL-1)
                        prev_pin = PLUG+"."+PIN
                    else:
                        sc.fatal_error("Overlapping global points: "+str(GLOBAL)+" fix file testcables_to_outlets.csv")
    
    return csv_data