#!/usr/bin/python3

import time
import os.path
import sys
import json
from collections import Counter

def write_matchInfo(outputFile, matchInfo):
    encoder = json.JSONEncoder()
    with open(outputFile, 'w') as database:
            database.write(encoder.encode(matchInfo))
    database.close()

def read_matchInfo(inputFile):
    print("Reading "+inputFile)
    with open(inputFile, 'r') as database:
            data = json.load(database)
    database.close()
    return data
                
def strip_info(matchInfo, idSet):
    strippedInfo = []
    for match in matchInfo:
        #check if dupe or null
        if match == None:
            print('match = None')
            continue
        if match['matchId'] not in idSet:
            print("dupe found and destroyed")
            continue
        idSet.remove(match['matchId'])

        #check if victory valid
        win100=None
        win200=None
        for team in match['teams']:
            if team['teamId']==100:
                win100=team['winner']
            if team['teamId']==200:
                win200=team['winner']
        if (win100==None or win200==None) or (win100==win200):
            print('match '+str(match['matchId'])+' victory data incorrect')
            continue
        
        #check if champions and bans valid
        count100 = 0
        champions100 = []
        count200 = 0
        champions200 = []
        for participant in match['participants']:
            if participant['teamId']==100:
                count100+=1
                champions100.append(participant['championId'])
            if participant['teamId']==200:
                count200+=1
                champions200.append(participant['championId'])

        bans = []
        for team in match['teams']:
            if 'bans' in team.keys():
                for ban in team['bans']:
                    #print(ban)
                    bans.append(ban['championId'])
                
        if count100!=5 or count200!=5:
            print('match '+str(match['matchId'])+' champion count incorrect')
            print("team 100: " + str(count100) + " team 200: " + str(count200))
            continue

        championstotal = champions100 + champions200
        championstotalbans = champions100 + champions200 + bans
        #print(championstotal)
        #print(Counter(championstotal).items())
        for champ, amount in Counter(championstotal).items():
            if (amount > 1):
                print('match '+str(match['matchId'])+' champion occurs twice')
                continue

        for champ, amount in Counter(bans).items():
            if (amount > 1):
                print('match '+str(match['matchId'])+' champion banned twice')
                continue

        for champ, amount in Counter(bans).items():
            if (amount > 1):
                print('match '+str(match['matchId'])+' banned champion played the match')
                continue

        #Strip the info
        strippedElement = {}
        strippedElement['teams'] = match['teams']
        for item in match['participants']:
            item.pop('stats',None)
            item.pop('masteries',None)
            item.pop('runes',None)
            item.pop('timeline',None)
            item.pop('highestAchievedSeasonTier',None)
        strippedElement['participants'] = match['participants']
        strippedInfo.append(strippedElement)
    return strippedInfo

def fillIdset(parts, idSet):
    for curIndex in range(parts):
        temp = read_matchInfo("matchInfo_part_"+str(curIndex)+".json")
        for match in temp:
            if match != None:
                idSet.add(match['matchId'])
    
def main():
    idSet = set()
    parts = int(input('How many parts need to be processed?'))
    fillIdset(parts, idSet)
    print(str(len(idSet)) + " unique matches found")
    time.sleep(0.5)
    cleanInfo = []
    for curIndex in range(parts):
        print("Start part " + str(curIndex))
        temp = read_matchInfo("matchInfo_part_"+str(curIndex)+".json")
        print("Stripping info..")
        temp = strip_info(temp, idSet)
        cleanInfo += temp
    print("Writing everything to disk")
    write_matchInfo("clean_merged_data.json",cleanInfo)
    print("Done")
    
    

if __name__ == "__main__":
    main()
