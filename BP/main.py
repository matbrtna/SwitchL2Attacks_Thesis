#!/usr/bin/env python3

import argparse
import connectionThrottling
import rstpAttack
import macFlooding
import connectionSpeed
import connectionLossAnalysys
import processKill
import utils
import sys 
import os
import json

def get_app_root():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))


APP_ROOT = get_app_root()
CONFIG_PATH       = os.path.join(APP_ROOT, "config.json")
CAPTURES_DIR      = os.path.join(APP_ROOT, "captures")
TEST_CONFIGS_DIR  = os.path.join(APP_ROOT, "test_configs")
TEST_RESULTS_DIR  = os.path.join(APP_ROOT, "test_results")


with open(CONFIG_PATH) as f:
    config = json.load(f)

os.makedirs(TEST_RESULTS_DIR, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(prog="metelTest")
    # parser.add_argument("-t", "--test", action="store_true", help="Spustí test")
    parser.add_argument("-r", "--rstp", action="store_true", help="Runs RSTP attack on deice, make sure you are using RSTP mode")
    parser.add_argument("-m", "--macflood", action="store_true", help="Runs MAC flood attack on device, any mode can be used")
    parser.add_argument( "-t", "--throttling",type=int,required=False, metavar="SECONDS", help="Runs connection throthling test, make have defined maximal allowed speed in configuration")
    parser.add_argument("-s", "--speed", action="store_true", help="Runs speed test, this test will maximum speed capable")
    parser.add_argument("-l", "--loss", action="store_true", help="Runs connection loss test on LAN-RING, you have to disconnect the main route from master switch during this test")
    parser.add_argument("-k", "--kill", action="store_true", help="Kills all tcpdump and macof processes (use if bug with unkilled porcesses appears)")
    args = parser.parse_args()
    if args.rstp:
        print("Running RSTP attack...")
        interface = utils.getInterface(CONFIG_PATH)
        ip = utils.getTesterIp(CONFIG_PATH)
        rstpAttack.runRstpAttack(interface,ip)

    elif args.macflood:
        print("Running MAC flood attack...")
        interface = utils.getInterface(CONFIG_PATH)
        ip = utils.getTesterIp(CONFIG_PATH)
        macFlooding.getMacFloodResult(interface, ip, 20)

    elif args.throttling:
        print("Running throttling test...")
        connectionThrottling.getResult(args.throttling)

    elif args.speed:
        print("Running speed test...")
        connectionSpeed.getResult()

    elif args.loss:
        print("Running connection loss test...")
        connectionLossAnalysys.getResult()

    elif args.kill:
        print("Killing processes...")
        processKill.kill_processes()
    else:
        parser.print_help()

if __name__ == "__main__":
    print("CONFIG_PATH:", CONFIG_PATH)
    print("Soubor existuje:", os.path.exists(CONFIG_PATH))
    main()