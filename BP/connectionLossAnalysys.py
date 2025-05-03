import pandas as pd
import utils
# test_results/preruseni.csv





# def readCSV(name):
#     df = pd.read_csv("test_results/"+name, sep=";")
#     return df


def findLoss(file):
    loss=utils.findJSONColumn(file,"loss")
    # print(loss)
    # print(loss)
    return loss


def getNonZeroValues(values):
    non_zero_values = [v for v in values if v != 0]
    return non_zero_values

def sumarizeValues(values):
    total = sum(values)
    return total

def convertToMS(percents):
    timeInMS=percents*10
    return timeInMS


def getConnectionLossResult(timeUnconnected):
    print("Device lost connection for: "+ str(timeUnconnected)+" ms")
    if timeUnconnected>30:
        print("Time is more than 30ms, test was unsuccesfull")
    elif timeUnconnected==0:
        print("Connection was not broken, check if you unconnected right path")
    else:
        print("Time is less than 30ms, test was succesfull")


def evaulateTestFromJSON(name):
    # csv=utils.readCSV(name)
    file=utils.readJSON("test_results/"+name)
    loss=findLoss(file)
    non_zero_values=getNonZeroValues(loss)
    sum=sumarizeValues(non_zero_values)
    lost_in_ms=convertToMS(sum)
    result=getConnectionLossResult(lost_in_ms)



evaulateTestFromJSON("test-1.flowping")



