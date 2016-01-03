#!/usr/bin/python3

import time
import os.path
import sys
import json
from collections import Counter

def getWinner(match):
    win100 = None
    win200 = None
    for team in match['teams']:
        if team['teamId'] == 100:
            win100 = team['winner']
        if team['teamId'] == 200:
            win200 = team['winner']
    return win100, win200

def getParticipants(match):
    champions100 = []
    champions200 = []
    for participant in match['participants']:
        if participant['teamId'] == 100:
            champions100.append(participant['championId'])
        elif participant['teamId'] == 200:
            champions200.append(participant['championId'])
    if len(champions100) != 5 or len(champions200) != 5:
        return None, None

    return sorted(champions100), sorted(champions200)

def getBans(match):
    bans = []
    try:
        for i in range(2):
            for ban in match['teams'][i]['bans']:
                bans.append(ban['championId'])
        return bans
    except Exception:
        return []

def writeMatch(info, results_file):
    for i in range(11):
        results_file.write(str(info[i]))
        if i == 10:
            results_file.write('\n')
        else:
            results_file.write(' ')

def main():
    data_file = open('merged_data.json', 'r')
    reduced_data_file = open('reduced_data.txt', 'a')
    print("[*] Loading data...")
    data = json.load(data_file)
    print("[+] Data loaded.")

    print("[*] Processing data...")
    for match in data:
        if match == None:
            print("[-] Match is None. Ignoring match...")
            continue
        info = 11 * [0]

        winner = getWinner(match)
        if (winner[0] == None or winner[1] == None) or (winner[0] == winner[1]):
            print("[-] No clear winner. Ignoring match...")
            continue
        info[0] = (int(winner[1] == True)) #0 if team 100 wins. 1 if team 200 wins.

        participants = getParticipants(match)
        if participants[0] == None or participants[1] == None:
            print("[-] Not both teams have 5 players. Ignoring match...")
            continue
        for i in range(5):
            info[1+i] = participants[0][i]
        for i in range(5):
            info[6+i] = participants[1][i]
        
        bans = getBans(match)
        for participant in participants[0] + participants[1]:
            if participant in bans:
               print("[-] Banned champion was played anyway. Ignoring match...")
               continue

        writeMatch(info, reduced_data_file)

    data_file.close()
    reduced_data_file.close()
    print("[+] Finished!")
    
if __name__ == "__main__":
    main()