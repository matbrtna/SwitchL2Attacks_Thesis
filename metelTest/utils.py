# import pandas as pd
import json
import sys
import netifaces
import fTester
import os

# def readCSV(name):
#     df = pd.read_csv(name, sep=";")
#     return df

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH       = os.path.join(APP_ROOT, "config.json")
CAPTURES_DIR      = os.path.join(APP_ROOT, "captures")
TEST_CONFIGS_DIR  = os.path.join(APP_ROOT, "test_configs")
TEST_RESULTS_DIR  = os.path.join(APP_ROOT, "test_results")

def findColumnValues(file,name):
    values = file[name].dropna()
    return values

def findColumn(csv, name,value):
    result = csv[csv[name] ==value]
    return result


def readJSON(name):
    with open(name, "r") as file:
        data = json.load(file)
    return data


def findJSONColumn(file,columnName):
    values=[]
    for entry in file.get("client_data", []):
        if "loss" in entry:
            loss_value = entry[columnName]
            values.append(loss_value)
    if len(values)>0:
        # print(values)
        return values
    else:
        print("Values column was not found in test result, check if right test was started")
        sys.exit(1)



def get_ip_address(interface):
    try:
        addresses = netifaces.ifaddresses(interface)
        ip_info = addresses.get(netifaces.AF_INET)
        if ip_info:
            return ip_info[0]['addr']
        else:
            return None
    except ValueError:
        print("Non existing interface selected")
        sys.exit(1)
        return None


def getInterface():
    config = readJSON(CONFIG_PATH)
    return config["interface"]

def getTesterIp():
    config = readJSON(CONFIG_PATH)
    return config["tester_ip"]

def getSwitchIp():
    config = readJSON(CONFIG_PATH)
    return config["switch_ip"]

def buildTester():
    config = readJSON(CONFIG_PATH)
    return fTester.F_Tester(config["tester_ip"], config["tester_name"])


def getTestDuration(test):
    test_config=readJSON(TEST_CONFIGS_DIR+"/"+test)
    total_duration = test_config.get("duration", 0)
    return total_duration




