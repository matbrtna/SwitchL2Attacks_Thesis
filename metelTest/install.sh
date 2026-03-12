#!/bin/bash
set -e

sudo apt install -y dsniff
sudo apt install -y tcpdump
sudo python3 build_metelTest.py
