'''taylor series implementation for logrithms'''

# prereqs for taylor series
#  https://fiziko.bureau42.com/teaching_tidbits/manual_logarithms.pdf

#from __future__ import print_function
import sys
import mersenne_twister as mt
import timeit
import random
import math as c_mod_math

REPEATS = 5
NUMBER = 5

THRESHOLD=50


def pow (base, expo):
    res = 1
    for x in range(expo):
        res *= base
    return res

def factorial(base):
    res = 1
    for x in range(base):
        res *= (base-x)
    return res

## taylor series ##



def ln(x) : # 0 <x <=2
    if x == 0: return 1
    sum = 0
    for n in range(1,THRESHOLD+1):
        sum += (pow(-1, n+1))*(pow(x-1, n)/n)
    return sum

def log(base, val):
    #convert to ln with 0 <= val <= 2
    pass


def get_rand(low, up):
    #if low >= up: raise Exception('bad input')
    return mt.genrand() * (up-low) + low

def c_get_rand(low, up):
    #if low >= up: raise Exception('bad input')
    return random.random() * (up-low) + low

def lc_get_rand(low, up):
    #
    return lc.genrand() * (up-low) + low

def sanity_check():

    assert factorial(10) == 3628800
    assert factorial(4) == 24

    assert pow(2, 10) == 1024
    assert pow(7, 3) == 343
    print (ln(1.0/3.0))
    print (ln(1.0/64.0))

    mt.sgenrand(1234)
    print (mt.genrand())
    print (get_rand(1,5))
    print (get_rand(10,1000))
    #get_rand(2,1)
    
#sanity_check()
    



#####

def test_1():
    '''pure python'''
    for x in range(1000000):
        get_rand(1,10000)
    sys.stdout.write('.')
    #sys.stdout.flush()
    #print('.', end='')    

def test_2():
    '''c module'''
    for x in range(1000000):
        c_get_rand(1,10000)
    sys.stdout.write('.')
    
def test_3():
    '''cache technique'''
    pass

def test_4():
    '''pure python'''
    for x in range(10000):
        ln(get_rand(0,2))
    sys.stdout.write('.')
    #sys.stdout.flush()
    #print('.', end='')    

def test_5():
    '''c module'''
    for x in range(10000):
        c_mod_math.log(c_get_rand(0,2))
    sys.stdout.write('.')
    
def test_6():
    '''cache technique'''
    pass
    
    
print(min(timeit.Timer(test_1).repeat(repeat=REPEATS, number=NUMBER))/NUMBER)
print(min(timeit.Timer(test_2).repeat(repeat=REPEATS, number=NUMBER))/NUMBER)
#print(min(timeit.Timer(test_3).repeat(repeat=REPEATS, number=NUMBER))/NUMBER)
print(min(timeit.Timer(test_4).repeat(repeat=REPEATS, number=NUMBER))/NUMBER)
print(min(timeit.Timer(test_5).repeat(repeat=REPEATS, number=NUMBER))/NUMBER)
#print(min(timeit.Timer(test_6).repeat(repeat=REPEATS, number=NUMBER))/NUMBER)
