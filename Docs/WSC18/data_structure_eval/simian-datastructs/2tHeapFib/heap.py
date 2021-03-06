import fibonacci_heap_mod

# each LP has a Fibonacci Heap  and each
#  Rank (Simian Engine) has a fib heap 

tierDict = {}
infTime = 0

class tier2():
    def __init__(self,key):
        self.key = key
        self.arr = fibonacci_heap_mod.Fibonacci_heap()
        
    def push(self, item):
        self.arr.enqueue(item,item[0])
        self.key = self.arr.min().m_priority
        
    def pop(self):
        e = self.arr.dequeue_min().m_elem
        if len(self.arr):
            self.key = self.arr.min().m_priority # update key
        else:
            self.key = infTime
        return e
    
    def peak(self):
        return self.arr.min().m_elem
    
    def size(self):
        return len(self.arr)

    def annihilate(self, event):
        ret = False
        otherEvents = []
        if event["antimessage"]:
            event["antimessage"] = False
        else:
            event["antimessage"] = True
        while self.isEvent() and self.peak()[0] <= event["time"] :
            poppedEvent = self.pop()
            if poppedEvent[1] == event:
                ret = True
                break
            else:
                otherEvents.append(poppedEvent)
        if ret == False:
            if event["antimessage"]:
                event["antimessage"] = False
            else:
                event["antimessage"] = True
        for x in otherEvents:
            self.push(x)
        return ret
    
    def isEvent(self):
        try:
            return self.arr.min()
        except IndexError:
            return False

    def __cmp__(self, o):
        return cmp(self.key, o.key)

## tier 1 
    
def init(engine):
    tier1 = fibonacci_heap_mod.Fibonacci_heap()
    global infTime
    infTime = int(engine.infTime) + 1
    #for e in engine.entities:
    #    for x in engine.entities[e]:
    #        tier = tier2(infTime)
    #        tierDict[(e,x)] = tier1.enqueue(tier,tier.key)
    return tier1

def push(arr, element):
    try:
        t = tierDict[(element[1]['rx'],element[1]['rxId'])] # tier2 obj
    except:
        newTier = tier2(infTime)
        tierDict[(element[1]['rx'],element[1]['rxId'])] = arr.enqueue(newTier,newTier.key)
        #tierDict[(element[1]['rx'],element[1]['rxId'])] = tier1
        t = tierDict[(element[1]['rx'],element[1]['rxId'])]
        
    t.m_elem.push(element)
    if t.m_priority > t.m_elem.key: # the new element has a smaller timestamp
        arr.decrease_key(t,t.m_elem.key)
    
def pop(arr):
    tier = arr.dequeue_min()
    e = tier.m_elem.pop()
    tierDict[(e[1]['rx'],e[1]['rxId'])] = arr.enqueue(tier.m_elem,tier.m_elem.key)    
    return e

def annihilate(arr, event):
    t = tierDict[(event['rx'],event['rxId'])] # time,q
    ret = t.m_elem.annihilate(event)
    #heapq.heapify(arr)
    if t.m_elem.key > t.m_priority:
        # decrease key to -inf, remove element, add with new priority
        arr.decrease_key(t,-1)
        e = arr.dequeue_min().m_elem
        tierDict[(event['rx'],event['rxId'])] = arr.enqueue(e,e.key)
    else:
        arr.decrease_key(t,t.m_elem.key)
    return ret

def peak(arr):
    return arr.min().m_elem.peak()

def isEvent(arr):
    return arr.min().m_elem.isEvent()

def size(arr):
    ## TODO
    numEvents = 0
    for heap in arr:
        numEvents += heap.size()
    return numEvents
