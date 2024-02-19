from SmartConsole import SmartConsole
from functions.Outlets import GetOutletStart
sc = SmartConsole("NA", "NA")

# a csv file is built in the folowing format:
# PLUG, PIN, GLOBAL, NET, NET_LOC, NET_NAME, KELVIN
def GenerateCSVfile(Data, Braids_location):
    # unpack data
    netlist = Data[0]
    netnames = Data[1]
    testcables_to_outlets = Data[2]
    testcables_to_product = Data[3]
    
    # gather PinsNets
    PinsNets = {}
    for line in netlist[1:]:
        PinsNets[line[0]+"."+line[1]] = line[2]
    
    # gather net names
    NetNames = {}
    for line in netnames[1:]:
        NetNames[line[0]] = line[1]

    # gather BraidsPlugs
    BraidsPlugs = {}
    for line in testcables_to_product[1:]:
        BraidsPlugs[line[0]] = line[1]

    # gather maps
    maps = {}
    for braid_outlet in testcables_to_outlets[1:]:
        braid = braid_outlet[0]
        outlet = braid_outlet[1]
        path_to_braid = Braids_location+"/"+braid+".csv"
        sc.test_path(path_to_braid)
        maps[braid] = (outlet, sc.load_csv(path_to_braid))
    
    # generate csv data
    # PLUG, PIN, GLOBAL, NET, NET_LOC, NET_NAME, KELVIN
    csv_data = []
    EmptyNets = 1000
    nets = {}
    prev_pin = None
    for braid_outlet_map in maps.items():
        braid = braid_outlet_map[0]
        outlet = braid_outlet_map[1][0]
        map = braid_outlet_map[1][1]
        for line in map[1:]:
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
                    NET_LOC = nets[NET][0]
                    if prev_pin != PLUG+"."+PIN:
                        csv_data.append(str(PLUG)+","+str(PIN)+","+str(GLOBAL)+","+str(NET)+","+str(NET_LOC)+","+str(NET_NAME)+","+"1")
                    else:
                        csv_data.pop()
                        csv_data.append(str(PLUG)+","+str(PIN)+","+str(GLOBAL-1)+","+str(NET)+","+str(NET_LOC)+","+str(NET_NAME)+","+"2")
                    prev_pin = PLUG+"."+PIN
    for line in csv_data:
        print(line)