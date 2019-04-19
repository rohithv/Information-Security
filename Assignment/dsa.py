#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 21:26:09 2019

@author: rohith
"""

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random

def sha(msg):
    '''create a SHA hash of the given message '''
    h=SHA.new(msg)
    return h.digest()

def sign(key, msg):
    ''' Sign the given message and return message '''
    h=sha(msg)
    sgn = key.decrypt(h) #using private key
    return (msg, sgn)

def verify(key, sign):
    ''' Verify the validity of the signature'''
    msg=sign[0]
    sgn=sign[1]
    h=sha(msg)
    h_ = key.encrypt(sgn, 1024) #using public key
    h_ = h_[0]
    return h == h_ #checking the equality

random_generator = Random.new().read
key = RSA.generate(1024, random_generator) #generate pub and priv key

message = b'message'

tosend = sign(key, message)
print("(message, sign) pair is:")
print(tosend)

received = tosend #message sending is simulated like this

check = verify(key, received)
print("Result of verification:")
print(check)