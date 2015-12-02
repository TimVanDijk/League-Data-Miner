from RiotAPI import RiotAPI
import argparse
import time
import sqlite3

def store_results(results):
    conn = sqlite3.connect('summoners.db')
    for s in results:
        query = "INSERT INTO summoners(id, name) VALUES (" + str(s[0]) + ", " + str(s[1].encode('ascii', 'replace')) + ")"
        conn.execute(query)
    conn.commit()
    cursor = conn.execute("SELECT id, name FROM summoners")
    for row in cursor:
       print("ID = ", row[0])
       print("NAME = ", row[1])
    conn.close()

def collect_summoner_ids(api, beginId):
    matchHistory = api.get_matchlist_by_summonerid(beginId)
    #Grab the 3 most recent matches played from the match history
    if matchHistory == None:
        return []
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
    api_key = raw_input('Enter API key: ')
    print('')
    api = RiotAPI(api_key)

    closedList = []
    
    #Get a summonerid from a summoner that is known to exist e.g. by using your own nickname
    summoner = api.get_summoner_by_name('timinat0r')['timinat0r']
    openList = []
    tup = (summoner['id'], summoner['name'])
    openList.append(tup)

    #Counts the current iteration
    i = 0
    startTime = time.time()
    while len(closedList) + len(openList) < amount:
        i += 1
        #Print info on the progress
        print("Iteration: " + str(i) + " - IDs found: " + str(len(openList)\
         + len(closedList)) + " - Current player: " + str(openList[0][1].encode('ascii', 'replace')))
        
        #Take the first element from the openList as the next summoner
        currentPlayer = openList[0]
        results = collect_summoner_ids(api, currentPlayer[0])
        results = list(set(results))

        #To prevent index out of bounds errors
        if len(openList) > 1:
            openList = openList[1:]
        else:
            openList = []

        #Add all NEW summoners we found to the open list
        for result in results:
            if result not in openList and result not in closedList and result != currentPlayer:
                openList.append(result)
        #Add the summoner we just checked to the closed list
        closedList.append(currentPlayer)
        #Remove duplicates in the open list (I think this might be redundant)
        openList = list(set(openList))

    #Combine the summoners from the open and closed lists to form a list of all discovered summoners
    #set() might also be redundant here, but I really dont feel like thinking about that now
    summonerList = set(closedList + openList)
    endTime = time.time()

    print("\nCollected " + str(len(summonerList)) + " IDs in " + str(endTime - startTime) + " seconds")
    
    #Store the list of summoners in a file
    with open('summoners.txt', 'a') as database:
        for s in summonerList:
                #Some people have unicode characters in their name. str() throws an error on those,
                 #therefore we must convert all unicode characters to ? before we can cast them to a string
            database.write(str(s[0]) + ' ' + str(s[1].encode('ascii', 'replace')) + '\n')

if __name__ == "__main__":
    main()
