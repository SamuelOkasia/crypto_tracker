import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Crypto Historical Data", layout="wide")
st.title("Bitcoin Historical Data Viewer")

api_url = "https://crypto-tracker-backend-428718.nw.r.appspot.com/historical_data/"

response = requests.get(api_url)
if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)

    st.dataframe(df)

    st.subheader("Closing Price Chart")
    fig = px.line(df, x='date', y='close', title='Closing Price Over Time')
    st.plotly_chart(fig)


    st.subheader("RSI and CCI Chart")
    fig2 = px.line(df, x='date', y=['rsi_7', 'rsi_14', 'cci_7', 'cci_14'], title='RSI and CCI Indicators')
    st.plotly_chart(fig2)

else:
    st.error("Failed to retrieve data")

st.markdown("""
    <style>
    .stDataFrame {
        font-size: 90%;
    }
    </style>
""", unsafe_allow_html=True)
