#!/usr/bin/python3

from RiotAPI import RiotAPI
import argparse
import time

def save_summoners(summonerList, outputFile):
    #To retrieve the data from the file, split on the first space
    with open(outputFile, 'a') as database:
        for s in summonerList:
            database.write(str(s[0]) + ' ' + str(s[1]) + '\n')

def collect_summoner_ids(api, beginId):
    matchHistory = api.get_matchlist_by_summonerid(beginId)
    #Grab the 3 most recent matches played from the match history
    matches = matchHistory['matches'][:3]
    
    #First we store the match ids from the selected matches and store them in a list
    matchIds = []
    for match in matches:
        matchIds.append(match['matchId'])
    
    #Next we retrieve all data on the matches using the match ids
    summoners = []
    for matchId in matchIds:
        matchInfo = api.get_match_by_id(str(matchId))
        #And extract all the summoner name and id from each participant
        for participant in matchInfo['participantIdentities']:
            summoner = participant['player']
            summoners.append((summoner['summonerId'], summoner['summonerName']))
    #Remove duplicate entries
    summoners = set(summoners)
    
    #return list of tuples (id, name)
    return summoners

def main():
    #TODO: Move code out of main()
    parser = argparse.ArgumentParser()
    parser.add_argument("amount", help="Amount of IDs to collect", type=int)
    amount = parser.parse_args().amount
    #The api key is not hardcoded because it should not be publicly available on github
    api_key = input('Enter API key: ')
    print('')
    api = RiotAPI(api_key)

    #List of all summoners that we have expanded already
    closedList = []
    #List of summoners that have yet to expand
    openList = []

    #Get a summonerid from a summoner that is known to exist e.g. by using your own nickname
    summoner = api.get_summoner_by_name('timinat0r')['timinat0r']

    openList.append((summoner['id'], summoner['name']))

    #Counts the current iteration
    i = 0
    startTime = time.time()
    while len(closedList) + len(openList) < amount:
        i += 1
        #Print info on the progress
        print("Iteration: " + str(i) + " - IDs found: " + str(len(openList)\
         + len(closedList)) + " - Current player: " + openList[0][1])
        
        #Take the first element from the openList as the next summoner
        currentPlayer = openList[0]
        results = collect_summoner_ids(api, currentPlayer[0])
        #Remove duplicates
        results = list(set(results))

        #Remove the selected player from the open list
        openList = openList[1:]

        #Add all NEW summoners we found to the open list
        for result in results:
            if result not in openList and result not in closedList and result != currentPlayer:
                openList.append(result)
        
        #Add the summoner we just expanded to the closed list
        closedList.append(currentPlayer)

    #Combine the summoners from the open and closed lists to form a list of all discovered summoners
    #set() might also be redundant here, but I really dont feel like thinking about that now
    summonerList = set(closedList + openList)
    endTime = time.time()

    print("\nCollected " + str(len(summonerList)) + " IDs in " + str(endTime - startTime) + " seconds")
    
    #Store the list of summoners in a file
    save_summoners(summonerList, 'summoners.txt')

if __name__ == "__main__":
    main()
