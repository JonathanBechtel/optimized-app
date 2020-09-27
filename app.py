# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 15:53:06 2020

@author: Jonathan
"""

import streamlit as st
import pandas as pd
import pickle

# list of columns to use for app
cols = ['Id',
 'MSSubClass',
 'MSZoning',
 'LotArea',
 'Neighborhood',
 'OverallQual',
 'OverallCond',
 'YearBuilt',
 'GrLivArea',
 '1stFlrSF',
 '2ndFlrSF',
 'GrLivArea.1',
 'FullBath',
 'HalfBath',
 'GarageType',
 'GarageYrBlt',
 'GarageFinish',
 'GarageCars',
 'SalePrice']

num_cols = ['Id',
 'MSSubClass',
 'LotArea',
 'OverallQual',
 'OverallCond',
 'YearBuilt',
 'GrLivArea',
 '1stFlrSF',
 '2ndFlrSF',
 'GrLivArea.1',
 'FullBath',
 'HalfBath',
 'GarageYrBlt',
 'GarageCars',
 'SalePrice']

# function for loading in the grouping file -- notice the use of @st.cache -- speeds things up

st.title('Iowa Housing Data Application')

@st.cache
def load_grouping_file(x_col, y_col):
    filepath = f"https://raw.githubusercontent.com/JonathanBechtel/optimized-app/master/groupbys/{x_col}_{y_col}.csv"
    print(filepath)
    df = pd.read_csv(filepath)
    return df

@st.cache
def load_boxplot_dict():
    with open('boxplots.pkl', 'rb') as boxplot_dict:
        boxplots = pickle.load(boxplot_dict)
        
@st.cache
def load_seaborn_boxplot(boxplot_dict, x_axis, y_axis):
    chart_key = f"{x_axis}_{y_axis}"
    return boxplot_dict[chart_key]
    

section = st.sidebar.radio('Choose Application Section', ['Data Explorer', 'Model Explorer', 'Causal Impact'])

if section == 'Data Explorer':
    
    st.subheader("Build Charts From Sidebar Choices")
    
    x_axis = st.sidebar.selectbox('Choose Column For X-Axis', cols, index=1)
    y_axis = st.sidebar.selectbox('Choose Column For Y-Axis', num_cols, index=14)
    
    chart_type = st.sidebar.selectbox('Choose Chart Type', ['bar', 'line', 'box'])
    
    if chart_type == 'bar':
        try:
            file = load_grouping_file(x_axis, y_axis)
            st.bar_chart(file)
        except:
            st.text("Could not find data for specified column combinations")    
        
    elif chart_type == 'line':
        try:
            file = load_grouping_file(x_axis, y_axis)
            st.line_chart(file)
        except:
            st.text("Could not find data for specified column combinations")
            
    elif chart_type == 'box':
        boxplots = load_boxplot_dict()
        try:
            chart = load_seaborn_boxplot(boxplots, x_axis, y_axis)
            st.pyplot(chart.figure)
        except:
            st.text("Could not find seaborn chart figure for specified columns")
