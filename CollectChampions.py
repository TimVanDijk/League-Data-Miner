#!/usr/bin/python3

from RiotAPI import RiotAPI
import argparse
import json
import os


def write_champs(outputFile, champList):
    encoder = json.JSONEncoder()
    with open(outputFile, 'w') as database:
            database.write(encoder.encode(champList))
    print("Done writing")
    database.close()

def write_portrait(outputFile, byteData):
    with open(outputFile, 'wb') as f:
        f.write(byteData)

def main():
    #The api key is not hardcoded because it should not be publicly available on github
    api_key = input('Enter API key: ')
    print('')
    api = RiotAPI(api_key)
    champData = api.get_all_champions()['data']
    champList = []
    for item in champData.keys():
        champList.append((champData[item]['id'],champData[item]['key']))
    write_champs('champions.json',champList)

    avatardir = os.path.dirname(os.path.abspath(__file__))+"/portraits/"
    if not os.path.exists(avatardir):
        os.makedirs(avatardir)

    for item in champList:
        portrait = api.get_champion_portrait(item[1])
        write_portrait("portraits/"+str(item[0])+".png",portrait)
    

if __name__ == "__main__":
    main()
