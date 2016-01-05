#!/usr/bin/python3

from RiotAPI import RiotAPI
import argparse
import time
import os.path
import sys
import json

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

def partition(lst, n):
    division = len(lst) / float(n)
    return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n) ]

def split_matchIDs(matchIDs, count):
    print("Creating milestone subfiles")
    #OVERWRITES LAST FILE! BE CAREFUL!
    temp = partition(matchIDs,count)
    for i in range(count):
        print("write match_part_"+str(i) + ".txt")
        with open("match_part_"+str(i) + ".txt", 'w') as database:
            for m in temp[i]:
                database.write(str(m) + '\n')
        database.close()

def write_matchInfo(outputFile, matchInfo, part):
    encoder = json.JSONEncoder()
    with open(outputFile, 'w') as database:
            database.write(encoder.encode(matchInfo))
    print("Done writing part " + str(part) + ".")
    print('')
    database.close()
    

def collect_matchInfo(api, matchIDs, part):
    beginTime = time.time()
    lastMessage = time.time()
    progcount = 0
    matchInfo = []
    for mid in matchIDs:
        if time.time() > (lastMessage + 60):
            lastMessage = time.time()
            elapsed = time.time() - beginTime
            print("=====Progress update in part " + str(part) + ":\n"
                + "Running for: " + str(int(elapsed)) + " sec  - "
                + "Progress: " + str(round(100 * progcount / len(matchIDs), 3)) + "% - "
                + "Time remaining: " + str(round((elapsed / (progcount / len(matchIDs))) - elapsed,1)) + " sec")
        matchInfo.append(api.get_match_by_id(mid))
        progcount = progcount + 1
    return matchInfo
    
def main():
    #Usage of the argument: Only give a starting index if an earlier run of the program failed
    parts = 10
    startpart = 0
    #The api key is not hardcoded because it should not be publicly available on github
    api_key = input('Enter API key: ')
    print('')
    api = RiotAPI(api_key)

    #See if the file still needs to be split into milestones and create the if necessary
    #This makes sure if there are any unexpected events, work can be resumed with minimal loss of time.
    recreate = False
    for i in range(parts):
        if not os.path.isfile(os.path.dirname(os.path.abspath(__file__))+"/match_part_"+str(i)+".txt"):
            recreate = True
            break
    if recreate:
        matchIDs = list(read_matchIDs('matches.txt'))
        split_matchIDs(matchIDs,parts)
    else:
        print("Split file already detected")
        print("")
        parser = argparse.ArgumentParser()
        parser.add_argument("startindex", type=int)
        startindex = parser.parse_args().startindex
        if startindex not in range(parts):
            print("Please rerun with a valid starting index")
            exit(0)
        else:
            startpart = startindex


    #Now onto the actual data collection:
    
    for curIndex in range(startpart, parts):
        matches = read_matchIDs("match_part_"+str(curIndex)+".txt")
        temp = collect_matchInfo(api, matches, curIndex)
        print('')
        write_matchInfo("matchInfo_part_" + str(curIndex) + ".json", temp, curIndex)
        #temp = strip_info(temp)
        print("Done with part " + str(curIndex))
        print("Writing it to disk..")
        partname = "matchInfo_part_" + str(curIndex) + ".json"
        os.system("scp "+ partname + " timvandijk@91.121.112.183:" + partname)
        os.remove(os.path.dirname(os.path.abspath(__file__))+"/"+partname)

    print("Cleaning the temporary files")
    for i in range(parts):
        os.remove(os.path.dirname(os.path.abspath(__file__))+"/match_part_"+str(i)+".txt")

if __name__ == "__main__":
    main()
