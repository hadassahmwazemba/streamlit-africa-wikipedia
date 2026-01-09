import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Visualization",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Conclusions")
st.write("""
         It was insightful to examine which countries engage most with Africa-related articles \
         on the English Wikipedia. Overall, the results aligned with my initial expectations: \
         **countries in the Americas and Europe exhibited the highest levels of engagement**, likely \
         because users in these regions make up a large proportion of the English-language Wikipedia readership.

         After applying a Naive Bayes classifier, the articles categorized as Africa-related \
         were largely accurate. However, some *classification limitations* remain such as
         -  *The model was trained and applied only to articles within the WikiProject Africa dataset, \
         meaning that additional Africa-related articles present in the broader DPDP dataset may not \
         have been captured.*

         There are also important limitations to this analysis. 
         - *Using the English Wikipedia as\
         a proxy for African engagement does not account for the multilingual nature of many Wikipedia \
         users, particularly across African countries where content is accessed in multiple languages.*

         Furthermore, Wikipedia pageviews are an imperfect measure of \
         regional engagement, as usage patterns vary significantly by country. \
         For example, countries such as the United States rely on Wikipedia more \
         heavily than many other regions, which may inflate their apparent level of engagement \
         relative to others. """)