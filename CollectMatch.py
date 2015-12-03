#!/usr/bin/python3

from RiotAPI import RiotAPI
import argparse
import time

def read_summoners(inputFile):
    #TODO stop using txt, use a json file for easy parsing and writing
    summonerIDs = set()
    counter = 0    
    with open(inputFile, 'r', encoding='utf-8') as database:
        for line in database:
            counter+=1
            sid = line.split(' ')[0]
            summonerIDs.add(sid)
    print("Read " + str(counter) + " summoner ids.")
    database.close()
    return summonerIDs

def collect_matchIDs_from_patch(api, summonerIDs, patch_epoch_mil):
    matchIDs = set()
    for sid in summonerIDs:
        tempList = api.get_matchlist_by_summonerid(sid,{'beginTime':patch_epoch_mil ,'rankedQueues':'RANKED_SOLO_5x5'})['matches']
        for match in tempList:
            matchIDs.add(match['matchId'])
    return matchIDs
                


def main():
    last_patch_epoch_mil = 1448372142000
    #TODO: Move code out of main()
    parser = argparse.ArgumentParser()
    parser.add_argument("amount", help="Amount of IDs to collect", type=int)
    amount = parser.parse_args().amount
    #The api key is not hardcoded because it should not be publicly available on github
    api_key = input('Enter API key: ')
    print('')
    api = RiotAPI(api_key)
    matchlist = api.get_matchlist_by_summonerid(56673574,{'beginTime':last_patch_epoch_mil ,'rankedQueues':'RANKED_SOLO_5x5'})
    print(matchlist['matches'][0])
    print(collect_matchIDs_from_patch(api, read_summoners('summoners.txt'), last_patch_epoch_mil))
    

if __name__ == "__main__":
    main()
