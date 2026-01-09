import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile, json
from io import TextIOWrapper

#set page configuration
st.set_page_config(
    page_title="African Articles Engagement on Wikipedia",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Indroduction of my research
st.title("Wikipedia Users Engagement with African-Related Articles on the \
         English Wikipedia")
st.write("By Hadassah Mwazemba")

st.subheader("Research Question")
st.write("""
         In this analysis, I examine how users of the English Wikipedia engage with articles\
         related to Africa.
         
         Using data collected from Wikidata and the 2023-2025 Wikipedia DPDP dataset, \
         I focus on patterns of engagement (page views) with Africa-related content.
         
         Specifically, this analysis addresses the following question:
         
         1. Which countries show the highest levels of engagement with \
         African-related Wikipedia articles?
         
         As such my overall Research Question is:

         **What is the engagement of African-Related Wikipedia articles \
         in the English Wikipedia?**
         """ )

st.divider()

st.subheader("Initial Expectations")
st.write("""
         My goal with this research question and its subsequent analysis is to examine how high or low 
         engagement with African-related articles is on the English Wikipedia.

         Based on this, I expect the following:
         1. Overall engagement with African-related articles will be relatively low.
         2. Regions with a high concentration of English-speaking countries, such that those in Nothern America and Europe 
         will exhibit the highest levels of engagement.
         """ )


st.divider()

st.subheader("Hypothesis")
st.write("My Hypothesis for this Research topic is that **American and European \
         countries have the highest engagement with these articles in terms\
         of pageviews**")
