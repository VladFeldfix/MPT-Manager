from SmartConsole import SmartConsole
import os
sc = SmartConsole("NA", "NA")

def CreateNewProduct(path, part_number):
    os.makedirs(path)
    if not os.path.isfile(path+"/netlist.csv"):
        file = open(path+"/netlist.csv", 'w')
        file.write("CONNAME,PINNAME,NETNUM")
        file.close()
    if not os.path.isfile(path+"/netnames.csv"):
        file = open(path+"/netnames.csv", 'w')
        file.write("NETNUM,NETNAME")
        file.close()
    if not os.path.isfile(path+"/testcables_to_outlets.csv"):
        file = open(path+"/testcables_to_outlets.csv", 'w')
        file.write("TESTCABLE,OUTLET")
        file.close()
    if not os.path.isfile(path+"/testcables_to_product.csv"):
        file = open(path+"/testcables_to_product.csv", 'w')
        file.write("TESTCABLE,PRODUCT,PARTNUMBER")
        file.close()
    if not os.path.isfile(path+"/script.txt"):
        file = open(path+"/script.txt", 'w')
        file.write("START("+part_number+", PL , PR , Description , Drawing , Drawing_Rev , TRD, TRD_Rev )\n")
        file.write("TEST_CONTACT()\n")
        file.write("TEST_INSULATION()\n")
        file.write("TEST_HIPOT()\n")
        file.write("END()\n")
        file.close()
    sc.print("Fill all the files and come back here to generate an MPT program")
    #sc.open_folder(path)