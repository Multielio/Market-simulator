# Market simulator

![Market](https://github.com/Multielio/Market_simulator/blob/master/example.png)

[**Fig. 1:** Blue line is the price of the item over time. Green and orange are the dynamic boundaries of the price.]

-------------------------------------------------------------------------------------------------------------------------
   **Required libraries**
   
  - matplotlib
  - scipy
  - numpy


  **Description**
  
  This Python script simulate a market, given the initial price of the product, the volatility of the market (constant), the max price,     the min price of the product and other parameters, it generate the item price over time randomly.
  A dynamic border is created to model market cycles and to avoid prices droping too fast.

  To use this script call the "continuousFunctionOfPricesOverTime" function with an float in argument and put visualize=False if you    don't   need the graph.


  **Usage case**
  
  - You could use it if you want to implement a real market in your game and force players to sell their items at the right time !
-------------------------------------------------------------------------------------------------------------------------

  **Images**

Over more time:

![Market](https://github.com/Multielio/Market_simulator/blob/master/example2.png)

[**Fig. 2:** Blue line is the price of the item over time. Green and orange are the dynamic boundaries of the price.]


With other periodic functions for dynamic borders :

![Market](https://github.com/Multielio/Market_simulator/blob/master/example4.png)

[**Fig. 3:** Blue line is the price of the item over time. Green and orange are the dynamic boundaries of the price.]
