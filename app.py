import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers,OpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import re
import os

load_dotenv()


st.title("Personalized Diet and Workout Recommender:coffee:")

st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
st.subheader('🤖 Google Gemini-Pro LLM Model', divider='rainbow')

st.markdown('<style>h5{color: pink;  text-align: right;}</style>', unsafe_allow_html=True)

hide_streamlit_style = """
            <style>

            background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
            background-size: cover;
            
            [data-testid="stToolbar"] {visibility: hidden;}
            .reportview-container {
            margin-top: -2em;
        }
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            #stDecoration {display:none;}
            footer {visibility: hidden;}
            div.embeddedAppMetaInfoBar_container__DxxL1 {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

llm = OpenAI(temperature=0.9)

prompt_template = PromptTemplate(
  input_variables=['age','gender','weight','height','veg_or_nonveg','allergies'],
  template="Diet Recommendation System:\n"
        "I want you to recommend 5 restaurants names, 5 breakfast names, 5 dinner names, and 5 workout names, "
             "based on the following criteria:\n"
             "Age: {age}\n"
             "Gender: {gender}\n"
             "Weight: {weight}\n"
             "Height: {height}\n"
             "Veg_or_Nonveg: {veg_or_nonveg}\n"
             "Food allergies: {allergies}."
)

age = st.number_input("Age",min_value=0)
gender = st.selectbox("Gender",["Male","Female","Other"])
weight = st.number_input("Weight(pounds)",min_value=0)
height = st.number_input("Height(cm)",min_value=0)
veg_or_nonveg = st.selectbox('Veg or Non-Veg',['Veg','Non-Veg'])
allergies = st.text_input("Food allergies")

if st.button("Get Recommendations"):
    chain = LLMChain(llm=llm ,prompt = prompt_template)
    input_data = {
        'age':age,
        'gender':gender,
        'weight':weight,
        'height':height,
        'veg_or_nonveg':veg_or_nonveg,
        'allergies':allergies

    }
    results = chain.run(input_data)

    #initialize recommendation lists
    restaurant_names = []
    breakfast_names = []
    dinner_names = []
    workout_names = []

    #Extract the different recommendations using regular expressions
    restaurant_matches = re.findall(r'Restaurants:(.*?)Breakfast:',results,re.DOTALL)
    if restaurant_matches:
        restaurant_names = [name.strip() for name in restaurant_matches[0].strip().split('\n') if name.strip()]
    
    breakfast_matches = re.findall(r'Breakfast:(.*?)Dinner:', results, re.DOTALL)
    if breakfast_matches:
        breakfast_names = [name.strip() for name in breakfast_matches[0].strip().split('\n') if name.strip()]

    dinner_matches = re.findall(r'Dinner:(.*?)Workouts:', results, re.DOTALL)
    if dinner_matches:
        dinner_names = [name.strip() for name in dinner_matches[0].strip().split('\n') if name.strip()]

    workout_matches = re.findall(r'Workouts:(.*?)$', results, re.DOTALL)
    if workout_matches:
        workout_names = [name.strip() for name in workout_matches[0].strip().split('\n') if name.strip()]


    st.subheader('Recommendations')
    st.markdown('###Restaurants')
    if restaurant_names:
        for restaurant in restaurant_names:
            st.write(restaurant)
    else:
        st.write("No restaurant recommendation available")
        
    st.markdown("#### Breakfast")
    if breakfast_names:
        for breakfast in breakfast_names:
            st.write(breakfast)
    else:
        st.write("No breakfast recommendations available.")

    st.markdown("#### Dinner")
    if dinner_names:
        for dinner in dinner_names:
            st.write(dinner)
    else:
        st.write("No dinner recommendations available.")

    st.markdown("#### Workouts")
    if workout_names:
        for workout in workout_names:
            st.write(workout)

# Footer
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #000000; /* Black background color */
    color: #ffffff; /* White text color */
    text-align: center;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown('<p class="footer">Generative AI : Python-Langchain Application <br>  Created by Khalid Kifayat <br> (www.beingkhalid.com / www.builtautomations.com)</p>', unsafe_allow_html=True)
