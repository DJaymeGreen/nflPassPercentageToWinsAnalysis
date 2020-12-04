"""
Creates a quiz and answer file for a given csv questionBank and 
another with the possible multiple choice options
This is used to generate quizzing for Geography Now learning

Author: Jayme Green
Date: 1/29/2019
"""

import csv
import matplotlib.pyplot as mpl

colorToDivision = {
    'NFC North' : 'blue',
    'NFC West' : 'cyan',
    'NFC South' : 'purple',
    'NFC East' : 'lime',
    'AFC North' : 'red',
    'AFC West' : 'orange',
    'AFC South' : 'gold',
    'AFC East' : 'pink',
    }

def centroidOfTwoGroups(percentPasses, winPercentage):
    passPercentAboveBelow500 = [0,0]
    winPercentageAboveBelow500 = [0,0]
    teamsAbove500 = 0
    teamsBelow500 = 0
    for x in range(0,len(percentPasses)):
        if float(winPercentage[x]) > .5:
            passPercentAboveBelow500[0] += float(percentPasses[x])
            winPercentageAboveBelow500[0] += float(winPercentage[x])
            teamsAbove500 += 1
        else:
            passPercentAboveBelow500[1] += float(percentPasses[x])
            winPercentageAboveBelow500[1] += float(winPercentage[x])
            teamsBelow500 += 1

    passPercentAboveBelow500 = passPercentAboveBelow500[0] / teamsAbove500, passPercentAboveBelow500[1] /teamsBelow500
    winPercentageAboveBelow500 = winPercentageAboveBelow500[0] / teamsAbove500, winPercentageAboveBelow500[1] /teamsBelow500
    return passPercentAboveBelow500, winPercentageAboveBelow500

def insertionSort(arr): 
    for i in range(1, len(arr)): 
        key = arr[i] 
        j = i-1
        while j >=0 and key[4] > arr[j][4] : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key 

def writeDataToTextFile(teamData):
    output = open("output", "w")
    output.write("Team \t  Passing Yds/G \t Pass% \t Average Opponent Passing Yds/G \t Passing Yds/G + Avg Opp Passing Yds/G \n")
    for team in teamData:
        for datapoint in team:
            output.write(str(datapoint) +"\t")
        output.write("\n")

def toCSVFile(teamData):
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Team','Passing Yds/G','Pass%','Average Opponent Passing Yds/G','Passing Yds/G + Avg Opponent Passing Yds/G'])
        for team in teamData:
            writer.writerow(team)

def printData(dataToGraph):
    teamData = list()
    for team in range(0,len(dataToGraph[0])):
        teamData.append(list())
        for dataList in dataToGraph:
            teamData[team].append(dataList[team])
        teamData[team].append(dataToGraph[1][team] + dataToGraph[3][team])
    insertionSort(teamData)
    print(teamData)
    toCSVFile(teamData)


"""
Makes a scatter plot graph of X vs. Y
"""
def makeGraph(listOfX, listOfY, xAxisName, yAxisName, titleOfGraph):
    mpl.scatter(listOfX, listOfY, s=100)

    mpl.xlabel(xAxisName)
    mpl.ylabel(yAxisName)
    mpl.title(titleOfGraph)
    mpl.show()


def calculateAverageOpponentPassing(dataToGraph, futureOpponents, teamToOpponentPassingYdsPerGame):
    for team in range(0, len(dataToGraph[0])):
        averageOpponentPassing = 0
        for opponent in futureOpponents[team]:
            if opponent != "Bye":
                averageOpponentPassing += teamToOpponentPassingYdsPerGame.get(opponent)
        dataToGraph[3].append(averageOpponentPassing/4)
    return dataToGraph

"""
Reads a csv file containing all of the questions/answers that can 
be on the quiz
"""
def openCSVFile(fileName):
    dataToGraph = [[] for i in range(4)]
    futureOpponents = list()
    teamToOpponentPassingYdsPerGame = dict()
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        colNum = len(next(reader))
        for row in reader:
            teamToOpponentPassingYdsPerGame[row[0]] = float(row[1])
            futureOpponents.append(list())
            for val in range(0,colNum):
                if val == 0:
                    dataToGraph[0].append(row[val])
                elif val == 2:
                    dataToGraph[1].append(float(row[val]))
                elif val == 3:
                    dataToGraph[2].append(float(row[val]))
                elif val > 3:
                    futureOpponents[len(futureOpponents)-1].append(row[val])
    return dataToGraph, teamToOpponentPassingYdsPerGame, futureOpponents


def main(fileName):
    dataToGraph, teamToOpponentPassingYdsPerGame, futureOpponents = openCSVFile(fileName)
    dataToGraph = calculateAverageOpponentPassing(dataToGraph, futureOpponents, teamToOpponentPassingYdsPerGame)
    makeGraph(dataToGraph[3], dataToGraph[1], 'Opponent Yds/G', 'Offensive Passing Yds/G', 'Next 4 Opponent Yds/G vs. Offensive Passing Yds/G')
    makeGraph(dataToGraph[3], dataToGraph[2], 'Opponent Yds/G', 'Percentage of Passing Plays', 'Next 4 Opponent Yds/G vs. Passing Play Percentage')
    printData(dataToGraph)


main('passingPredictionForNextFourGames.csv')