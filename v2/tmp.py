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
TestcablesToProduct = {} # { BraidMptSide: ProductPlug }
Maps = {}                # { BraidMptSide: [ GlobalPoint, BraidProductSide, PinName, FourWire ] }
UsedNetNumbers = {}      # { NetNumber: 1, 2, 3 ... }
FourWires = {}           # { BraidProductSide: 1 or 2 }

MappedNetNumbers = [] # [ 1, 2, 3 ... ]
UsedNetNames = []     # [ Net1_Power, Net2_Rtn ... ]

csv_file = []   # [(ProductPlug, PinName, GlobalPoint, NetNumber, NetLocation, NetName, FourWire), ]