# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 15:14:25 2019

@author: Multielio
"""
import random
import numpy as np
import matplotlib.pyplot as mp
from scipy.interpolate import interp1d


defaultItemStartPrice = 50  # Item default price
defaultItemMaxPrice = defaultItemStartPrice*1.5
defaultItemMinPrice = defaultItemStartPrice*0.5
defaultBorder = defaultItemStartPrice*0.1  # Border arround maxprice or minprice where the price will want to go to the opposite direction
defaultVolatility = 0.008 
defaultMaxVol = 0.02  # Set the max volatility to avoid violent price moves


def gen(old_price, volatility):
    rnd = random.random()
    change_percent = 2 * volatility * rnd
    if (change_percent > volatility):
        change_percent -= (2 * volatility)
    change_amount = old_price * change_percent
    return old_price + change_amount

def genNextPrice(oldPrice, volatility, maxprice, minprice,border,maxvol):
    g = gen(oldPrice, volatility)
    rand = random.random()
    while (g > maxprice-border*rand or g < minprice+border*rand):
        rand = random.random()
        if maxvol > volatility:
            volatility += 0.002
        g = gen(oldPrice, volatility)
    volatility = 0.008
    return g	



def genPriceOverTime(numberOfPriceChanges, itemStartPrice, itemMaxPrice, itemMinPrice, border, volatility, maxVol, visualize=False):
    t = np.arange(0,numberOfPriceChanges)
    prices = []
    prices.append(itemStartPrice)
    for j in t[1:] : 
        itemStartPrice = genNextPrice(itemStartPrice,volatility, itemStartPrice +(itemMaxPrice-itemStartPrice)*np.abs(np.sin((1/700)*j)), itemStartPrice -(itemStartPrice-itemMinPrice)*np.abs(np.sin((1/300)*j)),border,maxVol) # here I implemented a way to make maxprice an minprice fluctuate.
        prices.append(itemStartPrice)
    
    continuousPriceOverTime = interp1d(t,prices)  # z is a fonction that takes a integer and return the item price
    
    if visualize:
        mp.plot(np.linspace(0,numberOfPriceChanges-1,numberOfPriceChanges*10),continuousPriceOverTime(np.linspace(0,numberOfPriceChanges-1,numberOfPriceChanges*10)))  # just ploting to look at the curb
    return continuousPriceOverTime

continuousFunctionOfPricesOverTime =genPriceOverTime(700,defaultItemStartPrice,defaultItemMaxPrice,defaultItemMinPrice,defaultBorder,defaultVolatility,defaultMaxVol,visualize=True)

# To evalute price at a given time use: continuousFunctionOfPricesOverTime(float).flat[0]
