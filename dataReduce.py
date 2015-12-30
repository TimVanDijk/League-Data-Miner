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
    print("Done writing")
    print('')
    database.close()

def read_matchInfo(inputFile):
    print("Reading json")
    with open(inputFile, 'r') as database:
            data = json.load(database)
    database.close()
    return data
                
def reduce_data(matchList):
    strippedInfo = []
    
    print(matchList[0].keys())
    print("")
    print(matchList[0]['teams'][0].keys())
    print("")
    print(matchList[0]['teams'][0])
    print("")     
    print(matchList[0]['participants'][0].keys())
    print("")
    print(matchList[0]['participants'][0])
    print("")
    print("")
    print(matchList[0])
    '''
    counter = 0
    for match in matchList:
        win100=None
        win200=None
        for team in match['teams']:
            if team['teamId']==100:
                win100=team['winner']
            if team['teamId']==200:
                win200=team['winner']
        if (win100==None or win200==None) or (win100==win200):
            print('ERROR ERROR TEAM ERRROOOOOORR ERROROOROROROROROR ERRORR!!!')
            
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
            print('ERROR ERROR CHAMPION ERRROOOOOORR ERROROOROROROROROR ERRORR!!!')
            print("team 100: " + str(count100) + " team 200: " + str(count200))
            for participant in match['participants']:
                print(participant)
            print(match)
            print(counter)

        championstotal = champions100 + champions200
        display = False
        for champ, amount in Counter(championstotal).items():
            if (amount > 1):
                display=True
        if display:
            print(Counter(championstotal))
            print(match['matchId'])
        
        counter += 1
        '''
            
    return strippedInfo
    
def main():
    print("Start")
    temp = read_matchInfo("merged_data.json")
    print("Reducing data")
    temp = reduce_data(temp)
    print("Writing it to disk..")
        
        
    

if __name__ == "__main__":
    main()
