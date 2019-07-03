# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 15:14:25 2019

@author: Multielio
"""
import random
import numpy as np
import matplotlib.pyplot as mp
from scipy.interpolate import interp1d
init = 50 #Item default price
maxprice = init*1.5
minprice = init*0.5
border = init*0.1 #Border arround maxprice or minprice where the price will want to go to the opposite direction
volatility = 0.008 
maxvol = 0.02 # set the max volatility to avoid violent price moves

def gen(old_price):
    rnd = random.random()
    change_percent = 2 * volatility * rnd
    if (change_percent > volatility):
        change_percent -= (2 * volatility)
    change_amount = old_price * change_percent
    return old_price + change_amount

def next_price(old_price, volatility, maxprice, minprice,border,maxvol):
    g = gen(old_price)
    rand = random.random()
    while (g > maxprice-border*rand or g < minprice+border*rand):
        rand = random.random()
        if maxvol>volatility:
            volatility += 0.002
        g = gen(old_price)
    volatility = 0.008
    return g	




time = 700 # Amount of price changes wanted
t = np.arange(0,time)
l = []
l.append(init)
for j in t[1:] : 
    init = next_price(init,volatility, init +(maxprice-init)*np.abs(np.sin((1/700)*j)), init -(init-minprice)*np.abs(np.sin((1/300)*j)),border,maxvol) # here I implemented a way to make maxprice an minprice fluctuate.
    l.append(init)

z = interp1d(t,l) # z is a fonction that takes a integer and return the item price
mp.plot(np.linspace(0,time-1,time*10),z(np.linspace(0,time-1,time*10))) # just ploting to look at the curb