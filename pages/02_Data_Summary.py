import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile, json
from io import TextIOWrapper

st.set_page_config(
    page_title="Data Summary",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Read the csv
#PATH = "data/filtered_dpdp.csv"
#df = pd.read_csv(PATH)


zip_filepath = "data/filtered_dpdp.zip"
csv_filename = "filtered_dpdp.csv"

with zipfile.ZipFile(zip_filepath, "r") as zf:
    with zf.open(csv_filename) as f:
        df = pd.read_csv(TextIOWrapper(f, encoding="utf-8"))

df.head()







st.title("Data Summary")

st.subheader("Overview of the data metrics used for analysis")

st.metric("Number of Countries:","224")
st.metric("Number of unique articles (in the DPDP set)","15672")
st.metric("Wikipedia Project", "WikiProject Africa")
st.metric("Date Range","02/06/2023 - 12/31/2025")


st.divider()

st.subheader("Data Collection Process")

st.write("""

        The data used in the analysis was collected using the following process:
         
         Using **WikiProject Africa (a Wikipedia project \
         that covers all the articles about people, things, and events about Africa)**, \
         I got all the QIDs (unique identification) of the articles in the project.

         The QIDs were then used to get the instances for all the articles that were \
         present in the **DPDP** dataset for 2023 - 2025.

         **The pageviews of the articles (found in the DPDP dataset) are the metric that is \
         used to measure engagement in this analysis.**

         Below is a preview of the DPDP dataset that was collected:

         """)


preview_dpdp = df.drop(columns = ['Unnamed: 0', 'country', 'region', 'population'])
st.dataframe(preview_dpdp.head(50))

st.write("""
         In order to perform the engagement analysis per country and region using this dataset, I \
         added the following information for all the collected rows of DPDP data:
            1. Country
            2. Region (continent)
            3. Population
         """)

st.dataframe(df.head(50))

st.write("""
         While doing the data collection, it became clear that some articles in the WikiProject Africa dataset \
         were not explicity/clearly relevant to Africa. Some articles were in the \
         dataset even though they had mentioned the continent in passing, such as \
         the article for *Boxing day*

         As such, I had to build a classifier to categorize the articles in this dataset as either:
         *African* or *Not African*

         After classification, only **2931368** rows of data, with **15672** unique articles, remained. \
         This final data is what was used for the analysis.
         
         """)

st.divider()

st.subheader("Descriptive Statistics")

st.write("The following are the descriptive statistics of the dataset based on the pageviews")


desc = df["pageviews"].describe()

col1, col2 = st.columns(2)

with col1:
    st.metric("Count", f"{int(desc['count']):,}")
    st.metric("Mean", f"{desc['mean']:.2f}")
    st.metric("Std Dev", f"{desc['std']:.2f}")
    st.metric("Min", f"{int(desc['min']):,}")

with col2:
    st.metric("25%", f"{int(desc['25%']):,}")
    st.metric("Median (50%)", f"{int(desc['50%']):,}")
    st.metric("75%", f"{int(desc['75%']):,}")
    st.metric("Max", f"{int(desc['max']):,}")