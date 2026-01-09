import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile, json
from io import TextIOWrapper

st.set_page_config(
    page_title="Visualization",
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


st.title("Data Vizualization")


st.subheader("Map of Pageviews Per Capita")
st.write("The following visualization shows the number of pageviews per capita (per 1000000)\
         for each year (2023-2025)")

#adding the per capita column to the dataframe

# make year
df["year"] = pd.to_datetime(df["date"]).dt.year

# views per country-year
views_cty_yr = (
    df.groupby(["country", "year"], as_index=False)["pageviews"]
      .sum()
)



# population per country-year 
pop_cty_yr = (
    df.groupby(["country", "year"], as_index=False)["population"]
      .first()
)

# region per country-year 
region_cty_yr = (
    df.groupby(["country", "year"], as_index=False)["region"]
      .first()
)

# mergind df
merged_df = (views_cty_yr
             .merge(pop_cty_yr, on=["country", "year"], how="left")
             .merge(region_cty_yr, on=["country", "year"], how="left")
)



# per-capita (per 1,000,000 people)
merged_df["views_per_capita"] = (merged_df["pageviews"] / merged_df["population"]) * 1_000_000

merged_df["views_per_capita"] = pd.to_numeric(merged_df["views_per_capita"], errors="coerce")

# replace inf/-inf with NaN and drop bad rows for plotting
merged_df["views_per_capita"] = merged_df["views_per_capita"].replace([float("inf"), float("-inf")], pd.NA)
merged_df = merged_df.dropna(subset=["views_per_capita", "region"])

merged_df = merged_df[["country", "year", "region", "population", "pageviews", "views_per_capita"]]

merged_df = merged_df.dropna(subset=["region"])

# make sure population is numeric
merged_df["population"] = pd.to_numeric(merged_df["population"], errors="coerce")

# avoid division by 0
merged_df.loc[merged_df["population"] <= 0, "population"] = pd.NA


#User controls
regions = st.multiselect("Filter by region", ['North America','South America','Asia','Africa','Europe', 'Oceania'], default=['North America', 'South America','Asia','Africa','Europe', 'Oceania']) 

filtered_df = merged_df[merged_df["region"].isin(regions)]


#Plotly Chloropleth

# FORCE numeric right before plotting (this is the key)

# global_max = filtered_df["views_per_capita"].max()
# global_max = (int(global_max / 100) + 1) * 100

global_max = filtered_df["views_per_capita"].dropna().max()

if pd.isna(global_max) or global_max <= 0:
    global_max = 100  # fallback
else:
    global_max = int((global_max // 100 + 1) * 100)



fig = px.choropleth(
    filtered_df,
    locations="country",
    locationmode="country names",
    color="views_per_capita",
    range_color=[0, global_max],
    animation_frame="year",
    hover_name="country",
    color_continuous_scale="Viridis",
    title=f"Choropleth Map of {"views_per_capita (1M)".replace('_', ' ').title()}",
    height=700, width=1000
)

# Show borders
fig.update_geos(
    showcountries=True, countrycolor="black",
    showcoastlines=True, coastlinecolor="gray",
    showland=True, landcolor="lightgray"
)

fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)


st.divider()
st.subheader("Views Per Capita by Country")

# year widget
year_options = sorted(merged_df["year"].dropna().unique())
year_choice = st.selectbox("Choose a year:", year_options, key="bar_year")

df_year = merged_df[merged_df["year"] == year_choice].copy()

# region widget
region_options = sorted(df_year["region"].dropna().unique())
region_choice = st.selectbox("Choose a region:", region_options, key="bar_region")

df_region = df_year[df_year["region"] == region_choice].copy()


top_default = (
    df_region.sort_values("views_per_capita", ascending=False)
             .head(5)["country"]
             .tolist()
)

country_options = sorted(df_region["country"].dropna().unique())
countries = st.multiselect(
    "Select Countries:",
    country_options,
    default=top_default,
    key="bar_countries"
)

plot_df = df_region[df_region["country"].isin(countries)].copy()

if plot_df.empty:
    st.warning("No data to plot")
else:
    plot_df = plot_df.sort_values("views_per_capita", ascending=False)

    fig_bar = px.bar(
        plot_df,
        x="country",
        y="views_per_capita",
        hover_data={"pageviews": True, "population": True, "region": True, "year": True},
        title=f"Views per Capita (per 1M people) — {region_choice}, {year_choice}",
    )

    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)




st.divider()
st.header("Most Viewed Articles Per Country")

year_select = st.selectbox(
    "Choose a year:",
    sorted(df["year"].dropna().unique()),
    key="views_years"
)

df_year = df[df["year"] == year_select].copy()

if df_year.empty:
    st.warning("No rows available for that year.")
else:
    country = st.selectbox(
        "Choose a country:",
        sorted(df_year["country"].dropna().unique()),
        key="views_countries"
    )

    country_df = df_year[df_year["country"] == country].copy()

    top25 = (
        country_df.groupby("article", as_index=False)["pageviews"]
        .sum()
        .sort_values("pageviews", ascending=False)
        .head(25)
    )

    st.write(f"Most Viewed Articles in **{country}** for **{year_select}**")
    st.dataframe(top25[["article", "pageviews"]])