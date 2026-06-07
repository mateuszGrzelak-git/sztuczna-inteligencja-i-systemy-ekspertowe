from collections import deque
from typing import Dict

import matplotlib as plt
import csv
import numpy as np
from math import floor
from pathlib import Path
import os

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

"""
hamming - kafelki znajdujące się nie na swoich pozycjach
manhattan - suma ruchow kafelkow ktore wymagane sa by byly na swoich pozycjach
"""
countOfRows = 0
countOfColumns = 0

indexForRows = 0
indexForColumns = 1
startPos = 0

stepsForGoal = 0
stepsDirections = ""
directions = "LRUD"

def isSolvable(zadanie):
    zadanieCopy = zadanie.copy()
    rowFromBottomOf0 = 0
    isEven = countOfColumns % 2 == 0
    if isEven:
        indexOf0 = zadanieCopy.index(0)
        columnAndRowOf0 = getColumnAndRowFromIndex(indexOf0)
        rowOf0 = columnAndRowOf0[0]
        rowFromBottomOf0 = countOfRows - rowOf0
    zadanieCopy.remove(0)
    inwersja = 0
    for x in range(len(zadanieCopy)):
        for y in range(x+1, len(zadanieCopy)):
#            if x == zadanie[0]:
#                break
            if zadanieCopy[x] > zadanieCopy[y]:
                inwersja += 1
    if isEven:
        if (rowFromBottomOf0 + inwersja) % 2 == 1:
            return True
        return False
    if inwersja % 2 == 0:
        return True
    return False

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

def executeProgramForDirectory(directoryPath, glebokoscAlgorytmu, wybranyAlgorytm):
    path = Path(os.getcwd()) / directoryPath
    list = []
    global stepsDirections
    global stepsForGoal
    for filename in path.glob("*.txt"):
        zadanie = readFile(filename)
        if not isSolvable(zadanie):
            printResult(filename.name)
        elif wybranyAlgorytm == 1:
            stepsDirections = ""
            stepsForGoal = 0
            result = bfs(zadanie, glebokoscAlgorytmu)
            printResult(filename.name)
        elif wybranyAlgorytm == 2:
            stepsDirections = ""
            stepsForGoal = 0
            result = dfs(zadanie, glebokoscAlgorytmu)
            printResult(filename.name)
        elif wybranyAlgorytm == 3:
            stepsDirections = ""
            stepsForGoal = 0
            aStar(zadanie, startPos, 1)
        elif wybranyAlgorytm == 4:
            stepsDirections = ""
            stepsForGoal = 0
            aStar(zadanie, startPos, 2)
        else:
            print("Wpisano niepoprawny numer algorytmu, proszę spróbować ponownie")
            main()

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
            if direction == 'U' and row-1 >= 0:
                tmp = puzzleResult[index]
                puzzleResult[index] = puzzleResult[upBlock]
                puzzleResult[upBlock] = tmp
            elif direction == 'L' and column-1 >= 0:
                tmp = puzzleResult[index]
                puzzleResult[index] = puzzleResult[leftBlock]
                puzzleResult[leftBlock] = tmp
            elif direction == 'R' and (column + 1) < countOfColumns:
                tmp = puzzleResult[index]
                puzzleResult[index] = puzzleResult[rightBlock]
                puzzleResult[rightBlock] = tmp
            elif direction == 'D' and (row+1) < countOfRows:
                tmp = puzzleResult[index]
                puzzleResult[index] = puzzleResult[downBlock]
                puzzleResult[downBlock] = tmp
            else:
                return 0
        index += 1
    return tuple(puzzleResult)

#manhattan - suma ruchow kafelkow ktore wymagane sa by byly na swoich pozycjach
def manhattan(state):
    index = 0
    ruchyKafelkow = 0
    for x in range(countOfColumns):
        for y in range(countOfRows):
            if state[index] != (index+1) % (countOfColumns * countOfRows):
                if state[index] != 0:
                    goalPositionOfWrongBlock = getColumnAndRowFromIndex(state[index]-1)
                    currentPositionOfWrongBlock = getColumnAndRowFromIndex(index)
                    columnCost = abs(currentPositionOfWrongBlock[0] - goalPositionOfWrongBlock[0])
                    rowCost = abs(currentPositionOfWrongBlock[1] - goalPositionOfWrongBlock[1])
                    costOfWrongBlock = columnCost + rowCost
                    ruchyKafelkow += costOfWrongBlock
            index += 1
    return ruchyKafelkow

def hamming(state):
    index = 0
    missingBlocks = 0
    for x in range(countOfColumns):
        for y in range(countOfRows):
            if state[index] != (index+1) % (countOfColumns * countOfRows):
                if state[index] != 0:
                    missingBlocks += 1
            index += 1
    return missingBlocks

def isGoal(graph):
    index = 0
    for x in range(countOfColumns):
        for y in range(countOfRows):
            if graph[index] != (index+1) % (countOfColumns * countOfRows):
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
def bfs(start, glebokoscAlgorytmu):
    if isGoal(start):
        return start

    # currentStates saves state in queue not a numbers
    currentStates = deque()
    currentStatesWithoutDepthAndDirections = deque()
    visitedStates = []
    global stepsDirections
    global stepsForGoal
    glebokosc = glebokoscAlgorytmu
    currentStates.append((start, stepsDirections, glebokosc))
    currentStatesWithoutDepthAndDirections.append(start)

    while notEmpty(currentStates):
        v, stepDirection, glebokosc = currentStates.popleft()
        currentStatesWithoutDepthAndDirections.popleft()
        # wcześniej v nie było sprawdź czy rozumiesz
        if isGoal(v):
            stepsDirections = stepDirection
            stepsForGoal = len(stepDirection)
            return v
        if glebokosc <= 0:
            #TODO: moze to odkomentowac?
            #stepsDirections = ""
            #stepsForGoal = 0
            continue
        visitedStates.append(v)
        for x in directions:
            potentialNeighbor = neighborsAsState(v, visitedStates, x)
            # czy to nie jest 2 razy?
            if potentialNeighbor != 0 and potentialNeighbor not in visitedStates and potentialNeighbor not in currentStatesWithoutDepthAndDirections:
                currentStates.append((potentialNeighbor, stepDirection + x, glebokosc - 1))
                currentStatesWithoutDepthAndDirections.append(potentialNeighbor)

# szukanie w głąb
def dfs(start, glebokoscAlgorytmu):
    if isGoal(start):
        return start
    
    currentStates = deque()
    currentStatesWithoutDepthAndDirections = deque()
    visitedStates = {}
    global stepsDirections
    global stepsForGoal
    glebokosc = glebokoscAlgorytmu
    currentStates.append((start, stepsDirections, glebokosc))
    currentStatesWithoutDepthAndDirections.append(start)

    while notEmpty(currentStates):
        v, stepDirection, glebokosc = currentStates.pop()
        currentStatesWithoutDepthAndDirections.pop()
        if isGoal(v):
            stepsDirections = stepDirection
            stepsForGoal = len(stepDirection)
            return v
        if glebokosc <= 0:
            continue
        visitedStates.update({tuple(v): glebokosc})
        for x in directions:
            potentialNeighbor = neighborsAsState(v, visitedStates, x)
            # czy to nie jest 2 razy?
            if potentialNeighbor != 0 and potentialNeighbor not in currentStatesWithoutDepthAndDirections:
                if potentialNeighbor in visitedStates:
                    if glebokosc-1 <= visitedStates.get(potentialNeighbor):
                        continue
                visitedStates.update({potentialNeighbor: glebokosc-1})
                currentStates.append((potentialNeighbor, stepDirection + x, glebokosc - 1))
                currentStatesWithoutDepthAndDirections.append(potentialNeighbor)

def popPriorityQueue(queue):
    minimalIndex = 0
    fIndex = 0

    for i in range(1, len(queue)):
        if queue[i][fIndex] < queue[minimalIndex][fIndex]:
            minimalIndex = i
    result = queue[minimalIndex]
    queue.remove(result)
    return result

def aStar(start, glebokoscAlgorytmu, wybor):
    if isGoal(start):
        return start
    currentStatesWithPriority = []
    visitedStates = {}
    #g to jest odwrotnosc glebokosci tzn. glebokoscAlgorytmu - glebokosc
    glebokosc = glebokoscAlgorytmu
    priority = 1
    global stepsDirections
    global stepsForGoal
    currentStatesWithPriority.append((priority, start, 0, stepsDirections))
    while notEmpty(currentStatesWithPriority):
        f, v, g, stepDirection = popPriorityQueue(currentStatesWithPriority)
        if isGoal(v):
            stepsDirections = stepDirection
            stepsForGoal = len(stepDirection)
            return v
        if glebokosc <= 0:
            continue
        visitedStates.update({v: g})
        for direction in directions:
            neighbor = neighborsAsState(v, deque(), direction)
            if neighbor == 0:
                continue
            if visitedStates.get(neighbor) != None:
                if g+1 >= visitedStates.get(neighbor):
                    continue
            newG = g + 1
            #TODO: hamming or manhattan JUST DO IT!!!
            if wybor == 1:
                h = hamming(neighbor)
            elif wybor == 2:
                h = manhattan(neighbor)
            f = h + newG
            #neighbor czy jednak V???
            currentStatesWithPriority.append((f, neighbor, newG, stepDirection + direction))

def printResult(filename):
    dirName = "results"
    os.makedirs(dirName, exist_ok=True)
    filename = "results/result_" + str(filename)
    file = open(filename, "w")
    file.writelines(str(stepsForGoal))
    file.writelines(stepsDirections)

def main():
    print("Wybierz algorytm do wyszukiwania: ")
    print("1) wyszukiwanie wszerz")
    print("2) wyszukiwanie w głąb")
    print("3) wyszukiwanie A*")
    wybranyAlgorytm = int(input("Wybrany algorytm: "))
    if wybranyAlgorytm == 3:
        print("#ybierz metrykę: ")
        print("1) metryka hamminga")
        print("2) metryka manhattan")
        wybranyAlgorytm = int(input("Wybrana metryka: "))+2
    glebokoscAlgorytmu = int(input("Podaj głębokość algorytmu, by określić z jaką precyzją ma wyszukiwać algorytm: "))
    nazwaPliku = input("Podaj nazwę pliku w którym zapisano zadanie: ")
    executeProgramForDirectory(nazwaPliku, glebokoscAlgorytmu, wybranyAlgorytm)

if __name__ == '__main__':
    print_hi('PyCharm')
    main()