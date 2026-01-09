import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Text Classification",
    layout="wide",
    initial_sidebar_state="expanded"
)



#Read the csv
PATH = "data/predicted_data.csv"
df = pd.read_csv(PATH)

st.title("Text Classification (African Vs Non-African)")


st.subheader("1. Establishment of the Ground truth")
st.write("""
         In order to build a classifier to categories the articles as either \
         African and Non-African, I had to establish the ground truth.

         To do so, I used the Wikidata attributes *country* and *country \
         of citizenship* of the articles from WikiProject Africa (around 120000) to filter and retrieve articles that were explicitly about \
         people, locations and events in Africa. I collected about **28000** that fit \
         into this criteria.

         Below is a snippet of the ground truth data after collection:
         """)

PATH = "data/groundtruth_df.csv"
groundtruth = pd.read_csv(PATH)

groundtruth = groundtruth.drop(columns=['Unnamed: 0'])
st.dataframe(groundtruth.head(15))

st.write("""
         To get the data of articles that were not african for the ground truth data, I filtered out the QIDs in the WikiProject and got the same wikidata information \
         as above.

         Below is a snippet of the Non-African ground truth:
         """)

PATH = "data/groundfalse_df.csv"
groundfalse = pd.read_csv(PATH)

groundfalse = groundfalse.drop(columns=['Unnamed: 0'])
st.dataframe(groundfalse.tail(15))


st.divider()
st.subheader("2. Building the classifier")

st.write("""
         I built the classifier using Naive bayes using the following steps.
         
         1. Training the model.

            - I used the label and descriptions to train the model
            70% percent of the data was used training and 30% was used for testing.
            For the training data not about Africa, I filtered out all the QIDs \
            from the WikiProject Africa dataset in the DPDP set to ensure that the articles being used were not related\
            to the continent.
         
         2. Vectorizing the data

            - I vectorized the data using **TF-IDF**
         
         3. Modelling
         
            - I used **Multinomial Naive Bayes** as my classifier.""")

st.divider()

st.subheader("3. Evaluation of the Model")
st.write("""
         To evaluate the model, I used a confusion matrix to visualize the classification report
         
         The results of the classifier were as follows:
         1. Precision = 96%
         2. Recall = 96%
         3. F1-Score = 97%""")


st.image('data/confusionmatrix.png', caption='Confusion Matrix', use_container_width=True)

st.divider()
st.subheader("4. Classified Results")
st.write("""
         I used the model to classify the articles that I had collected from the WikiProject Africa dataset \
         to find articles that were clearly and explicitly related to Africa for my analysis.
         
         The column *input* is the combination of the label and description column for each row \
         which was used as the input data for the classifier during training and classification""")

st.write("Below is a snippet of the articles that were labelled as **African**:")

classified_df = pd.read_csv("data/predicted_data.csv")

african_df = classified_df[classified_df['prediction'] == 'African']

african_df = african_df.drop(columns=['Unnamed: 0'])

st.write(african_df.head(50))



st.write("Below is a snippet of the articles that were labelled as **Not African**:")

notafrican_df = classified_df[classified_df['prediction'] == 'Not African']

notafrican_df = notafrican_df.drop(columns=['Unnamed: 0'])

st.write(notafrican_df.head(50))