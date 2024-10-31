from SmartConsole import SmartConsole
sc = SmartConsole("NA", "NA")

def GatherData(path):
    Data = []
    for filename in ("/netlist.csv", "/netnames.csv", "/testcables_to_outlets.csv", "/testcables_to_product.csv"):
        path_to_file = path+filename
        sc.test_path(path_to_file)
        data = sc.load_csv(path_to_file)
        Data.append(data)
    return Data