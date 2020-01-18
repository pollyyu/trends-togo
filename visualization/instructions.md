# Trends To Go #
## Trends and Forecasts of Restaurant Profiles in US' Top Cities ##

This app demonstrates the trends and forecasts of 30 restaurant profiles in the top cities in US.
 
Please select the views on the sidebar to start navigating the pages 

## How Visualization is organized ##

There are four main views in identifying trending topic/ city combination: 

### Macro-level ###
1. Top Cities
1. Top Topics

### Micro-level ###
1. Top topics for a given city
1. Top cities for a given topic

### For each of these areas, we will rank top candidate(s) by comparing: ###
#### 1. Absolute count of reviews ####
 The data is first normalized to the beginning of the period (March 2018). We then compare the most recent 4 weeks' sum of review count and the first four weeks' of review count.
#### 2. Percentage difference #### 
The data is compared on a percentage difference of most recent 4-week period and tthe first 4-week period of a specified prior period.
#### 3. Forecast difference ####
 This ranking is currently available only for macro-view where we run topic and city level forecasting with SARIMA. A neural net is currently being trained for micro-view forecasting. Be patient for updates!

We have 25 top cities and 30 restaurant profile. Hence we have 715 city/topic combinations that are ranked by configurations you are able to manipulate. I hope you have fun!

### If you have any questions please feel free to email me at paulynnyu@gmail.com ### 
