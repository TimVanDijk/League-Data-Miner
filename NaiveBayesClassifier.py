from RiotAPI import RiotAPI
import math
global winLoss


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

def getMatches(filename):
    global winLoss
    winLoss = [(1, 1) for x in range(128)]
    
    matchesProcessed = 0
    with open(filename, 'r') as f:
        line = f.readline().strip('\n')
        while line:
            l = line.split(' ')
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
            line = f.readline().strip('\n')
            matchesProcessed += 1
    print("[+] - Processed " + str(matchesProcessed) + " matches.")
    
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

def main():
    global champList
    api_key = input('[!] - Enter API key: ')
    print("")
    api = RiotAPI(api_key)
    filename = 'reduced_data.txt'
    testname = 'test_data.txt'
    champList = buildChampList(api)
    print("[*] - Processing data...")
    getMatches(filename)
    print("[+] - Winrate and synergy matrix built!")
    print("[*] - Testing the classifier...")
    correct = 0
    total = 0
    with open('test_data.txt', 'r') as f:
        line = f.readline().strip('\n')
        while line:
            l = line.split(' ')
            winner = int(l[0])
            team1 = l[1:6]
            team2 = l[6:11]
            out = predict(team1, team2)
            p = out[1] > out[0]
            if p == False and winner == 0:
                correct += 1
            if p == True and winner == 1:
                correct += 1
            total += 1
            line = f.readline().strip('\n')
    print("[+] - Finished testing the classifier")

    print("[*] - Correct: " + str(correct))
    print("[*] - Total: " + str(total))   
    print("[*] - Percentage: " + str(float(correct) / total))

if __name__ == "__main__":
    main()
