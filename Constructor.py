from SmartConsole import *
class Const:
    def __init__(self, programs, maps):
        self.sc = SmartConsole("N/A", "N/A")
        self.programs = programs
        self.maps = maps
        self.NetList = {} # {1:("Net1 Name",["P1.1", "P1.2", "P2.1", "P2.2"])}
        self.Plugs = {} # {"P1":"R1_178_2", "P2":"R1_005_1"}
    
    def read_data(self, part_number):
        # Read netlist.csv
        path = self.programs+"/"+part_number+"/netlist.csv"
        self.sc.test_path(path)
        netlist_CSV = self.sc.load_csv(path)

        # Read netnames.csv
        path = self.programs+"/"+part_number+"/netnames.csv"
        self.sc.test_path(path)
        netnames_CSV = self.sc.load_csv(path)

        # Read testcables_to_outlets.csv
        path = self.programs+"/"+part_number+"/testcables_to_outlets.csv"
        self.sc.test_path(path)
        testcables_to_outlets_CSV = self.sc.load_csv(path)

        # Read testcables_to_product.csv
        path = self.programs+"/"+part_number+"/testcables_to_product.csv"
        self.sc.test_path(path)
        testcables_to_product_CSV = self.sc.load_csv(path)

        # Read script.txt
        # Construct self.NetList
        for 
        # Construct self.Plugs
        pass

    def generate_program(self, Machine):
        if Machine == "runMPT5000L":
            # generate PARTNUMBER.csv
            # generate PARTNUMBER.txt
            pass
        else:
            # generate PARTNUMBER.mpt_product
            pass
        # generate PARTNUMBER.html