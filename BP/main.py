#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser(prog="metelTest")
    parser.add_argument("-t", "--test", action="store_true", help="Spustí test")
    args = parser.parse_args()
    if args.test:
        print("🧹 Spouštím metelTest braaaap -t")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()