#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 10:59:12 2019

@author: rohith
"""
#%%
import math

#%%
nstr = '''
    00:b0:4d:ca:32:df:d2:4d:70:a9:6a:a4:dd:4f:ac:
    28:9a:f9:aa:21:ed:be:11:68:1d:30:41:b3:26:e6:
    35:fe:c5:53:fc:56:64:7b:2d:9c:ec:d5:3f:19:bf:
    4e:39:3d:f6:de:0d:92:a9:69:54:39:7c:ac:18:f8:
    7c:27:c5:1d:40:47:1e:4f:ab:31:ce:f2:04:85:61:
    78:d5:96:84:04:7a:82:25:4b:48:83:da:ae:cc:f5:
    7b:12:58:4f:73:5c:ea:a7:e5:2d:bd:f3:eb:9b:74:
    33:f9:55:d6:44:96:20:9c:1a:dd:48:f5:29:2f:73:
    a6:c2:a8:d9:de:03:aa:2e:11
'''
n = int(nstr.translate({ord(c): None for c in ': \n'}), 16)
e = 0x10001 #65537
#%%
k=int(math.ceil(math.log(n,2))/8) #no of bytes = 128
B = pow(2,8*(k-2))
B2 = B * 2
B3 = B * 3
#%%
#hello
msg = 0x00020c768a0cc690705021079c4a8ab9a70f2360caf114cde6a81421a9d50ea91a15ad215821520d55968ff0afbba6580fb368fa8f87b5e0fc8b6ff9f0b5c3574291a8bf3a8b923e10b47838d1a138c1dd5f7f54867f3489fa48aa94fa65e012424d85c3b9b650ec0a0cebfc35ea9b6c918dfd6af5a1d7e8a55c0068656c6c6f
m0 = m = msg
#%%
#Simulating oracle
oracle=0
def sO(m):
    global oracle
    oracle+=1
    mstr=str(hex(m))
    mstr = mstr[2:].zfill(256) #making it to the length 256
    if mstr[0:4]!="0002":
        return False
    else:
        bytes_seq = [mstr[i:i+2] for i in range(4, 256, 2)]
        try:
            ind = bytes_seq.index('00')
            if ind>=8:
                return True
            else:
                return False
        except:
            return False
    return False

#%%
#Unpads and prints the message
def unpad(m):
    mstr=str(hex(m))
    mstr = mstr[2:].zfill(256) #making it to the length 256
    bytes_seq = [mstr[i:i+2] for i in range(4, 256, 2)]
    ind = bytes_seq.index('00')
    x=bytes.fromhex(mstr[(ind+3)*2:]).decode('utf-8')
    print()
    print(x)
    #for i in bytes_seq[ind+1:]:
    #    print(i.decode("hex"))
    return

#%%
# computes the smallest integer greater than or equal to x/y
def ceil(x,y):
    return x//y + (x%y != 0)

s1 = ceil(n,B3) # this is the starting value for s1
print ("[-] Starting search for s1 (from value %i)" % s1)
i2a = 1          # counter for iterations
while True:
    m1 = (s1 * m0) % n
    if sO(m1):   # call the (simulated) oracle
        break    # padding is correct, we have found s1
    i2a += 1
    s1 += 1      # try next value of s1
print ("[*] Search done in %i iterations" % i2a)
print ("    s1: %i" % s1)
#%%
def floor(x, y):
    return x//y

#%%
#Narrowing interval for round 1
newM = set([])  # collects new intervals
for r in range(ceil((B2*s1 - B3 + 1),n), floor(((B3-1)*s1 - B2),n) + 1):
    aa = ceil(B2 + r*n,s1)
    bb = floor(B3 - 1 + r*n, s1)
    newa = max(B2,aa)
    newb = min(B3-1,bb)
    if newa <= newb:
        newM |= set([ (newa, newb) ])
    print ("Value of r:   %i" % r)

M = newM
newM = set([])
si_1 = s1
#%%
converged = False
gi = 2
while not converged:
    if(len(M)>1): #More than one interval -> linear search on si
        si = si_1 + 1
        while True:
            mi = (si * m0) % n
            if sO(mi):
                break
            si += 1
        #found si here
        
        for (a,b) in M: # for all intervals
            for r in range(ceil((a*si - B3 + 1),n), floor((b*si - B2),n) + 1):
                aa = ceil(B2 + r*n,si)
                bb = floor(B3 - 1 + r*n, si)
                newa = max(a,aa)
                newb = min(b,bb)
                if newa <= newb:
                    newM |= set([ (newa, newb) ])
        
        #got intersection of intervals here
        M.clear()
        M = newM
        newM = set([])
        si_1 = si
        print ("    s_%i:                    %i" % (gi,si))
        gi+=1
        
    elif len(M)==1: #only one interval
        for (a,b) in M:
            if a==b:
                print()
                print("**************************************************")
                print("[*][*] Message found:", a)
                #call a function
                unpad(a)
                converged = True
                break
    
            #binary search
            r = ceil((b*si_1 - B2)*2,n) # starting value for r
            i2c,nr = 0,1    # for statistics
            found = False
            while not found:
                for si in range(ceil((B2 + r * n),b),floor((B3-1 + r * n),a)+1):
                    mi = (si * m0) % n
                    i2c += 1
                    if sO(mi):
                        found = True
                        break # we found si
                if not found:
                    r  += 1   # try next value for r
                    nr += 1
            print ("[*] Search done in %i iterations" % (i2c))
            print ("    explored values of r:  %i" % nr)
            print ("    s_%i:                    %i" % (gi,si))
            gi+=1
            #Found si and r here
            #Narrowing the interval
            aa = ceil(B2 + r*n,si)
            bb = floor(B3 - 1 + r*n, si)
            newa = max(a,aa)
            newb = min(b,bb)
            if newa <= newb:
                newM |= set([ (newa, newb) ])
            else:
                print("Something is wrong")
                break
            
            break
        M.clear()
        M = newM
        newM = set([])
        si_1 = si
        
    else:
        print("Error in length of M ", len(M))
        break
        exit(1)


#%%
print("**************************************************")
print("Total number of oracle access: ",oracle)
#%%