from RiotAPI import RiotAPI
import math
global winLoss
from random import shuffle


champList = None

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

def getMatches(matchArray):
    global winLoss
    winLoss = [(1, 1) for x in range(128)]
    
    matchesProcessed = 0
    k = 0
    while k < len(matchArray):
        l = matchArray[k]
        winner = int(l[0])
        if winner == 0:
            for i in l[1:6]:
                a = idToIndex(int(i))
                #winLoss[a][0] += 1
                winLoss[a] = (winLoss[a][0]+1,winLoss[a][1])
            for i in l[6:11]:
                a = idToIndex(int(i))
                #winLoss[a][1] += 1
                winLoss[a] = (winLoss[a][0],winLoss[a][1]+1)
        else:
            for i in l[1:6]:
                a = idToIndex(int(i))
                #winLoss[a][1] += 1
                winLoss[a] = (winLoss[a][0]+1,winLoss[a][1]+1)
            for i in l[6:11]:
                a = idToIndex(int(i))
                #winLoss[a][0] += 1
                winLoss[a] = (winLoss[a][0]+1,winLoss[a][1])
        k += 1
        matchesProcessed += 1
    print("[+] - Processed " + str(matchesProcessed) + " matches.")
    
def getMatchData(filename):
    matches = []
    with open(filename, 'r') as f:
        line = f.readline().strip('\n')
        while line:
            l = line.split(' ')
            matches.append(l)
            line = f.readline().strip('\n')
    return matches

def predict(team1, team2):
    global winLoss
    
    win = 0
    loss = 0
    for item in winLoss:
        win += item[0]
        loss += item[1]
    total = win + loss
    probwin = float(win)/total
    probloss = float(loss)/total
    
    probchampions = 1
    for champ1 in team1:
        tup = winLoss[idToIndex(champ1)]
        sumo = tup[0]+tup[1]
        probchampions *= float(sumo)/total
    for champ1 in team2:
        tup = winLoss[idToIndex(champ1)]
        sumo = tup[0]+tup[1]
        probchampions *= float(sumo)/total

    team1winconditionals = 1
    team1lossconditionals = 1
    
    for champ1 in team1:
        tup = winLoss[idToIndex(champ1)]
        sumo = tup[0]+tup[1]
        team1winconditionals *= float(tup[0])/probwin
        team1lossconditionals *= float(tup[1])/probloss
    for champ1 in team2:
        tup = winLoss[idToIndex(champ1)]
        sumo = tup[0]+tup[1]
        team1winconditionals *= float(tup[1])/probloss
        team1lossconditionals *= float(tup[0])/probwin
        
    prob1win = (float(team1winconditionals)*probwin)/probchampions
    prob1loss = (float(team1lossconditionals)*probloss)/probchampions
    out = (prob1win,prob1loss)
    return out;

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
    champList = buildChampList(api)
    print("[*] - Processing data...")
    matches = getMatchData(filename)
    shuffle(matches)
    k = 10
    allResult = []
    
    kfold = [([x for x  in range(10) if x!= i],[i]) for i in range(10)]
    for item in kfold:
        train = getSlices(matches,item[0],k)
        test = getSlices(matches,item[1],k)
        
        getMatches(train)
        result = validate(test)
        print("[.] Test " + str(item[1][0] + 1) + " result is " + str(result) + ".")
        allResult.append(result)
        
    summ = 0;
    for item in allResult:
        summ += item
    print("[@] " + str(k) + "-fold: " + str(float(summ)/len(allResult)) + " percent correct.")
    
    

if __name__ == "__main__":
    main()
