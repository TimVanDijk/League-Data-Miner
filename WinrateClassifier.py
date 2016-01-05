from RiotAPI import RiotAPI

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

def buildMatrices(api, filename):
    global champList
    global versusMatrix
    global synergyMatrix

    champList = buildChampList(api)

    versusMatrix = [[(1, 2) for x in range(128)] for x in range(128)] #Initialize with 1 win 2 games.
    synergyMatrix = [[(1, 2) for x in range(128)] for x in range(128)] #Initialize with 1 win 2 games.

    matchesProcessed = 0
    with open(filename, 'r') as f:
        line = f.readline().strip('\n')
        while line:
            l = line.split(' ')
            winner = int(l[0])
            if winner == 0:
                AdjustVersusMatrix(l[1:6], l[6:11])
                AdjustSynergyMatrix(l[1:6], l[6:11])
            line = f.readline().strip('\n')
            matchesProcessed += 1
    print("[+] - Processed " + str(matchesProcessed) + " matches.")

def predict(team1, team2, wrWeight, syWeight, power):
    global versusMatrix
    global synergyMatrix
    team1winratescore = 0
    team1synergyscore = 0
    team2winratescore = 0
    team2synergyscore = 0
    for i in team1:
        a = idToIndex(i)
        for j in team2:
            b = idToIndex(j)
            ratio = float(versusMatrix[a][b][0]) / versusMatrix[a][b][1]
            #print(idToName(i) + " vs " + idToName(j) + " - " + str(ratio) )
            team1winratescore += sign(ratio - 0.5) * (abs(0.5 - ratio) ** power)
    #print("---------------------")
    for i in team1:
        a = idToIndex(i)
        for j in team1:
            if i != j: 
                b = idToIndex(j)
                ratio = float(synergyMatrix[a][b][0]) / synergyMatrix[a][b][1]
                #print(idToName(i) + " with " + idToName(j) + " - " + str(ratio) )
                team1synergyscore += sign(ratio - 0.5) * (abs(0.5 - ratio) ** power)
    #print("---------------------")
    for i in team2:
        a = idToIndex(i)
        for j in team1:
            b = idToIndex(j)
            ratio = float(versusMatrix[a][b][0]) / versusMatrix[a][b][1]
            #print(idToName(i) + " vs " + idToName(j) + " - " + str(ratio) )
            team2winratescore += sign(ratio - 0.5) * (abs(0.5 - ratio) ** power)
    #print("---------------------")
    for i in team2:
        a = idToIndex(i)
        for j in team2:
            if i != j: 
                b = idToIndex(j)
                ratio = float(synergyMatrix[a][b][0]) / synergyMatrix[a][b][1]
                #print(idToName(i) + " with " + idToName(j) + " - " + str(ratio) ** 0.75)
                team2synergyscore += sign(ratio - 0.5) * (abs(0.5 - ratio) ** power)

    #print("Team 1 winrate score: " + str(team1winratescore))
    #print("Team 1 synergy score: " + str(team1synergyscore))
    #print("Team 2 winrate score: " + str(team2winratescore))
    #print("Team 2 synergy score: " + str(team2synergyscore))
    return (wrWeight * (team2winratescore / 25.0) + syWeight * (team2synergyscore / 20.0)) > (wrWeight * (team1winratescore / 25.0) + syWeight * (team1synergyscore / 20.0))

def testClassifier(filename, vals):
    print("[*] - Testing classifier...")
    matchesProcessed = 0
    correct = 0
    with open(filename, 'r') as f:
        line = f.readline().strip('\n')
        while line:
            l = line.split(' ')
            winner = int(l[0])
            p = predict(l[1:6], l[6:11], float(vals[0]), float(vals[1]), float(vals[2]))
            if p == winner:
                correct += 1
            line = f.readline().strip('\n')
            matchesProcessed += 1
    print("Correct: " + str(correct))
    print("Total: " + str(matchesProcessed))
    print("Percentage correct: " + str(float(correct) / matchesProcessed))

def main():
    global versusMatrix
    api_key = input('[!] - Enter API key: ')
    print("")
    api = RiotAPI(api_key)
    filename = 'reduced_data.txt'
    testname = 'test_data.txt'
    print("[*] - Processing data...")
    buildMatrices(api, filename)
    print("[+] - Winrate and synergy matrix built!")
    team1 = []
    team2 = []
    while True:
        a = input("Values: ")
        testClassifier(testname, a.split(' '))
    while False:
        for team, color in [(team1, "blue"), (team2, "red")]:
            print("[*] - Enter the names of the five champions in the " + color + " team seperated by commas:")
            line = input(">> ")
            line = line.strip('\n').split(',')
            for champName in line:
                team.append(nameToId(champName.lstrip().rstrip()))

        p = predict(team1, team2)
        if not p:
            print("[+] - Blue team wins.")
        else:
            print("[+] - Red team wins.")

if __name__ == "__main__":
    main()