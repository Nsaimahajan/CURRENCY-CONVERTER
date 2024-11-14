import streamlit as st
from PIL import Image
import pandas as pd
import requests

#---------------------------------#
# Title

image = Image.open('logo.png')
st.image(image, width=390)
st.title('Currency Converter App')
st.markdown("""This app interconverts the value of foreign currencies!""")

#---------------------------------#
# Sidebar + Main panel
st.sidebar.header('Input Options')

## Sidebar - Currency price unit
currency_list = ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'GBP', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'USD', 'ZAR']
base_price_unit = st.sidebar.selectbox('Select base currency for conversion', currency_list)
symbols_price_unit = st.sidebar.selectbox('Select target currency to convert to', currency_list)

# Retrieving currency data from Exchangerate-API
@st.cache_data
def load_data(base, symbols):
    # Define the API URL
    url = f'https://v6.exchangerate-api.com/v6/3267531ea17ed6ee50603daa/latest/{base}'
    
    try:
        # Send request to the API
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            raise ValueError(f"Error {response.status_code}: {data.get('error-type', 'Unknown error')}")

        # Extract rates from the response
        rates = data['conversion_rates']  # The key containing the conversion rates
        
        if symbols in rates:
            # Get the conversion rate for the selected target currency
            conversion_rate = rates[symbols]
            
            # Prepare DataFrame for display
            df = pd.DataFrame({
                'Base Currency': [base],
                'Target Currency': [symbols],
                'Conversion Rate': [conversion_rate],
                'Date': [data['time_last_update_utc']]
            })
            return df
        else:
            st.error(f"Conversion rate for {symbols} not found.")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Error retrieving data: {e}")
        return None
    except ValueError as ve:
        st.error(ve)
        return None

# Load and display data
df = load_data(base_price_unit, symbols_price_unit)
if df is not None:
    st.header('Currency Conversion')
    st.write(df)

#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown(""" 
* **Python libraries:** streamlit, pandas, pillow, requests
* **Data source:** [Exchangerate API](https://www.exchangerate-api.com/) which provides exchange rates based on various sources.
* **Note:** For educational purposes only. Not financial advice.
""")
