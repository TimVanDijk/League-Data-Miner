#!/usr/bin/python3

from RiotAPI import RiotAPI
import argparse
import time

def read_summoners(inputFile):
    #TODO stop using txt, use a json file for easy parsing and writing
    summonerIDs = set()
    counter = 0
    uniqcounter = 0
    with open(inputFile, 'r') as database:#, encoding='utf-8'
        for line in database:
            counter+=1
            sid = line.split(' ')[0]
            if sid not in summonerIDs:
                uniqcounter+=1
            summonerIDs.add(sid)
    print("Read " + str(counter) + " summoner ids.")
    print(str(uniqcounter) + " unique.")
    database.close()
    return summonerIDs

def write_matches(outputFile, matchList):
    #TODO stop using txt, use a json file for easy parsing and writing
    print("Writing " + str(len(matchList)) + " matches to disk..")
    #OVERWRITES LAST FILE! BE CAREFUL!
    with open(outputFile, 'w') as database:
        for m in matchList:
            database.write(str(m) + '\n')
    print("Done writing")
    database.close()

def collect_matchIDs_from_patch(api, summonerIDs, patch_epoch_mil, end_epoch_mil):
    matchIDs = set()
    beginTime = time.time()
    lastMessage = time.time()
    progcount = 0
    for sid in summonerIDs:
        if time.time() > (lastMessage + 10):
            lastMessage = time.time()
            elapsed = time.time() - beginTime
            print("Running for: " + str(int(elapsed)) + " sec  - "
                + "Progress: " + str(round(100 * progcount / len(summonerIDs), 3)) + "% - "
                + "Time remaining: " + str(round((elapsed / (progcount / len(summonerIDs))) - elapsed,1)) + " sec")
        temp = api.get_matchlist_by_summonerid(sid,{'beginTime':patch_epoch_mil ,'rankedQueues':'RANKED_SOLO_5x5' , 'endTime': end_epoch_mil})
        if temp['totalGames'] != 0:
            tempList = temp['matches']
            for match in tempList:
                matchIDs.add(match['matchId'])
        progcount = progcount + 1
    return matchIDs
                


def main():
    last_patch_epoch_mil = 1448372142000
    end_range_epoch_mil = 1449234650000
    parts = 10
    #The api key is not hardcoded because it should not be publicly available on github
    api_key = input('Enter API key: ')
    print('')
    api = RiotAPI(api_key)
    summonerList = list(read_summoners('summoners.txt'))

    for i in range(0, parts):
        print("Processing part " + str(i) + "...")
        summonerListPart = summonerList[int(i/parts*len(summonerList)):int((i+1)/parts*len(summonerList))]
        matchIdList = collect_matchIDs_from_patch(api, summonerListPart, last_patch_epoch_mil, end_range_epoch_mil)
        write_matches("matches_part"+str(i)+".txt", matchIdList)
    print("Done")

if __name__ == "__main__":
    main()
