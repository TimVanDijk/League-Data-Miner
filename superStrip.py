#!/usr/bin/python3

import time
import os.path
import sys
import json
'''
def write_matchInfo(outputFile, matchInfo, part):
    encoder = json.JSONEncoder()
    with open(outputFile, 'w') as database:
            database.write(encoder.encode(matchInfo))
    print("Done writing part " + str(part) + ".")
    print('')
    database.close()
'''
def read_matchInfo(inputFile):
    print("Reading json")
    print('')
    with open(inputFile, 'r') as database:
            data = json.load(database)
    database.close()
    return data
'''                
def strip_info(matchInfo, idSet):
    strippedInfo = []
    print(len(idSet))
    for matchElement in matchInfo:
        if matchElement == None:
            print('match '+str(matchElement)+' = NONE ERORORORORORORO EROOOOR')
            continue
        if matchElement['matchId'] in idSet:
            print("dupe found and destroyed")
            continue
        idSet.add(matchElement['matchId'])
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
'''
def fillIdset(parts, idSet):
    for curIndex in range(parts):
        temp = read_matchInfo("matchInfo_part_"+str(curIndex)+".json")
        for match in temp:
            if match != None
                idSet.add(match['matchId'])
    
def main():
    idSet = set()
    parts = int(input('How many parts need to be processed?'))
    fillIdset(parts, idSet)
    print(len(idSet))
    '''
    parts = 20  
    for curIndex in range(parts):
        print("Start part " + str(curIndex))
        temp = read_matchInfo("matchInfo_part_"+str(curIndex)+".json")
        print("Stripping info..")
        temp = strip_info(temp, idSet)
        write_matchInfo("clean_match_part_"+str(curIndex)+".json", temp, curIndex)
        print("Done with part " + str(curIndex))
        print("Writing it to disk..")
        
        
    '
    #experiment to test if all matches have well-formed data (succesful for test with 800 matches)
    matchIDs = read_matchIDs('matches.txt')
    for match in matchIDs:
        print(match)
        temp = api.get_match_by_id(match, {'includeTimeline': False})
        win100=None
        win200=None
        for element in temp['teams']:
            print(str(element['teamId'])+" "+str(element['winner']))
            if element['teamId']==100:
                win100=element['winner']
            if element['teamId']==200:
                win200=element['winner']
        if (win100==None or win200==None) or (win100==win200):
            print('ERROR ERROR TEAM ERRROOOOOORR ERROROOROROROROROR ERRORR!!!')
        count100 = 0
        count200 = 0
        for element in temp['participants']:
            print(str(element['championId'])+" "+str(element['teamId']))
            if element['teamId']==100:
                count100+=1
            if element['teamId']==200:
                count200+=1
        if count100!=5 or count200!=5:
            print('ERROR ERROR CHAMPION ERRROOOOOORR ERROROOROROROROROR ERRORR!!!')
        print('')
        time.sleep(20)
    '''
    '''
    for i in range(0, parts):
        print("Processing part " + str(i+1) + " out of " + str(parts) + "...")
        matchListPart = matchIDs[int(i/parts*len(matchIDs)):int((i+1)/parts*len(matchIDs))]
        matchInfoList = collect_matchInfo(api, matchListPart)
        write_matches("matchinfo_part"+str(i)+".txt", matchInfoList)
        
    print("Done")
    '''

if __name__ == "__main__":
    main()
