import utils


def getTestUS():
    return utils.readJSON("test_results/maxSpeedUS.json")


def getTestDS():
    return utils.readJSON("test_results/maxSpeedDS.json")

def getTest():
    return utils.readJSON("test_results/maxRychlostUS.json")

def getSpeedList(test):
    return [interval["sum"]["bits_per_second"] for interval in test["intervals"]]

def getAvarage(speed_list):
    return sum(speed_list) / len(speed_list)

def getMax(speed_list):
    return max(speed_list)


def convertToMb(speed):
    return speed/1000000


def getResultUS():
    print("TCP Upstreeam:")
    test=getTestUS()
    speeed_list=getSpeedList(test)
    avarage=convertToMb(getAvarage(speeed_list))
    max=convertToMb(getMax(speeed_list))
    print(f"Average speed was: {avarage:.2f} Mbps")
    print(f"Max speed was: {max:.2f} Mbps")
    if avarage<85:
        print("Speed was lower than 85. Usual speed on L4 should be around 94, topology is not working right")
    else:
        print("Test was successfull")
    print("\n")


def getResultDS():
    print("TCP Downstream:")
    test=getTestDS()
    speeed_list=getSpeedList(test)
    avarage=convertToMb(getAvarage(speeed_list))
    max=convertToMb(getMax(speeed_list))
    print(f"Average speed was: {avarage:.2f} Mbps")
    print(f"Max speed was: {max:.2f} Mbps")
    if avarage<85:
        print("Speed was lower than 85. Usual speed on L4 should be around 94, topology is not working right")
    else:
        print("Test was successfull")

getResultUS()
getResultDS()