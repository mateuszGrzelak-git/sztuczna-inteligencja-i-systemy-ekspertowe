from collections import deque
import matplotlib as plt
import csv
import numpy as np
from math import floor

"""
Błędy:
- Graph.isGoal()
- Q.not_empty()
- G.neighbors
"""
"""
Sąsiadem nie są liczby obok 0
tylko cała plansza według teorii algorytmów
"""

# True == success
# False == failure

countOfRows = 0
countOfColumns = 0

indexForRows = 0
indexForColumns = 1
startPos = 0

stepsForGoal = 0
stepsDirections = ""
directions = "LRUD"

def listOfStringsToListOfInt(list):
    result = []
    for x in list:
        result.append(int(x))
    return result

# TODO: jeśli można użyć numpy użyj tego
def twoDimensionalListToOne(list):
    return np.concatenate(list)

def twoDimensionalListToOne(list):
    result = []
    for x in list:
        for y in x:
            result.append(y)

    return result

def readFile(path):
    list = []
    file = open(path, 'r')
    lineIndex = 0
    for x in file.readlines():
        # pierwsze użycie strip usuwa entery
        # drugie użycie split usuwa spacje
        x = x.strip()
        x = x.split()
        if lineIndex == 0:
            global countOfRows
            global countOfColumns
            countOfRows = int(x[indexForRows])
            countOfColumns = int(x[indexForColumns])
        else:
            x = listOfStringsToListOfInt(x)
            list.append(x)
        lineIndex += 1

    file.close()

    list = twoDimensionalListToOne(list)
    return list

def getIndexForColumnAndRow(column, row):
    result = 0
    result = countOfColumns * row + column
    return result

def getColumnAndRowFromIndex(index):
    rowAndColumn = []
    row = floor(index / countOfColumns)
    column = index % countOfColumns
    rowAndColumn.append(row)
    rowAndColumn.append(column)
    return rowAndColumn

def neighbors(puzzleList, visitedStates):
    puzzle = tuple(puzzleList)
    neighbors = []
    index = 0
    for x in puzzleList:
        if x == 0:
            rowAndColumn = getColumnAndRowFromIndex(index)
            row = rowAndColumn[0]
            column = rowAndColumn[1]
            upBlock = getIndexForColumnAndRow(column, row - 1)
            rightBlock = getIndexForColumnAndRow(column + 1, row)
            leftBlock = getIndexForColumnAndRow(column - 1, row)
            downBlock = getIndexForColumnAndRow(column, row + 1)
            if row - 1 >= 0:
                neighbors.append(puzzleList[upBlock])
            if column - 1 >= 0:
                neighbors.append(puzzleList[leftBlock])
            if column + 1 <= countOfColumns - 1:
                neighbors.append(puzzleList[rightBlock])
            if row + 1 <= countOfRows - 1:
                neighbors.append(puzzleList[downBlock])
        index += 1

def neighborsAsState(puzzleList, visitedStates, direction):
    puzzle = tuple(puzzleList)
    neighbors = []
    puzzleResult = list(puzzle)
    index = 0
    for x in puzzleList:
        if x == 0:
            rowAndColumn = getColumnAndRowFromIndex(index)
            row = rowAndColumn[0]
            column = rowAndColumn[1]
            upBlock = getIndexForColumnAndRow(column, row - 1)
            rightBlock = getIndexForColumnAndRow(column + 1, row)
            leftBlock = getIndexForColumnAndRow(column - 1, row)
            downBlock = getIndexForColumnAndRow(column, row + 1)
            if direction == 'U':
                tmp = puzzleResult[index]
                puzzleResult[index] = puzzleResult[upBlock]
                puzzleResult[upBlock] = tmp
            if direction == 'L':
                tmp = puzzleResult[index]
                puzzleResult[index] = puzzleResult[leftBlock]
                puzzleResult[leftBlock] = tmp
            if direction == 'R':
                tmp = puzzleResult[index]
                puzzleResult[index] = puzzleResult[rightBlock]
                puzzleResult[rightBlock] = tmp
            if direction == 'D':
                tmp = puzzleResult[index]
                puzzleResult[index] = puzzleResult[downBlock]
                puzzleResult[downBlock] = tmp
        index += 1
    return tuple(puzzleResult)

def isGoal(graph):
    index = 0
    for x in range(countOfColumns):
        for y in range(countOfRows):
            if graph[index] != index:
                return False
            index += 1
    return True

def notEmpty(deque):
    if deque:
        return True
    return False

def print_hi(name):
    print(f'Hi, {name}')

# szukanie wszerz
def bfs(Graph, start):
    if Graph.isGoal():
        return True
    Q = deque()
    T = set()
    # enqueue = append (TYLKO W TYM ALGORYTMIE!!!)
    Q.append(start)

    while Q.not_empty:
        # dequeue = popleft (TYLKO W TYM ALGORYTMIE!!!)
        v = Q.popleft()
        if Graph.isGoal():
            return True
        T.add(v)

        for n in Graph.neighbors(v):
            if n not in T and n not in Q:
                Q.append(n)
    return False

#TODO: implement limit of depth
def bfs(start):
    if isGoal(start):
        return start

    # currentStates saves state in queue not a numbers
    currentStates = deque()
    visitedStates = []
    global stepsDirections
    global stepsForGoal
    currentStates.append((start, stepsDirections))

    while notEmpty(currentStates):
        v, stepDirection = currentStates.popleft()
        # wcześniej v nie było sprawdź czy rozumiesz
        if isGoal(v):
            stepsDirections = stepDirection
            stepsForGoal = len(stepDirection)
            return v
        visitedStates.append(v)
        for x in directions:
            potentialNeighbor = neighborsAsState(v, visitedStates, x)
            # czy to nie jest 2 razy?
            if potentialNeighbor != 0 and potentialNeighbor not in visitedStates and potentialNeighbor not in currentStates:
                currentStates.append((potentialNeighbor, stepDirection + x))

# szukanie w głąb
def dfs():
    print()

def aStar():
    print()

def printResult():
    filename = "result.txt"
    file = open(filename, "w")
    file.writelines(str(stepsForGoal))
    file.writelines(stepsDirections)

def main():
    print("Wybierz algorytm do wyszukiwania: ")
    print("1) wyszukiwanie wszerz")
    print("2) wyszukiwanie w głąb")
    print("3) wyszukiwanie A*")
    wybranyAlgorytm = int(input("Wybrany algorytm: "))
    glebokoscAlgorytmu = int(input("Podaj głębokość algorytmu, by określić z jaką precyzją ma wyszukiwać algorytm: "))
    nazwaPliku = input("Podaj nazwę pliku w którym zapisano zadanie: ")

    zadanie = readFile(nazwaPliku)

    if wybranyAlgorytm == 1:
        result = bfs(zadanie)
        printResult()
    elif wybranyAlgorytm == 2:
        dfs(zadanie, startPos)
    elif wybranyAlgorytm == 3:
        aStar(zadanie, startPos)
    else:
        print("Wpisano niepoprawny numer algorytmu, proszę spróbować ponownie")
        main()

if __name__ == '__main__':
    print_hi('PyCharm')
    main()