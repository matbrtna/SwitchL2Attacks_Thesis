import utils
import time

def getTest():
    return utils.readJSON("test_results/udp.json")




def getSpeedList(test):
    return [interval["sum"]["bits_per_second"] for interval in test["intervals"]]


def getAvarage(speed_list):
    return sum(speed_list) / len(speed_list)

def convertToMb(speed):
    return speed/1000000


def getMax(speed_list):
    return max(speed_list)



def evaulateTest(wantedSpeedInMb,test):
    speeed_list=getSpeedList(test)
    avarage=convertToMb(getAvarage(speeed_list))
    max=convertToMb(getMax(speeed_list))
    abs_difference_average = abs(wantedSpeedInMb - avarage)
    abs_difference_max = abs(wantedSpeedInMb - max)
    rel_difference_max = abs((wantedSpeedInMb - max) / wantedSpeedInMb) * 100
    rel_difference_average = abs((wantedSpeedInMb - avarage) / wantedSpeedInMb) * 100
    # print(wantedSpeedInMb)
    print(f"Average speed on L2 was: {avarage:.2f} Mbps")
    print(f"Max speed on L2 was: {max:.2f} Mbps")
    print(f"Difference between average speed and wanted speed: {abs_difference_average:.2f} Mbps, equals {rel_difference_average:.1f}% difference")
    print(f"Difference between max speed and wanted speed: {abs_difference_max:.2f} Mbps, equals {rel_difference_max:.1f}% difference")
    



def getResult(wantedSpeedInMb):
    try:
        test_name="connectionThrottling.json"
        tester=utils.buildTester()
        tester.startTest(test_name)
        print("Waiting for end of the test")
        sleep_time=utils.getTestDuration(test_name)+30
        time.sleep(sleep_time)
        test_result_us,test_result_ds=tester.getLastTcpSpeedTest()
        print("UDP Downstream:")
        evaulateTest(wantedSpeedInMb,test_result_ds)
        print("UDP Upstream")
        evaulateTest(wantedSpeedInMb,test_result_us)
    except KeyboardInterrupt:
        print("")
        print("Test was interrupted by user")
    except Exception as e:
        print(f"Unexpected error during test: {e}")



