import meraki
import os
from dotenv import load_dotenv
import json

# load all environment variables
load_dotenv()


def get_orgs():
    """Gets the list of all orgs (name and id) that admin has access to"""
    orgs = []
    dict = {"id": "", "name": ""}
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.getOrganizations()

    for i in response:
        dict["id"] = i["id"]
        dict["name"] = i["name"]
        orgs.append(dict)
        dict = {"id": "", "name": ""}

    return orgs


def get_networks(org_id):
    """Get a list of networks and returns dict with net IDs and names"""
    nets = []
    dict = {"id": "", "name": ""}
    # collect network names
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.getOrganizationNetworks(
        org_id, total_pages='all'
    )
    for i in response:
        dict["id"] = i["id"]
        dict["name"] = i["name"]
        nets.append(dict)
        dict = {"id": "", "name": ""}

    return nets


def get_mg(net_id):
    """Gets cellular gateway devices from a network and returns a dictionary with model and serial numbers of MG
    devices """
    dict = {"model": "", "serial": ""}
    mg = []
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.networks.getNetworkDevices(net_id)

    for i in response:
        if 'MG' in i['model']:
            dict["model"] = i["model"]
            dict["serial"] = i["serial"]
            mg.append(dict)
            dict = {"model": "", "serial": ""}

    # print(mg)
    return mg

def apply_apn(serial):
    """Loads 3 profiles and applies to an MG"""
    profile_1 = open('sim_profile_1.json')
    apn_profile_1 = json.load(profile_1)

    profile_2 = open('sim_profile_2.json')
    apn_profile_2 = json.load(profile_2)

    profile_3 = open('sim_profile_3.json')
    apn_profile_3 = json.load(profile_3)

    select_profile = input("Would you like to apply profile 1, 2 or 3? Enter the number: ")
    if select_profile == "1":
        select_profile = apn_profile_1
    elif select_profile == "2":
        select_profile = apn_profile_2
    elif select_profile == "3":
        select_profile = apn_profile_3

    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.devices.updateDeviceCellularSims(
        serial,
        sims=select_profile
    )
    print("Profile is updated")