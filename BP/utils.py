import pandas as pd
import json
import sys

def readCSV(name):
    df = pd.read_csv(name, sep=";")
    return df

def findColumnValues(file,name):
    values = file[name].dropna()
    return values

def findColumn(csv, name):
    result = csv[csv["jmeno"] == "Eva"]


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
            # print(f"Seq {entry['seq']}: loss = {loss_value}")
            # if loss_value > 0:
            #     print("  ⚠️  Ztráta paketů detekována!")
    if len(values)>0:
        # print(values)
        return values
    else:
        print("Hodnota loss nebyla v tabulce nalezena, zkontrolujte ze zapinate spravny test")
        sys.exit(1)


class ConfReader:
    def __init__(self,name):
        self.name=name
        

    def open(self):
        with open(self.name, 'r') as f:
            self.file = json.load(f)
            print("Config file: "+ self.name + " loaded")
    
    def read(self,name):
        return self.file[name]