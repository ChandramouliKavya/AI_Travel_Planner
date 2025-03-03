import streamlit as st
from langchain_core.prompts import ChatPromptTemplate 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser



# creating an template 

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Given a source and destination, and number of travelers, provide an estimated travel cost for different travel modes (e.g., flight, train, bus, car). Include the estimated travel time, cost range, and any key factors affecting the trip  and which is best time to travel."),
    ("human", "Can you provide travel details, including cost estimates and travel time, for a trip from {source} to {destination} for {num_travellers} people using {mode_of_transport}?")
])

# Retrieve API key from Streamlit Secrets
api_key = st.secrets["gcp"]["google_api_key"]

# setting the open ai key and initialize the chatmodel

chat_model = ChatGoogleGenerativeAI(google_api_key = api_key, model = "gemini-1.5-flash")

output_parser = StrOutputParser()

# creating a chain

chain = prompt_template | chat_model  | output_parser

st.title("🌍 AI Travel Estimator")

st.markdown(
     "Easily plan trips with estimated costs, best travel seasons, and transport options. Get quick insights for hassle-free travel! ✈️🚆🚌🚗"
)


source = st.text_input("📌source")
destination = st.text_input(" 📍destination")
num_travellers = st.selectbox("👥Number of travellers",[1,2,3,4,5,6,7,8,9,10])
mode_of_transport = st.selectbox("Mode of Transport",["✈️ Flight", "🚆 Train", "🚌 Bus", "🚗 Car"])


if st.button(" 🔍Trip Estimation"):
    raw_input = {
        "source": source,
        "destination":destination,
        "num_travellers" : num_travellers,
        "mode_of_transport" : mode_of_transport
    }
    response = chain.invoke(raw_input)
    st.write("### Estimated Travel Details")
    st.write(response)


