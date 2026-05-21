from collections import deque
import matplotlib as plt
import csv

#True == success
#False == failure

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

def main():
    print("Wybierz algorytm do wyszukiwania: ")
    print("1) wyszukiwanie wszerz")
    print("2) wyszukiwanie w głąb")
    print("3) wyszukiwanie A*")
    wybranyAlgorytm = int(input("Wybrany algorytm: "))
    glebokoscAlgorytmu = int(input("Podaj głębokość algorytmu, by określić z jaką precyzją ma wyszukiwać algorytm: "))

    if wybranyAlgorytm == 1:
        bfs()
    elif wybranyAlgorytm == 2:
        dfs()
    elif wybranyAlgorytm == 3:
        aStar()
    else:
        print("Wpisano niepoprawny numer algorytmu")
        main()


if __name__ == '__main__':
    print_hi('PyCharm')
    main()