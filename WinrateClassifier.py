from RiotAPI import RiotAPI
import math
from random import shuffle

champList = None
versusMatrix = None
synergyMatrix = None

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def nameToId(champName):
    global champList
    for i in range(len(champList)):
        if champList[i][1] == champName:
            return champList[i][0]
    print("Error: couldn't find " + champName + "!")
    return None

def idToIndex(champId):
    global champList
    champId = int(champId)
    for i in range(len(champList)):
        if champList[i][0] == champId:
            return i
    print("Error: couldn't find " + str(champId) + "!")
    return None

def idToName(champId):
    global champList
    champId = int(champId)
    for i in range(len(champList)):
        if champList[i][0] == champId:
            return champList[i][1]
    print("Error: couldn't find " + str(champId) + "!")
    return None

def indexToId(index):
    global champList
    return champList[index][0]

def buildChampList(api):
    #Builds and returns a list of tuples(id, name) of champions
    champData = api.get_all_champions()['data']

    champList = []
    for item in champData.keys():
        champList.append((champData[item]['id'], champData[item]['name']))

    return sorted(champList, key=lambda x: x[0])

def AdjustVersusMatrix(winners, losers):
    global versusMatrix
    global champList

    for winner in winners:
        w = idToIndex(winner)
        for loser in losers:
            l = idToIndex(loser)
            versusMatrix[w][l] = (versusMatrix[w][l][0]+ 1, versusMatrix[w][l][1] + 1)
            versusMatrix[l][w] = (versusMatrix[l][w][0], versusMatrix[l][w][1] + 1)

def AdjustSynergyMatrix(winners, losers):
    global synergyMatrix
    global champList

    for winner in winners:
        w = idToIndex(winner)
        for teammate in winners:
            t = idToIndex(teammate)
            if w != t:
                synergyMatrix[w][t] = (synergyMatrix[w][t][0] + 1, synergyMatrix[w][t][1] + 1)
    for loser in losers:
        l = idToIndex(loser)
        for teammate in losers:
            t = idToIndex(teammate)
            if l != t:
                synergyMatrix[l][t] = (synergyMatrix[l][t][0], synergyMatrix[l][t][1] + 1)

def buildMatrices(matchArray):
    global versusMatrix
    global synergyMatrix

    versusMatrix = [[(1, 2) for x in range(128)] for x in range(128)] #Initialize with 1 win 2 games.
    synergyMatrix = [[(1, 2) for x in range(128)] for x in range(128)] #Initialize with 1 win 2 games.

    matchesProcessed = 0
    k = 0
    while k < len(matchArray):
        l = matchArray[k]
        winner = int(l[0])
        if winner == 0:
            AdjustVersusMatrix(l[1:6], l[6:11])
            AdjustSynergyMatrix(l[1:6], l[6:11])
        else:
            AdjustVersusMatrix(l[6:11], l[1:6])
            AdjustSynergyMatrix(l[6:11], l[1:6])
        matchesProcessed += 1
        k += 1
    print("[+] - Processed " + str(matchesProcessed) + " matches.")

def predict(team1, team2):
    global versusMatrix
    global synergyMatrix
    team1winratescore = 33554432 #2^25
    team1synergyscore = 1048576  #2^20
    team2winratescore = 33554432 #2^25
    team2synergyscore = 1048576  #2^20
    for i in team1:
        a = idToIndex(i)
        for j in team2:
            b = idToIndex(j)
            ratio = float(versusMatrix[a][b][0]) / versusMatrix[a][b][1]
            #print(idToName(i) + " vs " + idToName(j) + " - " + str(ratio) )
            team1winratescore *= ratio
    #print("---------------------")
    for i in team1:
        a = idToIndex(i)
        for j in team1:
            if i != j: 
                b = idToIndex(j)
                ratio = float(synergyMatrix[a][b][0]) / synergyMatrix[a][b][1]
                #print(idToName(i) + " with " + idToName(j) + " - " + str(ratio) )
                team1synergyscore *= ratio 
    #print("---------------------")
    for i in team2:
        a = idToIndex(i)
        for j in team1:
            b = idToIndex(j)
            ratio = float(versusMatrix[a][b][0]) / versusMatrix[a][b][1]
            #print(idToName(i) + " vs " + idToName(j) + " - " + str(ratio) )
            team2winratescore *= ratio
    #print("---------------------")
    for i in team2:
        a = idToIndex(i)
        for j in team2:
            if i != j: 
                b = idToIndex(j)
                ratio = float(synergyMatrix[a][b][0]) / synergyMatrix[a][b][1]
                #print(idToName(i) + " with " + idToName(j) + " - " + str(ratio) ** 0.75)
                team2synergyscore *= ratio

    team1winratescore = math.log(team1winratescore, 2)
    team1synergyscore = math.log(team1synergyscore, 2)
    team2winratescore = math.log(team2winratescore, 2)
    team2synergyscore = math.log(team2synergyscore, 2)
    
    #print("Team 0 winrate score: " + str(team1winratescore))
    #print("Team 0 synergy score: " + str(team1synergyscore))
    #print("Team 1 winrate score: " + str(team2winratescore))
    #print("Team 1 synergy score: " + str(team2synergyscore))
    #print("Prediction: ")
    #print(int(team2winratescore + team2synergyscore > team1winratescore + team1synergyscore))
    #print("Team1 score: " + str(team1winratescore + team1synergyscore))
    #print("Team2 score: " + str(team2winratescore + team2synergyscore))
    return team1winratescore + team1synergyscore, team2winratescore + team2synergyscore

def getMatchData(filename):
    matches = []
    with open(filename, 'r') as f:
        line = f.readline().strip('\n')
        while line:
            l = line.split(' ')
            matches.append(l)
            line = f.readline().strip('\n')
    return matches

def getSlices(dataset, indices, k):
    slices = []
    for i in indices:
        slices += ([x for ind, x in enumerate(dataset) if ind % k == i])
    return slices

def validate(matchArray):
    print("[*] - Testing the classifier...")
    correct = 0
    total = 0
    k = 0
    while k < len(matchArray):
        l = matchArray[k]
        winner = int(l[0])
        team1 = l[1:6]
        team2 = l[6:11]
        out = predict(team1, team2)
        if out[1] <= out[0] and winner == 0:
            correct += 1
        if out[1] > out[0] and winner == 1:
            correct += 1
        total += 1
        k += 1
    return float(correct)/total

def main():
    global champList
    
    api_key = input('[!] - Enter API key: ')
    print("")
    api = RiotAPI(api_key)
    
    filename = 'combined.txt'
    print("[*] - Processing data...")
    champList = buildChampList(api)
    matches = getMatchData(filename)
    shuffle(matches)
    
    k = 10
    allResult = []
    
    kfold = [([x for x  in range(10) if x!= i],[i]) for i in range(10)]
    for item in kfold:
        train = getSlices(matches,item[0],k)
        test = getSlices(matches,item[1],k)
        
        buildMatrices(train)
        print("[+] - Winrate and synergy matrix built!")
        result = validate(test)
        print("[.] Test " + str(item[1][0] + 1) + " result is " + str(result) + ".")
        allResult.append(result)
        
    summ = 0;
    for item in allResult:
        summ += item
    print("[@] " + str(k) + "-fold: " + str(float(summ)/len(allResult)) + " percent correct.")

if __name__ == "__main__":
    main()
