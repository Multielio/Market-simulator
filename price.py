# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 15:14:25 2019
@author: Multielio
"""
import random
import numpy as np
import matplotlib.pyplot as mp
from scipy.interpolate import interp1d


class Item(object):
    def  __init__(self):
        pass
         
    def getPossiblePriceWithThatVolatity(self, old_price, volatility):
        rnd1 = random.random()
        rnd2 = random.random()
        change_direction = 1 if rnd1 > 0.5 else -1
        change_percent =  volatility * rnd2
        change_amount = old_price * change_direction * change_percent
        return old_price + change_amount

    def genNextItemPrice(self, oldPrice, volatility, maxprice, minprice,border,maxvol):
        suggested_price = self.getPossiblePriceWithThatVolatity(oldPrice, volatility)
        rand = random.random()
        while not( minprice + border * rand <= suggested_price <= maxprice - border * rand ):
            rand = random.random()
            if maxvol > volatility:
                volatility += 0.002
            suggested_price = self.getPossiblePriceWithThatVolatity(oldPrice, volatility)
        return suggested_price	


    def genPriceOverTime(self, numberOfPriceChanges, itemStartPrice, itemMaxPrice, itemMinPrice, border, volatility, maxVol, f1=lambda x: np.sin(x/300), f2=lambda x: np.sin(x/700), visualize=False):
        """
        f1 and f2 should be periodic functions that oscillate between -1 and 1
        """
        t = np.arange(0,numberOfPriceChanges)
        prices = [itemStartPrice]
        minPriceBorder = [itemMinPrice]
        maxPriceBorder = [itemMaxPrice]
        currentPrice = itemStartPrice
        for j in t[1:] : 
            dynamicLowBorder = itemStartPrice - (itemStartPrice-itemMinPrice)*np.abs(f1(j))
            dynamicHighBorder = itemStartPrice + (itemMaxPrice-itemStartPrice)*np.abs(f2(j))
            currentPrice = self.genNextItemPrice(currentPrice, volatility, dynamicHighBorder, dynamicLowBorder, border, maxVol) # here I implemented a way to make maxprice and minprice fluctuate.
            prices.append(currentPrice)
            minPriceBorder.append(dynamicLowBorder)
            maxPriceBorder.append(dynamicHighBorder)
        continuousPriceOverTime = interp1d(t,prices)  
        if visualize:
            continuousLowBorder = interp1d(t,minPriceBorder) 
            continuousHighBorder = interp1d(t,maxPriceBorder) 
            lin = np.linspace(0, numberOfPriceChanges-1, numberOfPriceChanges*10)
            mp.plot(lin, continuousPriceOverTime(lin))  # just ploting to look at the generated prices
            mp.plot(lin, continuousLowBorder(lin))
            mp.plot(lin, continuousHighBorder(lin))
            mp.legend(["Item Price", "Low Border", "High Border"])
            mp.show()
        return continuousPriceOverTime


#############################################################################################################################################################

defaultItemStartPrice = 20  # Item default price
defaultItemMaxPrice = defaultItemStartPrice*1.5
defaultItemMinPrice = defaultItemStartPrice*0.5
defaultBorder = defaultItemStartPrice*0.1  # Border around maxprice or minprice where the price will want to go to the opposite direction
defaultVolatility = 0.01 
defaultMaxVol = 0.02  # Set the max volatility to avoid violent price moves

# f1 and f2 should be any function that map:  Reals -> Interval 
# with Inverval included in [-1, 1]
# An oscillating function between -1 and 1 works well for item price for ingame economy
# Some example functions:
# f3 = lambda  x : np.exp(3*np.sin(x*f1_frequency))/np.exp(3)
# f4 = lambda  x : np.cosh(8*np.sin(x*f1_frequency))/np.cosh(8)
# f5 = lambda  x : np.cosh(8*np.sin(np.log((x/5)%600+30)))/np.cosh(8)


f1_frequency = 1/300
f1 = lambda  x : np.sin(x/300) # Low Border
f2 = lambda  x : np.sin(np.log((x/5)%600+30)) # High Border

item = Item()
continuousFunctionOfPricesOverTime = item.genPriceOverTime( 10000, 
                                                            defaultItemStartPrice, 
                                                            defaultItemMaxPrice, 
                                                            defaultItemMinPrice, 
                                                            defaultBorder, 
                                                            defaultVolatility, 
                                                            defaultMaxVol, 
                                                            f1, 
                                                            f2, 
                                                            visualize=True)


# To evalute price at a given time use: continuousFunctionOfPricesOverTime(float).flat[0]
