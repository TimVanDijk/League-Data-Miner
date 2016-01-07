#!/usr/bin/python3

import time
import os.path
import sys
import json
'''
def write_matchInfo(outputFile, matchInfo):
    encoder = json.JSONEncoder()
    with open(outputFile, 'w') as database:
            database.write(encoder.encode(matchInfo))
    print("Done writing part " + str(part) + ".")
    print('')
    database.close()
'''
def read_matchInfo(inputFile):
    print("Reading "+inputFile)
    with open(inputFile, 'r') as database:
            data = json.load(database)
    database.close()
    return data
                
def strip_info(matchInfo, idSet):
    strippedInfo = []
    for matchElement in matchInfo:
        #check if dupe or null
        if matchElement == None:
            print('match '+str(matchElement)+' = None')
            continue
        if matchElement['matchId'] not in idSet:
            print("dupe found and destroyed")
            continue
        idSet.remove(matchElement['matchId'])

        #check if victory valid
        win100=None
        win200=None
        for team in match['teams']:
            if team['teamId']==100:
                win100=team['winner']
            if team['teamId']==200:
                win200=team['winner']
        if (win100==None or win200==None) or (win100==win200):
            print('match '+str(matchElement)+' victory data incorrect')
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
                
        if count100!=5 or count200!=5:
            print('match '+str(matchElement)+' champion count incorrect')
            print("team 100: " + str(count100) + " team 200: " + str(count200))
            for participant in match['participants']:
                print(participant)

        championstotal = champions100 + champions200

        for champ, amount in Counter(championstotal).items():
            if (amount > 1):
                print(Counter(championstotal))
                print(match['matchId'])

            



        
        
        strippedElement = {}
        strippedElement['teams'] = matchElement['teams']
        for item in matchElement['participants']:
            item.pop('stats',None)
            item.pop('masteries',None)
            item.pop('runes',None)
            item.pop('timeline',None)
            item.pop('highestAchievedSeasonTier',None)
        strippedElement['participants'] = matchElement['participants']
        strippedInfo.append(strippedElement)
    return strippedInfo

def fillIdset(parts, idSet):
    for curIndex in range(parts):
        temp = read_matchInfo("matchInfo_part_"+str(curIndex)+".json")
        print(matchList[0].keys())
        for match in temp:
            if match != None:
                idSet.add(match['matchId'])
    
def main():
    idSet = set()
    parts = int(input('How many parts need to be processed?'))
    fillIdset(parts, idSet)
    print(len(idSet) + " unique matches found")
    '''
    for curIndex in range(parts):
        print("Start part " + str(curIndex))
        temp = read_matchInfo("matchInfo_part_"+str(curIndex)+".json")
        print("Stripping info..")
        temp = strip_info(temp, idSet)
        write_matchInfo("clean_match_part_"+str(curIndex)+".json", temp, curIndex)
        print("Done with part " + str(curIndex))
        print("Writing it to disk..")
    '''
    

if __name__ == "__main__":
    main()
