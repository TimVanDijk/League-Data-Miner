import neurolab as nl
import numpy as np
from RiotAPI import RiotAPI

champList = None

def idToIndex(champId):
    global champList
    champId = int(champId)
    for i in range(len(champList)):
        if champList[i][0] == champId:
            return i
    print("Error: couldn't find " + str(champId) + "!")
    return None

#Builds and returns a list of tuples(id, name) of champions
def buildChampList(api):
    champData = api.get_all_champions()['data']
    champList = []
    for item in champData.keys():
        champList.append((champData[item]['id'], champData[item]['name']))

    return sorted(champList, key=lambda x: x[0])

def main():
    global champList
    api_key = input('[!] - Enter API key: ')
    print("")
    api = RiotAPI(api_key)
    champList = buildChampList(api)

    net = nl.net.newff([[0, 1] for x in range(256)], [3, 1]) #Klopt die 3????

    inp = []
    tar = []
    index = 0
    with open('reduced_data.txt', 'r') as f:
        line = f.readline().strip('\n')
        while line:
            l = line.split(' ')
            winner = int(l[0])
            played = [0] * 256
            for champId in l[1:6]:
                played[idToIndex(champId)] = 1
            for champId in l[6:11]:
                played[idToIndex(champId) + 128] = 1
            inp.append(played)
            tar.append([winner])
            index += 1
            line = f.readline().strip('\n')
    
    #Train the neural network
    print("Started training the neural network")
    error = net.train(inp, tar, epochs=100, show=1, goal=0.02)
    print("Finished training the neural network")

    inp = []
    tar = []
    with open('test_data.txt', 'r') as f:
        line = f.readline().strip('\n')
        while line:
            l = line.split(' ')
            winner = int(l[0])
            played = [0] * 256
            for champId in l[1:6]:
                played[idToIndex(champId)] = 1
            for champId in l[6:11]:
                played[idToIndex(champId) + 128] = 1
            inp.append(played)
            tar.append(winner)
            line = f.readline().strip('\n')       

    correct = 0
    total = 0
    out = net.sim(inp)
    for i in range(len(out)):
        if out[i][0] <= 0.5 and tar[i] == 0:
            correct += 1
        if out[i][0] > 0.5 and tar[i] == 1:
            correct += 1
        total += 1
    print("Correct: " + str(correct))
    print("Total: " + str(total))   
    print("Percentage: " + str(float(correct) / total))


if __name__ == "__main__":
    main()