#!/usr/bin/python3

from RiotAPI import RiotAPI
import argparse
import time

def read_matchIDs(inputFile):
    matchIDs = set()
    counter = 0
    with open(inputFile, 'r', encoding='utf-8') as database:#, encoding='utf-8'
        for line in database:
            matchIDs.add(line.rstrip())
            counter+=1
    print("Read " + str(counter) + " match IDs.")
    print("From which " + str(len(matchIDs)) + " are unique.")
    database.close()
    return matchIDs

def write_matches(outputFile, matchInfoList):
    #TODO stop using txt, use a json file for easy parsing and writing
    print("Writing info of " + str(len(matchList)) + " matches to disk..")
    #OVERWRITES LAST FILE! BE CAREFUL!
    with open(outputFile, 'w') as database:
        for m in matchInfoList:
            database.write(str(m) + '\n')
    print("Done writing")
    database.close()

def collect_matchInfo(api, matchIDs):
    beginTime = time.time()
    lastMessage = time.time()
    progcount = 0
    for mid in matchIDs:
        if time.time() > (lastMessage + 10):
            lastMessage = time.time()
            elapsed = time.time() - beginTime
            print("Running for: " + str(int(elapsed)) + " sec  - "
                + "Progress: " + str(round(100 * progcount / len(summonerIDs), 3)) + "% - "
                + "Time remaining: " + str(round((elapsed / (progcount / len(summonerIDs))) - elapsed,1)) + " sec")
        matchinfo = api.get_match_by_id(mid)
        #How do we store this data?
        progcount = progcount + 1
    return matchIDs
                


def main():
    parts = 10
    #The api key is not hardcoded because it should not be publicly available on github
    api_key = input('Enter API key: ')
    print('')
    api = RiotAPI(api_key)
    matchIDs = list(read_matchIDs('matches.txt'))
    #experiment to test if all matches have well-formed data (succesful for test with 800 matches)
    for match in matchIDs:
        print(match)
        temp = api.get_match_by_id(match, {'includeTimeline': False})
        win100=None
        win200=None
        for element in temp['teams']:
            #print(str(element['teamId'])+" "+str(element['winner']))
            if element['teamId']==100:
                win100=element['winner']
            if element['teamId']==200:
                win200=element['winner']
        if (win100==None or win200==None) or (win100==win200):
            print('ERROR ERROR TEAM ERRROOOOOORR ERROROOROROROROROR ERRORR!!!')
        count100 = 0
        count200 = 0
        for element in temp['participants']:
            #print(str(element['championId'])+" "+str(element['teamId']))
            if element['teamId']==100:
                count100+=1
            if element['teamId']==200:
                count200+=1
        if count100!=5 or count200!=5:
            print('ERROR ERROR CHAMPION ERRROOOOOORR ERROROOROROROROROR ERRORR!!!')
        #print('')
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
