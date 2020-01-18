# trendstogo
trendstogo plots food trends at a City and Food Topic level. The data was obtained from menu and review data from 30,000 restaurants on grubhub.com. Please check it out on https://trendstogo.herokuapp.com/.

## Description
This project was incepted from a desire to find food trends in the US and an empathy towards restaurants, being difficult entities to succeed. As the demand for food delivery grow exponentially over the past years, so has the size of platforms such as Grubhub, Ubereats and Doordash. But while the market grows, restaurants are not necessarily better off as they [swallow high costs of delivery](https://www.forbes.com/sites/cameronkeng/2018/03/26/why-uber-eats-will-eat-you-into-bankruptcy/#29a1e0f221f6) and lose information on their customers and what customers value.

From public information (Grubhub's website), I was able to obtain data about restaurant, their menu profile and their review over time. 

**There are 3 main/ modules parts to this project:**

### 1. Clustering Restaurants to 30 Topics / Profiles ###
There were four types of information collected, which helped cluster the restaurants: 
1. Cuisine Names
1. Dish Names
1. Price of Top items
1. Variabilty of menu

LDA Topic Modeling was used to reduce the dimensions of *Cuisine Names* and *Dish Names* to fit into our final clustering model. K-means was selected as our final clustering model.

<img src="/static/images/full_model.png" width="70%">

The results enabled us to differentiate high level cuisine type restaurants. See below as an example:
<img src="/static/images/cluster_naming.png" width="70%">

**Related blog post:**[So you Want to Open a Ghost Kitchen](https://www.paulynnyu.com/trendstogo1)

The related notebook can be found here in these 
### 2. Finding Market Gaps through Creating a Clone ###
Cities are inherently different. iHouston is different from New York, so don't expect Italian places to do equally well in Houston as it does in New York. So how exactly do we compare between cities? We can choose to compare a city with cities similar to itself (sister cities) via similiarities in Food Importance. 

<img src="/static/images/houston_sisters.png" width="70%">

Better yet, we can create a clone.

<img src="/static/images/clone-houston.png" width="70%">

**Related Blog Post:** [Cities Aren't Alike, So Create a Clone](https://www.paulynnyu.com/trendstogo2/)

### 3. Finding Market Gaps through time-series ### 
While we can find market gaps between cities, trends change over time. What if Thai food is a more recent 8-month trend in Houston? One way we can capture that is through time-series. Here, I took posted date from restaurant reviews to obtain a time-series rolled up to a weekly level (starting Sunday). 

The final results, with its Topic and City clusters are visualized through a [Streamlit](https://www.streamlit.io/) app: https://trendstogo.herokuapp.com/.

**Related Blog Post:** [Being Bullish about ... Bulls?](https://www.paulynnyu.com/trendstogo3/)

## Data 
The data was obtained by making a direct API call to Grubhub. The first step was to get the longitude, latitude and radius mile of major city areas in the US and scrape all the restaurant ids. By iterating through each restaurant id, I am able to obtain restaurant, menu and review data in three separate API calls. 

The data was mostly parsed and kept in a postgres database. Only review data is updated weekly to update the streamlit app.

## Modules
**model - Clustering model and finding market gaps**
- cluster-model.ipynb - NLP and clustering model to create 30 restaurant profiles
- clone-city.ipynb - find market gaps by creating sister cities; a concrete example with Houston

### Requirements
numpy 1.16.1\
scipy 1.2.2\
pandas 0.24.2\
matplotlib 1.5.1\
psycopg2 2.6.1\
gensim 3.8.1\
streamlit 0.53.0

## Future Work
In the future, I'd like to incorporate the following improvements to the project: 
1. Forecasting at a City and Food Topic level
1. Menu generation
1. Price recommendation

Follow this repo updates :blush:
