from functions.outlets import GetOutletStart

def GenerateMPTPRODUCTfile(data, path_to_product, product, script):
    # make netnames 
    netnames = {} # {1: Net1}
    for line in data[1][1:]:
        #print(line)
        netnames[line[0]] = line[1]

    # make nets dict
    nets = {} # {Net1: [P1.1, P1.2]}
    for line in data[0][1:]:
        #print(line)
        plug = line[0]
        pin = line[1]
        point = plug+"."+pin
        netnumber = line[2]
        netname = netnames[netnumber]
        if not netname in nets:
            nets[netname] = []
        nets[netname].append(point)

    # make mapping_data
    mapping_data = {} # {plug: (testcable, branch)}
    for line in data[3][1:]:
        #print(line)
        tmp = line[0]
        tmp = tmp.split("_")
        branch = tmp[-1]
        plug = line[1]
        testcable = tmp[0]+"_"+tmp[1]
        mapping_data[plug] = (testcable, branch)

    # outlets
    outlets = {} # {'R2_045': 'A1'}
    for line in data[2][1:]:
        testcable = line[0]
        outlet = line[1]
        outlets[testcable] = outlet

    # generate data
    filedata = ""

    # start
    filedata += "{\n"

    # add name
    filedata += "\tname = [[\n\t\t"+product+"\n\t]],\n\n"
    
    # add mapping table
    filedata += "\tmapping_table = [[\n"
    for plug, mapping in mapping_data.items():
        testcable = mapping[0]
        branch = testcable+"_"+mapping[1]
        outlet = outlets[testcable]
        first_global_point = GetOutletStart(outlet)
        filedata += "\t\t"+plug+" = {'"+testcable+"', "+str(first_global_point+1)+", '"+branch+"'}\n"
        #filedata += "\t\t"+plug+" = {'"+testcable+"', 1, '"+branch+"'}\n"
    filedata += "\t]],\n\n"
    
    # add netlist
    filedata += "\tnet_list = [[\n"
    for net_name, points in nets.items():
        filedata += "\t\t"+net_name+" = {"
        for point in points:
            filedata += point+", "
        filedata = filedata[:-2]
        filedata += "}\n"
    filedata += "\t]],\n\n"

    # add script
    filedata += "\tscripts = {\n"
    filedata += "\t\ttest_program = [[\n\n"
    filedata += script
    filedata += "\n\n\t\t]]\n"
    filedata += "\t}\n"
    
    # end
    filedata += "}\n"

    # save to file
    file = open(path_to_product+"/"+product+".mpt_product", 'w')
    file.write(filedata)
    file.close()