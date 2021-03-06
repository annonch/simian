import heap
from random import randint
import sys
import timeit

REPEATS = 10
NUMBER = 10

# push in increasing
pq = heap.init(None)

def test1():
    for x in range(1000000) :
        heap.push(pq,(x,
                      {"rx" : "a",
                       "tx" : "b",
                       "txID" : 1,
                       "rxID" : 1,
                       "name" : "bob",         
                       "data": "none",
                      }))
        
    #for x in range(1000000) :
    #    y=heap.peak(pq)
    
    for x in range(1000000):
        y = heap.pop(pq)
        #print y
        #print "\n"


def test2():

    for x in range(1000000) :
        heap.push(pq,(randint(0,100000000),
                      {"rx" : "a",
                       "tx" : "b",
                       "txID" : 1,
                       "rxID" : 1,
                       "name" : "bob",         
                       "data": "none",
                      }))
        
    #for x in range(10000) :
    #    y=heap.peak(pq)
        
    for x in range(1000000):
        y = heap.pop(pq)
            #print y          


def test3():
    totalPushes=0
    pushes=0
    while(totalPushes<1000000):
        for x in range(randint(1,100)):
            heap.push(pq,(randint(0,1000000),
                          {"rx" : "a",
                           "tx" : "b",
                           "txID" : 1,
                           "rxID" : 1,
                           "name" : "bob",         
                           "data": "none",
                          }))
            totalPushes+=1
            pushes+=1
        #for x in range(10000) :
        #    y=heap.peak(pq)
        
        for x in range(randint(1,100)):
            if (pushes):
                pushes-=1
                y = heap.pop(pq)
            else:
                break
            #print y          
    while(pushes > 0):
        y=heap.pop(pq)
        pushes-=1
    #print totalPushes

#if test == 1:
print min(timeit.Timer(test1).repeat(repeat=REPEATS, number=NUMBER))/NUMBER     
#if test ==2:
print min(timeit.Timer(test2).repeat(repeat=REPEATS, number=NUMBER))/NUMBER     
print min(timeit.Timer(test3).repeat(repeat=REPEATS, number=NUMBER))/NUMBER     

#test1()
