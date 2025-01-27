from SmartConsole import SmartConsole
import shutil
import os
sc = SmartConsole("NA", "NA")

class TextGenerator:
    def __init__(self,path,software_rev,part_number,Machine):
        self.software_rev = software_rev
        self.code = ""
        self.diode_list = ""
        self.program_ver = ""
        self.test_number = 0
        self.path = path
        self.Machine = Machine

    def generate_code(self, load, arguments):
        filename = "functions/"+self.Machine+"_commands/"+load+".txt"
        if not os.path.isfile(filename):
            filename = "functions/"+self.Machine+"_commands/"+load+".lua"
        sc.test_path(filename)
        file = open(filename, 'r')
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
        code = code.replace("#X", "#"+str(self.test_number))
        self.code += n+code
        self.test_number += 1

    def start(self, arguments):
        functions = {}
        functions["PARTNUMBER"] = arguments[0]
        functions["PLREV"] = arguments[1]
        functions["PR"] = arguments[2]
        functions["DESCRIPTION"] = arguments[3]
        functions["DRAWING_PN"] = arguments[4]
        functions["DRAWING_REV"] = arguments[5]
        given_date_format = sc.today()
        months = {"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr", "05":"May", "06":"Jun", "07":"Jul", "08":"Aug", "09":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}
        DAY = given_date_format[8:10]
        MONTH = months[given_date_format[5:7]]
        YEAR = given_date_format[0:4]
        functions["TODAY"] = DAY+" "+MONTH+" "+YEAR
        functions["ACCORDINGTOTRD"] = arguments[6]
        functions["TRDREV"] = arguments[7]
        self.generate_code("START",functions)
        self.program_ver = arguments[5]
    
    def test_conductor(self, arguments):
        self.generate_code("TEST_CONTACT",arguments)

    def test_isolation(self, arguments):
        self.generate_code("TEST_INSULATION",arguments)

    def test_hipot(self, arguments):
        self.generate_code("TEST_HIPOT",arguments)
    
    def test_button(self, arguments):
        functions = {}
        functions["BTNNAME"] = arguments[0]
        functions["POINT1"] = arguments[1]
        functions["POINT2"] = arguments[2]
        self.generate_code("TEST_BUTTON",functions)
    
    def test_button_nc(self, arguments):
        functions = {}
        functions["BTNNAME"] = arguments[0]
        functions["POINT1"] = arguments[1]
        functions["POINT2"] = arguments[2]
        self.generate_code("TEST_BUTTON_NC",functions)

    def test_switch(self, arguments):
        functions = {}
        functions["SWNAME"] = arguments[0]
        functions["POSITION"] = arguments[1]
        functions["POINT1"] = arguments[2]
        functions["POINT2"] = arguments[3]
        self.generate_code("TEST_SWITCH",functions)

    def test_onoffswitch(self, arguments):
        functions = {}
        functions["SWNAME"] = arguments[0]
        functions["POINT1"] = arguments[1]
        functions["POINT2"] = arguments[2]
        self.generate_code("TEST_ONOFF_SWITCH",functions)
    
    def test_led(self, arguments):
        functions = {}
        functions["LEDNAME"] = arguments[0]
        functions["COLOR"] = arguments[1]
        functions["POINT1"] = arguments[2]
        functions["POINT2"] = arguments[3]
        self.generate_code("TEST_LED",functions)
        self.diode_list += "{label='"+arguments[0]+"', device='hcs', setup={v = 2.2 V, i = 0.01 A}, criteria = { v < 2.1 V},  terminals = {test = {"+arguments[2]+"},  com = {"+arguments[3]+"}}}\n"
    
    def test_coax_cable(self, arguments):
        functions = {}
        functions["COAXNAME"] = arguments[0]
        functions["DATA1"] = arguments[1]
        functions["DATA2"] = arguments[2]
        functions["BRAID1"] = arguments[3]
        functions["BRAID2"] = arguments[4]
        self.generate_code("TEST_COAX",functions) 
    
    def test_resistor(self, arguments):
        functions = {}
        functions["RESNAME"] = arguments[0]
        functions["MINOHM"] = arguments[1]
        functions["MAXOHM"] = arguments[2]
        functions["POINT1"] = arguments[3]
        functions["POINT2"] = arguments[4]
        self.generate_code("TEST_RESISTOR",functions)

    def test_capacitor(self, arguments):
        functions = {}
        functions["CAPNAME"] = arguments[0]
        functions["MIN"] = arguments[1]
        functions["MAX"] = arguments[2]
        functions["POINT1"] = arguments[3]
        functions["POINT2"] = arguments[4]
        self.generate_code("TEST_CAPACITOR",functions)

    def test_dimmer(self, arguments):
        functions = {}
        functions["DIMNAME"] = arguments[0]
        functions["MINOHM"] = arguments[1]
        functions["MAXOHM"] = arguments[2]
        functions["POINT1"] = arguments[3]
        functions["POINT2"] = arguments[4]
        functions["POINT3"] = arguments[5]
        self.generate_code("TEST_DIMMER",functions)
    
    def test_dc_to_dc(self, arguments):
        functions = {}
        functions["CONVERTERNAME"] = arguments[0]
        functions["P24V"] = arguments[1]
        functions["P24V_RTN"] = arguments[2]
        functions["P5V"] = arguments[3]
        functions["P5V_RTN"] = arguments[4]
        self.generate_code("TEST_DCDC_CONVERTER",functions)
    
    def test_relay(self, arguments):
        functions = {}
        functions["RELAYNAME"] = arguments[0]
        functions["INPUT_PLUS"] = arguments[1]
        functions["INPUT_MINUS"] = arguments[2]
        functions["OUTPUT_PLUS"] = arguments[3]
        functions["OUTPUT_MINUS"] = arguments[4]
        self.generate_code("TEST_RELAY",functions)

    def test_diode(self, arguments):
        functions = {}
        functions["DIODENAME"] = arguments[0]
        functions["POINT1"] = arguments[1]
        functions["POINT2"] = arguments[2]
        self.generate_code("TEST_DIODE",functions)
        self.diode_list += "{label='"+arguments[0]+"', device='hcs', setup={v = 5 V, i = 0.01 A}, criteria = { v < 5.1 V},  terminals = {test = {"+arguments[1]+"},  com = {"+arguments[2]+"}}}\n"

    def ptp(self, arguments):
        functions = {}
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
    functions["START"] = (text_generator.start, ("PARTNUMBER", "PLREV", "PR", "DESCRIPTION", "DRAWING_PN", "DRAWING_REV", "ACCORDINGTOTRD", "TRDREV"))
    functions["TEST_CONTACT"] = (text_generator.test_conductor, ())
    functions["TEST_INSULATION"] = (text_generator.test_isolation, ())
    functions["TEST_HIPOT"] = (text_generator.test_hipot, ())
    functions["TEST_BUTTON"] = (text_generator.test_button, ("BTNNAME", "POINT1", "POINT2"))
    functions["TEST_BUTTON_NC"] = (text_generator.test_button_nc, ("BTNNAME", "POINT1", "POINT2"))
    functions["TEST_SWITCH"] = (text_generator.test_switch, ("SWNAME", "POSITION", "POINT1", "POINT2"))
    functions["TEST_ONOFF_SWITCH"] = (text_generator.test_onoffswitch, ("SWNAME", "POINT1", "POINT2"))
    functions["TEST_LED"] = (text_generator.test_led, ("LEDNAME", "COLOR", "POINT1", "POINT2"))
    functions["TEST_COAX"] = (text_generator.test_coax_cable, ("COAXNAME", "DATA1", "DATA2", "BRAID1", "BRAID2"))
    functions["TEST_RESISTOR"] = (text_generator.test_resistor, ("RESNAME", "MINOHM", "MAXOHM", "POINT1", "POINT2"))
    functions["TEST_CAPACITOR"] = (text_generator.test_capacitor, ("CAPNAME", "MIN", "MAX", "POINT1", "POINT2"))
    functions["TEST_DIMMER"] = (text_generator.test_dimmer, ("DIMNAME", "MINOHM", "MAXOHM", "POINT1", "POINT2", "POINT3"))
    functions["TEST_DCDC_CONVERTER"] = (text_generator.test_dc_to_dc, ("CONVERTERNAME", "P24V", "P24V_RTN", "P5V", "P5V_RTN"))
    functions["TEST_RELAY"] = (text_generator.test_relay, ("RELAYNAME", "INPUT_PLUS", "INPUT_MINUS", "OUTPUT_PLUS", "OUTPUT_MINUS"))
    functions["TEST_DIODE"] = (text_generator.test_diode, ("DIODENAME", "POINT1", "POINT2"))
    functions["POINT_TO_POINT"] = (text_generator.ptp, ("PROBE", "POINT1", "POINT2", "SOUND"))
    functions["END"] = (text_generator.end, ())
    sc.run_script(path+"/script.txt", functions)
    return (text_generator.code, text_generator.program_ver, text_generator.diode_list)