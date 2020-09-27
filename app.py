# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 15:53:06 2020

@author: Jonathan
"""

import streamlit as st
import pandas as pd
import pickle
import seaborn as sns

# list of columns to use for app
cols = ['MSSubClass', 'MSZoning', 'Neighborhood', 'OverallQual', 'OverallCond', 'YearBuilt', 'FullBath', 'HalfBath', 'GarageType']

num_cols = ['OverallQual', 'OverallCond', 'GrLivArea', 'SalePrice', 'LotArea', 'SalePrice']
# function for loading in the grouping file -- notice the use of @st.cache -- speeds things up

st.title('Iowa Housing Data Application')

# loads in the grouping file to be used for bar/line charts
@st.cache
def load_grouping_file(x_col, y_col):
    filepath = f"https://raw.githubusercontent.com/JonathanBechtel/optimized-app/master/groupbys/{x_col}_{y_col}.csv"
    print(filepath)
    df = pd.read_csv(filepath, index_col=x_col)
    return df

# loads in the seaborn boxplot
@st.cache
def load_boxplots(x_col, y_col):
    pickled_boxplot = f"boxplots/{x_col}_{y_col}.pkl"
    with open(pickled_boxplot, 'rb') as boxplot_dict:
        chart = pickle.load(boxplot_dict)
    return chart
        
@st.cache
def load_seaborn_boxplot(boxplot_dict, x_axis, y_axis):
    chart_key = f"{x_axis}_{y_axis}"
    return boxplot_dict[chart_key]
    

section = st.sidebar.radio('Choose Application Section', ['Data Explorer', 'Model Explorer', 'Causal Impact'])

if section == 'Data Explorer':
    
    st.subheader("Build Charts From Sidebar Choices")
    
    x_axis = st.sidebar.selectbox('Choose Column For X-Axis', cols)
    y_axis = st.sidebar.selectbox('Choose Column For Y-Axis', num_cols)
    
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
        try:
            chart = load_seaborn_boxplot(x_axis, y_axis)
            st.pyplot(chart)
        except:
            st.text("Could not find seaborn chart figure for specified columns")
