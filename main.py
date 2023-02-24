import backend


def main():
    """runs the program and repeats unless user cancels the prompt"""
    flag = True
    while flag:
        orgs = backend.get_orgs()
        x = 1
        y = 1
        z = 1
        for i in orgs:
            print(f"{x}. {i['name']}")
            x = x + 1
        org_num = int(input("Select an organization by its number: "))
        org = orgs[org_num - 1]
        org_id = org['id']

        network = backend.get_networks(org_id)
        for i in network:
            print(f"{y}. {i['name']}")
            y = y + 1
        net_num = int(input("Select a network by its number: "))
        net = network[net_num - 1]
        net_id = net['id']

        mg_devices = backend.get_mg(net_id)
        for i in mg_devices:
            print(f"{z}. {i['model']}, serial: {i['serial']}")
            z = z + 1
        mg_num = int(input("Select an mg by its number to apply the config: "))
        mg = mg_devices[mg_num - 1]

        # serial of the MG is selected
        mg_serial = mg['serial']
        backend.apply_apn(mg_serial)

        repeat = input("Would you like to run the script again? Y to continue N to exit: ")
        if repeat.lower() == 'y':
            flag = True
        else:
            flag = False


if __name__ == '__main__':
    main()
