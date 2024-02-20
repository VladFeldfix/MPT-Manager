from SmartConsole import SmartConsole
import shutil
sc = SmartConsole("NA", "NA")

class TextGenerator:
    def __init__(self,path,software_rev,part_number,Machine):
        self.software_rev = software_rev
        self.code = ""
        self.path = path
        self.Machine = Machine

    def generate_code(self, load, arguments):
        file = open("functions/"+self.Machine+"_commands/"+load+".txt", 'r')
        lines = file.readlines()
        file.close()
        code = ""
        for line in lines:
            code += line
        if len(arguments) > 0:
            for key, val in arguments.items():
                code = code.replace(key, val)
        if len(self.code) > 0:
            n = "\n\n"
        else:
            n = ""
        self.code += n+code

    def start(self, arguments):
        functions = {}
        functions["PARTNUMBER"] = arguments[0]
        functions["PRODUCT_DESCRIPTION"] = arguments[1]
        functions["DRAWING_PN"] = arguments[2]
        functions["DRAWING_REV"] = arguments[3]
        functions["TODAY"] = sc.today()
        self.generate_code("START",functions)
    
    def test_conductor(self, arguments):
        self.generate_code("TEST_CONTACT",arguments)

    def test_isolation(self, arguments):
        self.generate_code("TEST_INSULATION",arguments)

    def test_hipot(self, arguments):
        self.generate_code("TEST_HIPOT",arguments)
    
    def test_button(self, arguments):
        function = {}
        functions["BTNNAME"] = arguments[0]
        functions["POINT1"] = arguments[1]
        functions["POINT2"] = arguments[2]
        self.generate_code("TEST_BUTTON",functions)
    
    def test_button_nc(self, arguments):
        function = {}
        functions["BTNNAME"] = arguments[0]
        functions["POINT1"] = arguments[1]
        functions["POINT2"] = arguments[2]
        self.generate_code("TEST_BUTTON_NC",functions)

    def test_switch(self, arguments):
        function = {}
        functions["SWNAME"] = arguments[0]
        functions["POSITION"] = arguments[1]
        functions["POINT1"] = arguments[2]
        functions["POINT2"] = arguments[3]
        self.generate_code("TEST_SWITCH",functions)

    def test_onoffswitch(self, arguments):
        function = {}
        functions["SWNAME"] = arguments[0]
        functions["POINT1"] = arguments[1]
        functions["POINT2"] = arguments[2]
        self.generate_code("TEST_ONOFF_SWITCH",functions)
    
    def test_led(self, arguments):
        function = {}
        functions["LEDNAME"] = arguments[0]
        functions["COLOR"] = arguments[1]
        functions["POINT1"] = arguments[2]
        functions["POINT2"] = arguments[3]
        self.generate_code("TEST_LED",functions)
    
    def test_coax_cable(self, arguments):
        function = {}
        functions["COAXNAME"] = arguments[0]
        functions["DATA1"] = arguments[1]
        functions["DATA2"] = arguments[2]
        functions["BRAID1"] = arguments[3]
        functions["BRAID2"] = arguments[4]
        self.generate_code("TEST_COAX",functions) 
    
    def test_resistor(self, arguments):
        function = {}
        functions["RESNAME"] = arguments[0]
        functions["OHM"] = arguments[1]
        functions["POINT1"] = arguments[2]
        functions["POINT2"] = arguments[3]
        self.generate_code("TEST_RESISTOR",functions)

    def test_capacitor(self, arguments):
        function = {}
        functions["CAPNAME"] = arguments[0]
        functions["MIN"] = arguments[1]
        functions["MAX"] = arguments[2]
        functions["POINT1"] = arguments[3]
        functions["POINT2"] = arguments[4]
        self.generate_code("TEST_CAPACITOR",functions)

    def test_dimmer(self, arguments):
        function = {}
        functions["DIMNAME"] = arguments[0]
        functions["MINOHM"] = arguments[1]
        functions["MAXOHM"] = arguments[2]
        functions["POINT1"] = arguments[3]
        functions["POINT2"] = arguments[4]
        functions["POINT3"] = arguments[5]
        self.generate_code("TEST_DIMMER",functions)
    
    def test_dc_to_dc(self, arguments):
        function = {}
        functions["CONVERTERNAME"] = arguments[0]
        functions["P24V"] = arguments[1]
        functions["P24V_RTN"] = arguments[2]
        functions["P5V"] = arguments[3]
        functions["P5V_RTN"] = arguments[4]
        self.generate_code("TEST_DCDC_CONVERTER",functions)
    
    def test_ssr(self, arguments):
        function = {}
        functions["SSRNAME"] = arguments[0]
        functions["OUTPUT1"] = arguments[1]
        functions["OUTPUT2"] = arguments[2]
        functions["INPUT3"] = arguments[3]
        functions["INPUT4"] = arguments[4]
        functions["PROBE1"] = arguments[5]
        functions["PROBE2"] = arguments[6]
        
        # create HTML
        file = open(self.path+"/"+arguments[0]+" Instructions.html", "w")
        file.write('<html>\n')
        file.write('    <head>\n')
        file.write('        <link rel="stylesheet" type="text/css" href="../__HTML__/style.css">\n')
        file.write('    </head>\n')
        file.write('    <body>\n')
        file.write('        <div id="content">\n')
        file.write('            <h1>'+arguments[0]+'</h1>\n')
        file.write('            <p>\n')
        file.write('                '+arguments[0]+'<br>\n')
        file.write('                <img src='+arguments[0]+' Instructions.jpeg>\n')
        file.write('            </p>\n')
        file.write('        </div>\n')
        file.write('    </body>\n')
        file.write('</html>\n')
        file.close()
        src = "img/SSR.png"
        dst = self.path+"/"+arguments[0]+" Instructions.jpeg"
        
        shutil.copyfile(src, dst)
        self.generate_code("TEST_SSR",functions)
    
    def test_diode(self, arguments):
        function = {}
        functions["DIODENAME"] = arguments[0]
        functions["POINT1"] = arguments[1]
        functions["POINT2"] = arguments[2]
        self.generate_code("TEST_DIODE",functions)

    def ptp(self, arguments):
        function = {}
        functions["PROBE"] = arguments[0]
        functions["POINT1"] = arguments[1]
        functions["POINT2"] = arguments[2]
        if arguments[3] == '1':
            sound = '1500'
        elif arguments[3] == '2':
            sound = '800'
        else:
            sc.fatal_error("In function POINT_TO_POINT argument SOUND must be 1 or 2")
        functions["SOUND"] = sound
        self.generate_code("POINT_TO_POINT",functions) 

    def end(self, arguments):
        functions = {}
        functions["SOFTWARE_REV"] = self.software_rev
        functions["TODAY"] = sc.today()
        self.generate_code("END", functions)

def CreateScript(path,software_rev,part_number,Machine):
    text_generator = TextGenerator(path,software_rev,part_number,Machine)
    functions = {}
    functions["START"] = (text_generator.start, ("PARTNUMBER", "PRODUCT_DESCRIPTION", "DRAWING_PN", "DRAWING_REV"))
    functions["TEST_CONTACT"] = (text_generator.test_conductor, ())
    functions["TEST_INSULATION"] = (text_generator.test_isolation, ())
    functions["TEST_HIPOT"] = (text_generator.test_hipot, ())
    functions["TEST_BUTTON"] = (text_generator.test_button, ("BTNNAME", "POINT1", "POINT2"))
    functions["TEST_BUTTON_NC"] = (text_generator.test_button_nc, ("BTNNAME", "POINT1", "POINT2"))
    functions["TEST_SWITCH"] = (text_generator.test_switch, ("SWNAME", "POSITION", "POINT1", "POINT2"))
    functions["TEST_ONOFF_SWITCH"] = (text_generator.test_onoffswitch, ("SWNAME", "POINT1", "POINT2"))
    functions["TEST_LED"] = (text_generator.test_led, ("LEDNAME", "COLOR", "POINT1", "POINT2"))
    functions["TEST_COAX"] = (text_generator.test_coax_cable, ("COAXNAME", "DATA1", "DATA2", "BRAID1", "BRAID2"))
    functions["TEST_RESISTOR"] = (text_generator.test_resistor, ("RESNAME", "OHM", "POINT1", "POINT2"))
    functions["TEST_CAPACITOR"] = (text_generator.test_capacitor, ("CAPNAME", "MIN", "MAX", "POINT1", "POINT2"))
    functions["TEST_DIMMER"] = (text_generator.test_dimmer, ("DIMNAME", "MINOHM", "MAXOHM", "POINT1", "POINT2", "POINT3"))
    functions["TEST_DCDC_CONVERTER"] = (text_generator.test_dc_to_dc, ("CONVERTERNAME", "P24V", "P24V_RTN", "P5V", "P5V_RTN"))
    functions["TEST_SSR"] = (text_generator.test_ssr, ("SSRNAME", "OUTPUT1", "OUTPUT2", "INPUT3", "INPUT4", "PROBE1", "PROBE2"))
    functions["TEST_DIODE"] = (text_generator.test_diode, ("DIODENAME", "POINT1", "POINT2"))
    functions["POINT_TO_POINT"] = (text_generator.ptp, ("PROBE", "POINT1", "POINT2", "SOUND"))
    functions["END"] = (text_generator.end, ())
    sc.run_script(path+"/script.txt", functions)
    return text_generator.code