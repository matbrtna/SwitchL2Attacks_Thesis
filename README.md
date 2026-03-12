# metelTest

This application is designed for automated performance and penetration testing of network switches manufactured by METEL s.r.o. Many of implemented features are meant to be used with F-Tester device that was developed at FEE CTU and will not be working it without it.

## Instalation

To install the project, run the BASH script named install.sh. Upon execution, the script will download the necessary dependencies and build the binary executable.

## Features

Some tests are designed to test the performance of the switche wihle others are meant to test the security of the device and test the configuration. The test usage can be controlled by the using arguments with the script.

## Usage
To run the installed project, simply enter metelTest into your CLI followed by the desired parameters:

-t Starts a throughput throttling test. A parameter is required (e.g., -t 50 for a 50 Mbps limit).

-l Starts a topology recovery speed test (e.g., measuring convergence time during network path changes).

-m Initiates a MAC flooding attack (utilizes the macof tool).

-r Initiates an RSTP attack using forged BPDU frames.

-k Terminates tcpdump and macof processes if they were not closed correctly.

-h Displays this help message. 

## Project structure
.
├── test_configs/               - Configuration files for individual tests
├── test_results/               - Results downloaded from F-Testers
├── unit_tests/                 - Unit tests (e.g., for connectionSpeed.py)
├── build_metelTest.py          - Environment build and customization script
├── config.json                 - Main application configuration file
├── connectionLossAnalysis.py   - Network connection loss analysis test
├── connectionSpeed.py          - Maximum network speed test
├── connectionThrottling.py     - Throughput limitation test
├── fTester.py                  - Script for communication with testers
├── install.sh                  - Installation script for dependencies
├── macFlooding.py              - MAC flooding attack implementation
├── main.py                     - Main application entry point
├── metelTest.spec              - PyInstaller configuration file
├── processes.py                - Subprocess management script
├── processKill.py              - Tool for terminating tcpdump and macof
├── rstpAttack.py               - RSTP attack via BPDU spoofing
├── scapyPackets.py             - Packet manipulation using Scapy
├── setup.py                    - Python package installation (optional)
├── utils.py                    - Utility and helper functions
└── vlanTest.py                 - VLAN behavior test (not yet implemented)