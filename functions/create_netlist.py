from SmartConsole import SmartConsole
from functions.Outlets import GetOutletStart
sc = SmartConsole("NA", "NA")

# a csv file is built in the folowing format:
# PLUG, PIN, GLOBAL, NET, NET_LOC, NET_NAME, KELVIN
def CreateNetlist(Data, Braids_location):
    # unpack data
    netlist = Data[0]
    netnames = Data[1]
    testcables_to_outlets = Data[2]
    testcables_to_product = Data[3]
    
    # gather PinsNets
    PinsNets = {}
    for line in netlist[1:]:
        if not line[0]+"."+line[1] in PinsNets:
            PinsNets[line[0]+"."+line[1]] = line[2]
        else:
            sc.fatal_error(line[0]+"."+line[1]+" is not unique!")
    
    # gather net names
    NetNames = {}
    for line in netnames[1:]:
        if not line[0] in NetNames:
            NetNames[line[0]] = line[1]
        else:
            sc.fatal_error(line[0]+" is not unique!")

    # gather BraidsPlugs
    BraidsPlugs = {}
    for line in testcables_to_product[1:]:
        if not line[0] in BraidsPlugs:
            BraidsPlugs[line[0]] = line[1]
        else:
            sc.fatal_error(line[0]+" is not unique!")

    # gather mapps
    mapps = {}
    for braid_outlet in testcables_to_outlets[1:]:
        braid = braid_outlet[0]
        outlet = braid_outlet[1]
        path_to_braid = Braids_location+"/"+braid+".csv"
        sc.test_path(path_to_braid)
        if not braid in mapps:
            mapps[braid] = (outlet, sc.load_csv(path_to_braid))
        else:
            sc.fatal_error(braid+" is not unique!")
    
    # generate csv data
    # PLUG, PIN, GLOBAL, NET, NET_LOC, NET_NAME, KELVIN
    csv_data = []
    EmptyNets = 1000
    nets = {}
    prev_pin = None
    for braid_outlet_mapp in mapps.items():
        braid = braid_outlet_mapp[0]
        outlet = braid_outlet_mapp[1][0]
        mapp = braid_outlet_mapp[1][1]
        for line in mapp[1:]:
            global_point = line[0]
            if len(line) > 1:
                braid_plug = line[1]
                if braid+"."+braid_plug in BraidsPlugs:
                    PLUG = BraidsPlugs[braid+"."+braid_plug]
                    PIN = line[2]
                    GLOBAL = int(global_point) + int(GetOutletStart(outlet))
                    if PLUG+"."+PIN in PinsNets:
                        NET = PinsNets[PLUG+"."+PIN]
                        NET_NAME = NetNames[NET]
                    else:
                        NET = EmptyNets
                        EmptyNets += 1
                        NET_NAME = "NC_"+PLUG+"."+PIN
                    if not NET in nets:
                        nets[NET] = [1,NET_NAME]
                    else:
                        nets[NET][0] += 1
                    if NET in nets:
                        NET_LOC = nets[NET][0]
                    else:
                        sc.fatal_error("Unnamed net number: "+NET)
                    if prev_pin != PLUG+"."+PIN:
                        csv_data.append(str(PLUG)+","+str(PIN)+","+str(GLOBAL)+","+str(NET)+","+str(NET_LOC)+","+str(NET_NAME)+","+"1")
                    else:
                        csv_data.pop()
                        csv_data.append(str(PLUG)+","+str(PIN)+","+str(GLOBAL-1)+","+str(NET)+","+str(NET_LOC)+","+str(NET_NAME)+","+"2")
                    prev_pin = PLUG+"."+PIN
    
    return csv_data