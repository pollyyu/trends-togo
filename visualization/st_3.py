#!/usr/bin/env python
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from collections import defaultdict
from sqlalchemy import create_engine
import time
from datetime import timedelta
from sys import getsizeof
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import data as data
plotsize = (13, 10)

def main():
	readme_text = st.markdown(open("instructions.md").read())
	st.sidebar.title("Pages")	
	app_mode = st.sidebar.selectbox("Select one of these pages to navigate app",["Instructions","Macro-view","Micro-view"])
	
	if app_mode == "Instructions":
		st.sidebar.success("To continue select one of the other views")
	elif app_mode == "Macro-view":
		readme_text.empty()
		run_the_app(app_mode)
	elif app_mode == "Micro-view":
		readme_text.empty()
		run_the_app(app_mode)

def topic_info(topic_list):
	topic_detail = data.topic_info()
	topic_detail = topic_detail.set_index(['km_label'])
	topic_out = pd.DataFrame()
	for i,r in enumerate(topic_list):
		topic_out = pd.concat([topic_out,topic_detail[topic_detail.index.isin([r])]])

	return(topic_out)

def run_the_app(app_mode):
	@st.cache #to download the data from endpoint only once
	def load_data():
		with open("df_keras.pickle", "rb") as f:
			df_keras = pickle.load(f)
		with open("topic_plot.pickle","rb") as f:
			topic_plot = pickle.load(f)
		with open("city_plot.pickle","rb") as f:
			city_plot = pickle.load(f)
		return df_keras, topic_plot, city_plot

	df_keras,topic_plot, city_plot = load_data()
	df_keras = df_keras.loc[:,'2018-03-03':'2019-11-17'] # taking the date after 2018-03-11 because data before that is sparse
	frame_selector_ui(df_keras, topic_plot, city_plot, app_mode)

def frame_selector_ui(df,topic_plot, city_plot, app_mode):
	'''
	Arguments
	---------
	df: the overall df without forecasting. For now this is reserved for macro view.
	topic_plot: this is df with forecasting by topics
	city_plot: this is df with forecasting by cities
	app_mode: this is the app mode that was selected (page). 
	
	Output
	--------
	plots of top restaurant profile segments based on user selection
	'''
	if app_mode == "Macro-view":
		st.title("The Macro View")
		st.sidebar.markdown("# Select your view")
		# Interested in Topics or Cities?
		area = st.selectbox("Topics or Cities?", ["Topics", "Cities"])
		# Getting best performing?
		best_worse = st.sidebar.radio("Best or Poorest Performing", ["Best", "Poorest"])
		# Top or bottom areas to visualize
		top_n = st.sidebar.slider("Select N Top / Bottom Area",0,25,5,1)
		# Method for ranking
		method = st.sidebar.radio("Select Normalized or Percentage Comparison",["norm","perc"])
		# If selection was percentage, what do you want to compare it to?
		if method == "perc":
			wks_prior = st.sidebar.slider("Choose periods before the most recent 4-week period to compare to", 10,len(data.df_topics()),100,1)
			st.sidebar.success("Topis/ cities are ranked by percentage difference of the most recent 4 weeks' vs the first 4 week's, starting from chosen periods prior to end point.")
		elif method == "norm":
			wks_prior = st.sidebar.slider("Periods prior to end point to normalize data", 10, len(data.df_topics()),52,1)
			st.sidebar.success("Topics/ cities are ranked by comparing the absolute difference of the most recent 4 weeks' vs  the first 4 weeks', starting from chosen normalized date. Normalized date is simply when total reviews are set to zero")
		# which data to run
		if best_worse == 'Best':
			ascending = False
		else:
			ascending = True
		df_sliced = slice_df(df, topic_plot, city_plot, sliced = area, topic = None, city = None)
		# run the plot
		plot_top_topic(app_mode, top_n, method, wks_prior, df_sliced, asc = ascending, sliced = area)
	
	elif app_mode == "Micro-view":
		st.title("The Micro View")
		st.sidebar.markdown('# Select your view')
		area = st.selectbox("Topics for a given city, or Cities for a given topic?",["Topics for a given city","Cities for a given topic"])
		if area == "Topics for a given city":
			area_plot = "topic_by_city"
			city = st.selectbox("Pick your city",df.loc[1,:].index)
			topic = None
		elif area == "Cities for a given topic":
			area_plot = "city_by_topic"
			topic = st.selectbox("Pick your topic",df.index.get_level_values('km_label').unique())
			city = None
		best_worse = st.sidebar.radio("Best or Poorest Performing", ["Best", "Poorest"])
		# Top or bottom areas to visualize$
		top_n = st.sidebar.slider("Select N Top / Bottom Area",0,25,5,1)
		# Method for ranking$
		method = st.sidebar.radio("Select Normalized or Percentage Comparison",["norm","perc"])
		# If selection was percentage, what do you want to compare it to?$
		if method == "perc":
			wks_prior = st.sidebar.slider("Choose periods before the most recent 4-week period to compare to", 0,90,52,1)
		elif method == "norm":
			wks_prior = st.sidebar.slider("Periods prior to end point to normalize data", 10, len(data.df_topics()),52,1)
			st.sidebar.success("Topics/ cities are ranked by comparing the absolute difference of the most recent 4 weeks' vs  the first 4 weeks', starting from chosen normalized date. Normalized date is simply when total reviews are set to zero")
		# which data to run$
		if best_worse == 'Best':
			ascending = False
		else:
			ascending = True
		
		df_sliced = slice_df(df, city_plot=None, topic_plot=None, sliced = area_plot, topic = topic, city = city)
		# run the plot$
		plot_top_topic(app_mode, top_n, method, wks_prior, df_sliced, asc = ascending, sliced = area_plot)
		if topic == None:
			st.write("")
		else:
			st.header("Topic Detail")
			st.table(topic_info([topic]))

def slice_df(df, topic_plot,city_plot, sliced, topic, city):
	if sliced == 'Cities':
		df_sliced = data.df_cities().T
	elif sliced == 'Topics':
		df_sliced = data.df_topics().T

	elif sliced == 'city_by_topic':
		df = data.df_all()
		df_sliced = df[df['km_label']==topic]
		df_sliced = df_sliced.set_index('city')
		df_sliced = df_sliced.iloc[:,2:]
	elif sliced == 'topic_by_city':
		df = data.df_all()
		df_sliced = df[df['city'] == city]
		df_sliced = df_sliced.set_index('km_label')
		df_sliced = df_sliced.iloc[:,2:]

	else:
		print("there is error with input data")

	return df_sliced

def plot_top_topic(app_mode, top_n, method, wks_prior, df, asc, sliced):
	'''
	Arguments
	----------
	top_n: top ranked cities we want to plot
	topic: selected topic
	method: norm or perc. Norm will return absolute difference and percentage will be on absolute percentage terms.
	wks_prior: only useful if we are using method == perc where we are comparing recent 4 weeks and n-wks prior's 4 weeks
	df: the dataframe we are plotting

	Returns
	----------
	A time series of the top n cities for the specified topic and method

'''
	#     df_sliced = df.loc[topic,:]  slicing data by specified topic

	# getting data by either normalized or percentage difference
	df_method = df_normalize(df, wks_prior)
	named_topic = data.topic_info()[['km_label','topic_name']].set_index(['km_label']) # pull named topic from sql database and create a dictionary
        
	if method == 'norm':
		top_cities = df_method.sum(axis=1).sort_values(ascending=asc)[:top_n].index # getting top n-specified cities
		to_plot = df_method[df_method.index.isin(top_cities)].reindex(top_cities)
        	
		if sliced == 'Topics' or sliced == 'topic_by_city':
			numbered_label = to_plot.sum(axis=1).index
			labels = []
			for i in numbered_label:
				labels.extend(str(i) + ": " + named_topic.loc[int(i)])
			to_plot.index = list(labels)
		st.header("Normalized Chart")
		st.write("Period in the chart starts from normalized date")
		plot_graph = to_plot.T
		plot_graph.index = [pd.to_datetime(x) for x in plot_graph.index]
		labels = list(to_plot.T.columns)
		to_plot.index = labels
		st.line_chart(to_plot.T)
		#df_sliced = df.loc[topic,:]
		topic = topic_info(list(top_cities.values))
		if sliced == 'Topics' or sliced == 'topic_by_city':
			topic = topic_info(list(top_cities.values))
			st.header("Topic details")
			st.write("Topic Names are ordered by their review volume")
			st.table(topic)
		else:
			st.write("")

	elif method == 'perc':
		perc_diff = df_percent_diff(df, wks_prior)
		top_cities = perc_diff.sort_values(ascending=asc)[:top_n].index
		df_actual = df[df.index.isin(list(top_cities))]
		# filtering chart by length of percentage volume
		df_actual = df_actual[df_actual.columns[-wks_prior:]]
	
		if sliced == 'Topics' or sliced == 'topic_by_city':
			numbered_label = df_actual.sum(axis=1).index
			labels = []
			for i in numbered_label:
				labels.extend(str(i) + ": " + named_topic.loc[int(i)])
			df_actual.index = list(labels)
		st.header("Percentage Chart")
		st.write("Period in the chart starts from normalized date")
		plot_graph = df_actual.T
		plot_graph.index = [pd.to_datetime(x) for x in plot_graph.index]
		labels = list(df_actual.T.columns)
		df_actual.index = labels
		st.line_chart(df_actual.T)
		topic = topic_info(list(top_cities.values))
		if topic.values.any():
			st.header("Topic details")
			st.write("Topic Names are ordered by their review volume")
			st.table(topic)
		else:
			st.write("")

	
	#else:
	#	forecast_diff = np.sum(df.iloc[:,-13:],axis=1) - np.sum(df.iloc[:,-25:-13], axis=1) # getting volume growth within 3 months
	#	top_cities = forecast_diff.sort_values(ascending=asc)[:top_n].index

def df_normalize(df, wks_prior):
	'''
	normalizes time series whereby each period is the difference from the first specified date
	'''
	f_date = pd.to_datetime(df.columns.T[-wks_prior])
	s_date = f_date + timedelta(7)
	normalized = df.loc[:,s_date:].sub(df.loc[:,f_date],axis='rows')
	
	#first_date = pd.to_datetime(df.T.columns[-wks_prior])
	#second_date = first_date + timedelta(7)
	#normalized = df.T.loc[:,second_date:].sub(df.T.loc[:,first_date],axis='rows')
	return normalized

def df_percent_diff(df, wks_prior):
	'''
	Arguments
	 -----------
	df: sliced df
	wks_prior: prior weeks we want to compare the most recent trend. E.g. 52 weeks would mean the same period 1 year ago
	Returns
	-----------
	returns list of area by their percent difference in the most recent 4 weeks vs start of trend
	'''
	list_perc = pd.DataFrame(df.iloc[:,-4:]).sum(axis=1) /(pd.DataFrame(df.iloc[:,-wks_prior:-wks_prior+4]).sum(axis=1)+1) - 1
	return list_perc



### Run the application
if __name__ == "__main__":
	main()
