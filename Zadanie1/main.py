from collections import deque
import matplotlib as plt
import csv

"""
Błędy:
- Graph.isGoal()
- Q.not_empty()
- G.neighbors
"""

#True == success
#False == failure

countOfRows = 0
countOfColumns = 0

indexForRows = 0
indexForColumns = 1
startPos = 0

stepsForGoal = 0
stepsDirections = ""

def readFile(path):
    list = []
    file = open(path, 'r')
    lineIndex = 0
    for x in file.readlines():
        #pierwsze użycie strip usuwa entery
        #drugie użycie split usuwa spacje
        x = x.strip()
        x = x.split()
        if lineIndex == 0:
            countOfRows = int(x[indexForRows])
            countOfColumns = int(x[indexForColumns])
        else:
            list.append(x)
        lineIndex += 1
    
    file.close()
    return list


def print_hi(name):
    print(f'Hi, {name}')

#szukanie wszerz
def bfs (Graph, start):
    if Graph.isGoal():
        return True
    Q = deque()
    T = set()
    #enqueue = append (TYLKO W TYM ALGORYTMIE!!!)
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

#szukanie w głąb
def dfs ():
    print()

def aStar():
    print()

def printResult():
    filename = "result.txt"
    file = open(filename, "w")
    file.writelines(stepsForGoal)
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
        bfs(zadanie, startPos)
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