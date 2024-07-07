import streamlit as st
import requests

url = "https://crypto-tracker-backend-428718.nw.r.appspot.com"

st.title("Crypto tracker")

st.subheader("Top Cryptos")

response = requests.get(f"{url}/top_crypto")
data = response.json()
columns = st.columns(len(data))
style = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    .small-text {
        font-size: 0.8em;
        font-family: 'Roboto', sans-serif;
    }
    .ask {
        color: green;
    }
    .bid {
        color: red;
    }
    </style>
"""

st.markdown(style, unsafe_allow_html=True)
for i, info in enumerate(data):
    with columns[i]:
        st.metric(label="Symbol", value=info['name'])
        st.markdown(f"<div class='small-text ask'>Ask: ${info['ask']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-text bid'>Bid: ${info['bid']}</div>", unsafe_allow_html=True)


def calculate_option_profit_loss(spot_price, strike_price, premium, option_type, contracts):
    if option_type == "Call":
        profit_loss = max(spot_price - strike_price - premium, -premium) * contracts * 100
    elif option_type == "Put":
        profit_loss = max(strike_price - spot_price - premium, -premium) * contracts * 100
    return profit_loss

# Form for user inputs
with st.form("options_calculator"):
    st.header("Crypto Options Profit/Loss Calculator")

    spot_price = st.number_input("Current Spot Price", min_value=0.0, step=0.01)
    strike_price = st.number_input("Strike Price", min_value=0.0, step=0.01)
    premium = st.number_input("Premium Paid", min_value=0.0, step=0.01)
    option_type = st.selectbox("Option Type", ["Call", "Put"])
    contracts = st.number_input("Number of Contracts", min_value=1, step=1)

    submitted = st.form_submit_button("Calculate")

    if submitted:
        result = calculate_option_profit_loss(spot_price, strike_price, premium, option_type, contracts)
        st.write(f"Profit/Loss: ${result:.2f}")



response = requests.get(f"{url}/cryptonews")
data = response.json()

st.markdown("""
    <style>
    .scrollable-container {
        max-height: 700px;
        overflow-y: auto;
        padding-right: 10px;
    }
    .scrollable-container::-webkit-scrollbar {
        width: 8px;
    }
    .scrollable-container::-webkit-scrollbar-thumb {
        background-color: #888;
        border-radius: 10px;
    }
    .scrollable-container::-webkit-scrollbar-thumb:hover {
        background-color: #555;
    }
    .article-card {
        padding: 1rem;
        margin: 10px 0;
        border-radius: 10px;
        background-color: #161A22;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .article-title {
        font-size: 1.5em;
        color: #fff;
    }
    .article-meta {
        font-size: 0.9em;
        color: #fff;
    }
    .article-text {
        font-size: 1em;
        color: #AEAEAE;
    }
  
    </style>
""", unsafe_allow_html=True)
st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
st.subheader("Crypto news")
for article in data:
    st.markdown(f"""
        <div class="article-card">
            <div class="article-title">{article['title']}</div>
            <div class="article-meta">Date: {article['date']}</div>
            <div class="article-text">{article['text']}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)