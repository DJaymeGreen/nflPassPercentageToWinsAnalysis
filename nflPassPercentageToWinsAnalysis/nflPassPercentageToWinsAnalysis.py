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

"""
Makes a scatter plot graph of X vs. Y
"""
def makeGraph(listOfX, listOfY, listOfColor, xAxisName, yAxisName, titleOfGraph):
    colors = list(map(lambda x: colorToDivision.get(x), listOfColor))
    centroidPassAboveBelow500, centroidWinPercentAboveBelow500 = centroidOfTwoGroups(listOfX, listOfY)
    mpl.scatter(listOfX, listOfY, s=100, c=colors)
    mpl.plot(centroidPassAboveBelow500[0],centroidWinPercentAboveBelow500[0], marker='x', ms=15,  mew=2)
    mpl.plot(centroidPassAboveBelow500[1],centroidWinPercentAboveBelow500[1], marker='x', ms=15, mew=2)

    #mpl.plot(listOfX, listOfY, 'ro')
    mpl.xlabel(xAxisName)
    mpl.ylabel(yAxisName)
    mpl.title(titleOfGraph)
    mpl.axhline(y=0.5)
    mpl.show()

    #mpl.savefig('nflPassingPercentVsWinPercent.png')

"""
Reads a csv file containing all of the questions/answers that can 
be on the quiz
"""
def openCSVFile(fileName, columnWithXData, columnWithYData, columnWithColorData):
    dataToGraph = [[] for i in range(3)]
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        colNum = len(next(reader))
        for row in reader:
            for val in range(0,colNum):
                if val == columnWithXData:
                    dataToGraph[0].append(row[val])
                elif val == columnWithYData:
                    dataToGraph[1].append(row[val])
                elif val == columnWithColorData:
                    dataToGraph[2].append(row[val])
    return dataToGraph


def main(fileName):
    columnWithXData = 6
    columnWithYData = 11
    columnWithColorData = 7
    dataToGraph = openCSVFile(fileName, columnWithXData, columnWithYData, columnWithColorData)
    makeGraph(dataToGraph[0], dataToGraph[1], dataToGraph[2], 'Percentage of Passing Plays', 'Win Percentage', 'Win Percentage vs. Passing Play Percentage')


main('nflPassingPercentageAndWins.csv')