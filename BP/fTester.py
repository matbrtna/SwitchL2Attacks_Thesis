import json
import requests
from datetime import datetime
import re
import sys
from bs4 import BeautifulSoup
import utils
import time


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
        return response
    
    def execute(self,test_scenario):
        url="http://"+self.ip+"/cgi-bin/luci/ftplanner/execute"
        response = requests.post(url, json=test_scenario,verify=False)
        return response


    def getTestIdFromOverview(self,test):
        return test['uid']
    
    def startTest(self,name):
        request_body=utils.readJSON("test_configs/"+name)
        current_time = int(time.time())

# Nastavíme "now" na aktuální čas a "start" o 10 sekund později
        request_body['now'] = current_time
        request_body['start'] = current_time + 10
        url="http://"+self.ip+"/cgi-bin/luci/ftplanner/execute"
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, json=request_body, headers=headers)
            if response.status_code == 200:
                print("TCP scenario successfully started ")
                # print("Odpověď: ", response.json())
            else:
                print("Error while starting the scenario: ", response.status_code)
                print("Response: ", response.text)
        
        except requests.exceptions.RequestException as e:
            print("There was error while sending the request to tester: ", e)
            sys.exit(1)
        return response
        

class TestResult:
    def __init__(self,id):
        self.id=id
    




# tester=F_Tester("192.168.0.201")
# test_overview=tester.getLastTestOverview()
# testId=tester.getTestIdFromOverview(test_overview)
# test=requests.get("http://192.168.0.201/cgi-bin/luci/ftplanner/file?file=127.0.0.1/client-1.iperf3.gz&scenario=UDP-20250422195637-1745344906&archive=false",verify=False)
# print(test.json())


# http://192.168.0.201/cgi-bin/luci/ftplanner/files?uid=UDP-20250422195637-1745344906&archive=false

# http://192.168.0.201/cgi-bin/luci/ftplanner/remove?uid=TCP-20250501101412-1746087544&archive=false
# test_result=tester.getTestResult()
# tester.downloadResult()


# client-1.flowping.gz&scenario=PreruseniTopologieMNGMT-20250330212403-1743362513
# http://192.168.0.201/cgi-bin/luci/ftplanner/file?file=127.0.0.1/client-1.iperf3.gz&scenario=UDP-20250422195637-1745344906&archive=false
# http://192.168.0.201/cgi-bin/luci/ftplanner/file?file=127.0.0.1/server-1.iperf3.gz&scenario=UDP-20250422195637-1745344906&archive=false
# http://192.168.0.201/cgi-bin/luci/ftplanner/file?file=127.0.0.1/server-2.iperf3.gz&scenario=UDP-20250422195637-1745344906&archive=false



# {"name":"TCP-20250501133208","description":"","template_version":"1.0","start":1746099128,"now":1746099118,"restart_tests":false,"force_restart":false,"scenario_id":0,"note":"","duration":60,"download_later":"false","repeat":1,"remote_opts":{},"tests":[{"type":"iperf3","ip":"127.0.0.1","ip_server":"192.168.0.204","opts_server":"-i 1 --rcv-timeout 30000 --snd-timeout 30000","test":{"duration":60,"delay":0,"target_port":1234,"target_ip":"192.168.0.204","opts":"-J --parallel 1 -i 1 --window 0k --set-mss 1400 -C cubic --bitrate 0k --connect-timeout 1000 --rcv-timeout 30000 --snd-timeout 30000","mode":"time","interval":1}},{"type":"iperf3","ip":"127.0.0.1","ip_server":"192.168.0.204","opts_server":"-i 1 --rcv-timeout 30000 --snd-timeout 30000","test":{"duration":60,"delay":0,"target_port":1234,"target_ip":"192.168.0.204","opts":"-J -R --parallel 1 -i 1 --window 0k --set-mss 1400 -C cubic --bitrate 0k --connect-timeout 1000 --rcv-timeout 30000 --snd-timeout 30000","mode":"time","interval":1}}]}

# print(datetime.timestamp)
# timestamp = 1745282709
# dt = datetime.fromtimestamp(timestamp)


# print(dt.strftime('%Y-%m-%d %H:%M:%S'))