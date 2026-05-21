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

if __name__ == '__main__':
    print_hi('PyCharm')