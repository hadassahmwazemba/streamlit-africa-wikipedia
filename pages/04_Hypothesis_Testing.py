import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile, json
from io import TextIOWrapper

st.set_page_config(
    page_title="Text Classification",
    layout="wide",
    initial_sidebar_state="expanded"
)



#Read the csv
zip_filepath = "data/filtered_dpdp.zip"
csv_filename = "filtered_dpdp.csv"

with zipfile.ZipFile(zip_filepath, "r") as zf:
    with zf.open(csv_filename) as f:
        df = pd.read_csv(TextIOWrapper(f, encoding="utf-8"))

df.head()


st.title("Hypothesis Testing")

st.subheader("Research Question")
st.write("What is the engagement of African-Related Wikipedia articles \
         in the English Wikipedia?")

st.divider()
st.subheader("Null Hypothesis")
st.write("There is no significant difference in African-Related \
         Wikipedia article pageviews across world regions.")


st.divider()
st.subheader("Alternative Hypothesis")
st.write("American and European countries show higher engagement \
         (pageviews) than other regions.")

st.divider()
st.subheader("Measurement")
st.write("To test this hypothesis I calculated the pageviews \
         of each continent per capita for both 2023 and 2024")

st.divider()
st.subheader("Testing")

########
# Visualization to  see the number of page views per Region
########

#getting the year of the dates

df['year'] = df['date'].apply(lambda x: x.split('-')[0])


###########
## Group into regions by country
#######
filtered_df = df.groupby(['region', 'year'])['pageviews'].sum().reset_index()

###########
## Normalize the data per capita
###########

#dropping duplicates (NB : will fix cause some of the countries are not in 2024)
unique_countries = df.drop_duplicates(subset=['country', 'year'])

#getting the total populations first
population_df = unique_countries.groupby(['region','year'])['population'].sum().reset_index()

merged_df = filtered_df.merge(population_df, how='right')

#calculate the pageviews per capita (1000)
merged_df['views_per_capita']  = merged_df['pageviews'] / df['population'] * 1000000

#zscore
merged_df["views_zscore"] = (
    merged_df["views_per_capita"] - merged_df["views_per_capita"].mean()
) / merged_df["views_per_capita"].std()



###########
## Visualization
##########

st.header("Analysis of Pageviews Per Capita")

year = st.selectbox('Choose a year:', ['2023','2024','2025'])

if year:
    year_df = merged_df[merged_df['year'] == year]

regions = st.multiselect('Filter by region:', ['North America','South America','Asia','Africa','Europe', 'Oceania'], default=['North America', 'South America','Asia','Africa','Europe', 'Oceania'])

regions_df = year_df[year_df['region'].isin(regions)]

regions_df = regions_df.sort_values(by="views_per_capita", ascending=False)

#st.dataframe(regions_df)


#Plot the barplot


fig = px.bar(regions_df,
             x=regions_df['region'],
             y=regions_df['views_per_capita'],
             color= regions_df['region'],
             title = 'Pageviews Per Capita Per Year')

fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Pageviews per capita (1M)",
    )

st.plotly_chart(fig, use_container_width=True)




########
# Visualization to  see the number of page views per Country
########

#getting the year of the dates

df['year'] = df['date'].apply(lambda x: x.split('-')[0])


###########
## Group into regions by country
#######
filtered_df = df.groupby(['country', 'year'])['pageviews'].sum().reset_index()

#dropping duplicates (NB : will fix cause some of the countries are not in 2024)
unique_countries = df.drop_duplicates(subset=['country', 'year'])

st.divider()
st.subheader("Conclusion")
st.write("Based on the observed pageview differences across regions, \
         we reject the null hypothesis and find evidence consistent with higher \
         engagement in Northern American and European countries.")