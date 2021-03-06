'''
This file contains the wrappers for the Calendar Queue
to be made compatible with SimianPie

Author: Christopher Hannon
Email_primary: channon@lanl.gov
Email_secondary: channon@iit.edu
Date: July 12, 2017

'''

import calendarQ

####                   ####
#                         #
##  Wrappers for Simian  ##
#                         #
####                   ####

MAXTIME = 1

def init(engine):
    global MAXTIME
    #MAXTIME = engine.endTime+10
    MAXTIME=1000000000
    return calendarQ.CalendarQ(MAXTIME)

def size(arr):
    return arr.size

def peak(arr):
    x = arr.c_min()
    #print x
    if x:
        return arr.c_min().data
    else:
        return None
    
def push(Q, item):    
    Q.enqueue(calendarQ.Element(float(item[0]),item))

def pop(Q):
    e = Q.dequeue_min()
    return (e.data)

def annihilate(arr, event):
    ret = False
    if event["antimessage"]:
        event["antimessage"] = False
    else:
        event["antimessage"] = True


    annih = calendarQ.Element(event['time'],(event['time'],event))
    ret = arr.annihilate(annih)    

    if ret == False:
        if event["antimessage"]:
            event["antimessage"] = False
        else:
            event["antimessage"] = True
    return ret
    
def isEvent(arr):
    return arr.size

def printCalinfo(arr):
    arr.printCalinfo()
    
