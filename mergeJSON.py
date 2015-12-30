#!/usr/bin/python3

import time
import os.path
import sys
import json
import argparse

def read_matchInfo(inputFile):
    print("Reading json")
    print('')
    with open(inputFile, 'r') as database:
            data = json.load(database)
    database.close()
    return data

def write_matchInfo(outputFile, matchInfo):
    encoder = json.JSONEncoder()
    with open(outputFile, 'w') as database:
            database.write(encoder.encode(matchInfo))
    print("Done writing")
    print('')
    database.close()

def main():
    parts = int(input('How many parts need to be merged?'))
    names = input('Naming scheme of the files? [example](0-parts).json:')
    fullSet = []
    for curIndex in range(parts):
        print("Part " + str(curIndex))
        fullSet += read_matchInfo(str(names)+str(curIndex)+".json")
    write_matchInfo("merged_data.json", fullSet)
    print("Writing it to disk..")

if __name__ == "__main__":
    main()
