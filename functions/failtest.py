def TestData(data):
    netlist = data[0][1:]
    netnames = data[1][1:]
    testcables_to_outlets = data[2][1:]
    testcables_to_product = data[3][1:]

    # testcables_to_outlets
    used_test_cables = []
    used_outlets = []
    for line in testcables_to_outlets:
        test_cable = line[0]
        outlet = line[1]
        if not test_cable in used_test_cables:
            used_test_cables.append(test_cable)
        else:
            return [False, "In file testcables_to_outlets.csv\nTest cable: "+test_cable+" is not unique!"]
        if not outlet in used_outlets:
            used_outlets.append(outlet)
        else:
            return [False, "In file testcables_to_outlets.csv\nOutlet: "+outlet+" is not unique!"]
    
    # testcables_to_product.csv
    used_testcables_braids = []
    used_product_connectors = []
    for line in testcables_to_product:
        test_cable_braid = line[0]
        test_cable = test_cable_braid.split("_")
        test_cable = test_cable[0]+"_"+test_cable[1]
        product_connector = line[1]
        if not test_cable_braid in used_testcables_braids:
            used_testcables_braids.append(test_cable_braid)
        else:
            return [False, "In file testcables_to_product.csv\nTest cable: "+test_cable+" is not unique!"]
        if not product_connector in used_product_connectors:
            used_product_connectors.append(product_connector)
        else:
            return [False, "In file testcables_to_product.csv\nProduct connector: "+product_connector+" is not unique!"]
        if not test_cable in used_test_cables:
            return [False, "In file testcables_to_product.csv\nPlug: "+test_cable+" is not mapped in testcables_to_outlets!"]

    # netnames.csv
    used_netnumbers = []
    used_netnames = []
    for line in netnames:
        net_number = line[0]
        net_name = line[1]
        if not net_name in used_netnames:
            used_netnames.append(net_name)
        else:
            return [False, "In file netnames.csv\nNet name: "+net_name+" is not unique!"]
        if not net_number in used_netnumbers:
            used_netnumbers.append(net_number)
        else:
            return [False, "In file netnames.csv\nNet number: "+net_number+" is not unique!"]

    # netlist.csv
    used_points = []
    used_nets = []
    for line in netlist:
        product_connector = line[0]
        point = product_connector+"."+line[1]
        net = line[2]
        used_nets.append(net)
        if not net in used_netnumbers:
            return [False, "In file netlist.csv\nNet: "+net+" is not named in netnames.csv!"]
        if not point in used_points:
            used_points.append(point)
        else:
            return [False, "In file netlist.csv\nPoint: "+point+" is not unique!"]
        if not product_connector in used_product_connectors:
            return [False, "In file netlist.csv\nPlug: "+product_connector+" is not mapped in testcables_to_product.csv!"]
    
    # make sure that all net numbers are used
    for net_number in used_netnumbers:
        if not net_number in used_nets:
            return [False, "In file netnames.csv\nNet number: "+net_number+" is not used in netlist.csv!"]

    # return result
    return [True, ""]