# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 15:14:25 2019
@author: Multielio
"""
import random
import numpy as np
import matplotlib.pyplot as mp
from scipy.interpolate import interp1d



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
    prices = [itemStartPrice]
    minPriceBorder = [itemMinPrice]
    maxPriceBorder = [itemMaxPrice]
    currentPrice = itemStartPrice
    for j in t[1:] : 
        dynamicLowBorder = itemStartPrice -(itemStartPrice-itemMinPrice)*np.abs(np.sin((1/300)*j))
        dynamicHighBorder = itemStartPrice +(itemMaxPrice-itemStartPrice)*np.abs(np.sin((1/700)*j))
        currentPrice = genNextPrice(currentPrice, volatility, dynamicHighBorder, dynamicLowBorder, border, maxVol) # here I implemented a way to make maxprice and minprice fluctuate.
        prices.append(currentPrice)
        minPriceBorder.append(dynamicLowBorder)
        maxPriceBorder.append(dynamicHighBorder)
    continuousPriceOverTime = interp1d(t,prices)  
    if visualize:
        continuousLowBorder = interp1d(t,minPriceBorder) 
        continuousHighBorder = interp1d(t,maxPriceBorder) 
        mp.plot(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10), continuousPriceOverTime(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10)))  # just ploting to look at the curb
        mp.plot(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10), continuousLowBorder(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10)))
        mp.plot(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10), continuousHighBorder(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10)))
    return continuousPriceOverTime

def advancedGenPriceOverTime(numberOfPriceChanges, itemStartPrice, itemMaxPrice, itemMinPrice, border, volatility, maxVol, f1, f2, visualize=False):
    """
    f1 and f2 should be periodic functions that oscillate between -1 and 1
    """
    t = np.arange(0,numberOfPriceChanges)
    prices = [itemStartPrice]
    minPriceBorder = [itemMinPrice]
    maxPriceBorder = [itemMaxPrice]
    currentPrice = itemStartPrice
    for j in t[1:] : 
        dynamicLowBorder = itemStartPrice -(itemStartPrice-itemMinPrice)*np.abs(f1(j))
        dynamicHighBorder = itemStartPrice +(itemMaxPrice-itemStartPrice)*np.abs(f2(j))
        currentPrice = genNextPrice(currentPrice, volatility, dynamicHighBorder, dynamicLowBorder, border, maxVol) # here I implemented a way to make maxprice and minprice fluctuate.
        prices.append(currentPrice)
        minPriceBorder.append(dynamicLowBorder)
        maxPriceBorder.append(dynamicHighBorder)
    continuousPriceOverTime = interp1d(t,prices)  
    if visualize:
        continuousLowBorder = interp1d(t,minPriceBorder) 
        continuousHighBorder = interp1d(t,maxPriceBorder) 
        mp.plot(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10), continuousPriceOverTime(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10)))  # just ploting to look at the curb
        mp.plot(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10), continuousLowBorder(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10)))
        mp.plot(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10), continuousHighBorder(np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10)))
    return continuousPriceOverTime


#############################################################################################################################################################

defaultItemStartPrice = 50  # Item default price
defaultItemMaxPrice = defaultItemStartPrice*1.5
defaultItemMinPrice = defaultItemStartPrice*0.5
defaultBorder = defaultItemStartPrice*0.1  # Border arround maxprice or minprice where the price will want to go to the opposite direction
defaultVolatility = 0.01 
defaultMaxVol = 0.02  # Set the max volatility to avoid violent price moves


#continuousFunctionOfPricesOverTime =genPriceOverTime(10000,defaultItemStartPrice,defaultItemMaxPrice,defaultItemMinPrice,defaultBorder,defaultVolatility,defaultMaxVol,visualize=True)
f1 = lambda  x : np.sin(x/300)
f2 = lambda  x : np.sin(x*np.log(x))
continuousFunctionOfPricesOverTime =advancedGenPriceOverTime(10000, defaultItemStartPrice, defaultItemMaxPrice, defaultItemMinPrice, defaultBorder, defaultVolatility, defaultMaxVol,f1, f2, visualize=True)



# To evalute price at a given time use: continuousFunctionOfPricesOverTime(float).flat[0]
