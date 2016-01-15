import neurolab as nl
import numpy as np
from RiotAPI import RiotAPI

champList = None

def AdjustVersusMatrix(winners, losers):
    global versusMatrix
    global champList

    for winner in winners:
        w = idToIndex(winner)
        for loser in losers:
            l = idToIndex(loser)
            versusMatrix[w][l] = (versusMatrix[w][l][0]+ 1, versusMatrix[w][l][1] + 1)
            versusMatrix[l][w] = (versusMatrix[l][w][0], versusMatrix[l][w][1] + 1)

def buildMatrices():
    global champList
    global versusMatrix

    print("[*] - Started building winrate matrix")

    versusMatrix = [[(1, 2) for x in range(128)] for x in range(128)] #Initialize with 1 win 2 games.

    matchesProcessed = 0
    with open('reduced_data.txt', 'r') as f:
        line = f.readline().strip('\n')
        while line:
            l = line.split(' ')
            winner = int(l[0])
            if winner == 0:
                AdjustVersusMatrix(l[1:6], l[6:11])
            line = f.readline().strip('\n')
            matchesProcessed += 1
    print("[+] - Processed " + str(matchesProcessed) + " matches.")

def idToIndex(champId):
    global champList
    champId = int(champId)
    for i in range(len(champList)):
        if champList[i][0] == champId:
            return i
    print("[-] - Error: couldn't find " + str(champId) + "!")
    return None

#Builds and returns a list of tuples(id, name) of champions
def buildChampList(api):
    champData = api.get_all_champions()['data']
    champList = []
    for item in champData.keys():
        champList.append((champData[item]['id'], champData[item]['name']))

    return sorted(champList, key=lambda x: x[0])

def trainAndTestNetwork(H):
    global versusMatrix

    #Initialize the neural network
    net = nl.net.newff([[0, 1] for x in range(50)], [H, 1]) #Klopt die 3????

    #Build list containing train set
    print("[*] - Building train set")
    inp = []
    tar = []
    with open('reduced_data.txt', 'r') as f:
        line = f.readline().strip('\n')
        while line:
            l = line.split(' ')
            winner = int(l[0])
            winrates = []
            for i in l[1:6]:
                a = idToIndex(i)
                for j in l[6:11]:
                    b = idToIndex(j)
                    winrates.append(float(versusMatrix[a][b][0]) / versusMatrix[a][b][1])
            for i in l[6:11]:
                a = idToIndex(i)
                for j in l[1:6]:
                    b = idToIndex(j)
                    winrates.append(float(versusMatrix[a][b][0]) / versusMatrix[a][b][1])
            inp.append(winrates)
            tar.append([winner])
            line = f.readline().strip('\n')
    print("[+] - Finished building train set")
    
    #Train the neural network
    print("[*] - Started training the neural network")
    error = net.train(inp, tar, epochs=20, show=1, goal=0.02)
    print("[+] - Finished training the neural network")

    #Build list containing test set
    print("[*] - Building test set")
    inp = []
    tar = []
    with open('test_data.txt', 'r') as f:
        line = f.readline().strip('\n')
        while line:
            l = line.split(' ')
            winner = int(l[0])
            winrates = []
            for i in l[1:6]:
                a = idToIndex(i)
                for j in l[6:11]:
                    b = idToIndex(j)
                    winrates.append(float(versusMatrix[a][b][0]) / versusMatrix[a][b][1])
            for i in l[6:11]:
                a = idToIndex(i)
                for j in l[1:6]:
                    b = idToIndex(j)
                    winrates.append(float(versusMatrix[a][b][0]) / versusMatrix[a][b][1])
            inp.append(winrates)
            tar.append([winner])
            line = f.readline().strip('\n')
    print("Finished building train set")     
    #Do the actual testing
    correct = 0
    total = 0
    out = net.sim(inp)
    for i in range(len(out)):
        if out[i][0] <= 0.5 and tar[i][0] == 0:
            correct += 1
        if out[i][0] > 0.5 and tar[i][0] == 1:
            correct += 1
        total += 1
    print("[+] - Finished testing the classifier")

    print("[*] - Correct: " + str(correct))
    print("[*] - Total: " + str(total))   
    print("[*] - Percentage: " + str(float(correct) / total))

def main():
    global champList
    api_key = input('[!] - Enter API key: ')
    print("")
    api = RiotAPI(api_key)
    champList = buildChampList(api)
    buildMatrices()
    trainAndTestNetwork(3)
    #for i in range(1, 21):
    #    trainAndTestNetwork(i)  


if __name__ == "__main__":
    main()