'''
This file contains the implementation for a CalendarQ in pure Python

Author: Christopher Hannon
Email_primary: channon@lanl.gov
Email_secondary: channon@iit.edu
Date: July 12, 2017
'''

###                                                      ###
#   CalendarQ contains Buckets, Buckets contain Elements   #
###                                                      ###
'''
CalendarQ              
                       Bucket
  ##          ------------------------
 ####         | ####        #### - Element
 #  #   --->  | #  #  <==>  #  #   
 ####         | ####        ####
  ##          ------------------------
  ##
  ##          ------------------------
 ####         | ####        ####  
 #  #   --->  | #  #  <==>  #  #   o o o
 ####         | ####        ####
  ##          ------------------------
  ##
  ##          ------------------------
 ####         | ####        ####
 #  #   --->  | #  #  <==>  #  #   o o o 
 ####         | ####        ####
  ##          ------------------------

'''

heuristicWidthMultiplier = 3
import copy 

class CalendarQ():
    '''
    This class creates a calendar Q see Randy Browns Paper:
    Calendar Queues: A Fast O(1) Priority Queue Implemenation
    for the Simulation Event Set Problem
    '''
    ##                     ##
    # Hashed Data Structure #
    ##                     ##
    def __init__(self, maxtime):
        #self.yearSize   = 1
        self.numBuckets = 2
        self.dayLength  = 0.5
        self.buckets    = []
        for x in range(self.numBuckets):
            self.buckets.append(Bucket())
        self.size       = 0   # numElements
        self.currTime   = 0   # min event time in q AKA startpriority
        # currTime is updated upon enqueue but not on dequeue
        self.eventRate  = [.03 for x in range(32)]
        self.eventRateIndex = 0
        self.prevEventTime = 0
        self.MAXTIME = maxtime

        #self.printCalinfo()
        
    def printCalinfo(self):
        print("numBuckets: %s dayLength: %s size: %s currTime: %s" %
              (self.numBuckets, self.dayLength, self.size, self.currTime))
        print('BucketInfo:')
        for bucket in self.buckets:
            print(' ')
            x = bucket.firstElement
            while x:
                print(x.data)
                x = x.n

    def __print__(self):
        self.printCalcinfo()
        
    def enqueue(self,element):
        self.size += 1
        #print('curTime: %s el time: %s '% (self.currTime,element.time))
        if element.time < self.currTime:
            self.currTime = element.time
            #print('curTime Shrinking')
        # grow queue
        if self.size > 2 * self.numBuckets:
            self.resize(2 * self.numBuckets)
        
        self.insert(element)
        #self.printCalinfo()

    def dequeue_min(self):

        #self.printCalinfo()
        

        event = self.remove()
        self.currTime = event.time
        
        ## running average of EventRate ##
        self.eventRateIndex = (self.eventRateIndex + 1) % len(self.eventRate)
        self.eventRate[self.eventRateIndex] = (event.time - self.prevEventTime)
        self.prevEventTime = event.time

        # shrink queue
        self.size -=1
        if self.size < 0.5 * self.numBuckets:
            self.resize(int(0.5 * self.numBuckets))
            
            
        # return event
        return event # Element object
            
    def c_min(self):
        #self.printCalinfo()
        x = self.buckets[self.getBucketIndex(self.findNextSmallest())].firstElement
        return x
    
    def annihilate(self, element):
        index = self.getBucketIndex(element.time)
        el = self.buckets[index].firstElement
        while el:
            if el.time <= element.time:
                if el == element:
                    self.size -= 1
                    self.buckets[index].removeElement()
                    #print('annhihating')
                    return True
            el = el.n
        #print('not annihilating')
        return False
    
    def resize(self,newSize):
        #oldYearSize  = self.yearSize
        #oldNumBuckets = self.numBuckets
        if not newSize:
            return
        self.numBuckets = newSize

        allEvents = []
        for bucket in self.buckets:
            x = bucket.firstElement
            while x:
                allEvents.append(x)
                x = x.n
        
        self.dayLength = heuristicWidthMultiplier *  max(sum(self.eventRate)/len(self.eventRate),0.000000001)
        #print self.dayLength
        
        self.buckets = []

        #print('look here: v')
        #self.printCalinfo()

        for x in range(newSize):
            self.buckets.append(Bucket())
        for e in allEvents:
                self.insert(e)
                
    def insert(self,e):
        e.n = None
        e.p = None
        bucketIndex = self.getBucketIndex(e.time)
        self.buckets[bucketIndex].addElement(e)

    def remove(self):
        #self.findNextSmallest()
        index = self.getBucketIndex(self.findNextSmallest())
        #self.size -= 1
        return self.buckets[index].removeElement()
    
   
    def findNextSmallest(self):
        # returns the time of the next smallest event
      
        # self.currTime may be a valid event (from enqueue) or be the last removed time (dequeue)
        # use the min event time to find the next smallest eventTime
        # updates the q variable

        #find upper bound on year
        # look at index of currTime
        # find next event within a year of currTime

        # if not then find min of all buckets

        index = self.getBucketIndex(self.currTime)
        yearLength  = self.dayLength * self.numBuckets
        bottomIndex = int(float(self.currTime) / float(self.dayLength)) # this is required because of if 0.086 time with day lenght 0.005 the year should end at 0.085 + yearLength ranther than 6
        newCurrTime = float(bottomIndex) * float(self.dayLength)
        year = yearLength + newCurrTime 
        
        startingIndex = index
        while True:
            buck = self.buckets[index].firstElement
            if buck and buck.time < year:
                # element is within year, return this time
                time = buck.time
                self.currTime = time
                return time
            index = (index +1) % self.numBuckets
            if index == startingIndex:
                # need to find min of all buckets
                time = self.MAXTIME
                for bucket in self.buckets:
                    if bucket.firstElement:
                        time = min(time,bucket.firstElement.time)
                self.currTime = time
                return time
                
    def getBucketIndex(self, time):
        # hash function
        virtualBucketIndex = int(float(time) / float(self.dayLength))
        #print('time: %s index: %s' %(time,virtualBucketIndex))
        return virtualBucketIndex % self.numBuckets
        
class Element():
    ##           ##
    # Linked List #
    ##           ##
    def __init__(self, time, data, n = None, p = None):
        self.time = time
        self.data = data
        self.n    = n
        self.p    = p
        
    def __cmp__(self, other):
        if self.data == other.data:
            return 0
        return 1
        
class Bucket():
    ##                          ##
    #  Bucket contains elements  #
    ##                          ##
    def __init__(self,firstElement = None):
        self.firstElement = firstElement

    def addElement(self,e):
        ##                                 ##
        # Purpose: add element into Bucket  #
        ##                                 ##
        el = self.firstElement
        if el:
            if el.time > e.time: # insert e before el
                self.firstElement = e
                e.n = el
                el.p = e
            else:
                while (el.n): # is next link
                    if (el.n.time > e.time): # 
                        # should look like :
                        #  el <==> e <==> e.n
                        el.n.p = e
                        e.n = el.n
                        el.n = e
                        e.p = el
                        return
                    el = el.n
                # new element is inserted at the end    
                el.n = e
                e.p = el
                return
        else:
            # element is only element in bucket
            self.firstElement = e
            return     

    def removeElement(self):
        ##                                                  ##
        # Purpose: Remove the first Element from the Bucket  #
        ##                                                  ##
        element = self.firstElement
        self.firstElement = self.firstElement.n
        if self.firstElement:
            self.firstElement.p = None
        return element
