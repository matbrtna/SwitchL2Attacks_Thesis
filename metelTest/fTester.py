
import requests
from datetime import datetime
import sys
# from bs4 import BeautifulSoup
import utils
import time
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH       = os.path.join(APP_ROOT, "config.json")
CAPTURES_DIR      = os.path.join(APP_ROOT, "captures")
TEST_CONFIGS_DIR  = os.path.join(APP_ROOT, "test_configs")
TEST_RESULTS_DIR  = os.path.join(APP_ROOT, "test_results")



class F_Tester:
    def __init__(self,ip,name="defult_tester") -> None:
        self.ip=ip
        self.name=name


    def pingTester(self):
        pass


    def getResults(self):
        try:
            response = requests.get(
                "https://" + self.ip + "/cgi-bin/luci/ftplanner/results?archive=false",
                verify=False,
                timeout=5  # čeká max. 5 sekund
            )
            response = response.json()
            return response
        except requests.exceptions.Timeout:
            print("Chyba: Server neodpověděl do 5 sekund. Zkuste zkontrolovat pripojeni k F-Testeru.")
            print("IP F-Testeru: "+ self.ip)
            sys.exit(1)
        except requests.exceptions.ConnectionError as e:
            print("Chyba připojení:", e)
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print("Obecná chyba požadavku:", e)
            sys.exit(1)
                
    def getLastTestOverview(self):
        sorted_tests=self.getSortedTests()
        last_test_overview=sorted_tests[-1]
        return last_test_overview
        

    def getLastTest(self):
        last_test_overview=self.getLastTestOverview()
        las_test_id=self.getTestIdFromOverview(last_test_overview)
        last_test=self.getTestResult(las_test_id)
        return last_test
    
    def getLastTcpSpeedTest(self):
        last_test_overview=self.getLastTestOverview()
        last_test_id=self.getTestIdFromOverview(last_test_overview)
        url_client2="client-2.iperf3.gz&scenario="+last_test_id
        url_client1="client-1.iperf3.gz&scenario="+last_test_id
        last_test_us=self.getTestResult(url_client1)
        last_test_ds=self.getTestResult(url_client2)
        return last_test_us,last_test_ds   
    
    def getLastFlowPingTest(self):
        last_test_overview=self.getLastTestOverview()
        las_test_id=self.getTestIdFromOverview(last_test_overview)
        url="client-1.flowping.gz&scenario="+las_test_id
        # print(url)
        last_test=self.getTestResult(url)
        return last_test
    
    def getLastUdpTrottlingTest(self):
        last_test_overview=self.getLastTestOverview()
        last_test_id=self.getTestIdFromOverview(last_test_overview)
        url_client2="client-2.iperf3.gz&scenario="+last_test_id
        url_client1="client-1.iperf3.gz&scenario="+last_test_id
        last_test_us=self.getTestResult(url_client1)
        last_test_ds=self.getTestResult(url_client2)
        return last_test_us,last_test_ds   
        
    def getSortedTests(self):
        tests=self.getResults()
        sorted_tests = sorted(
        tests,
        key=lambda test: datetime.strptime(test["status"]["date"], "%Y-%m-%d %H:%M:%S")
        )   
        return sorted_tests

    def getTestResult(self,name):
        url="http://"+self.ip+"/cgi-bin/luci/ftplanner/file?file=127.0.0.1/"+name+"&archive=false"
        response=requests.get(url,verify=False)
        return response.json()
    



    def getTestIdFromOverview(self,test):
        return test['uid']
    
    def startTest(self,name):
        request_path = os.path.join(TEST_CONFIGS_DIR, name)
        request_body = utils.readJSON(request_path)
        current_time = int(time.time())


        request_body['now'] = current_time
        request_body['start'] = current_time + 10
        url="http://"+self.ip+"/cgi-bin/luci/ftplanner/execute"
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, json=request_body, headers=headers)
            if response.status_code == 200:
                print("Scenario successfully started on F-Tester")
         
            else:
                print("Error while starting the scenario: ", response.status_code)
                print("Response: ", response.text)
        
        except requests.exceptions.RequestException as e:
            print("There was error while sending the request to tester: ", e)
            sys.exit(1)
        return response


    




