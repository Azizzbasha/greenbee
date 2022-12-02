import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
from firebase_admin import credentials
from firebase_admin import db

cred_obj = credentials.Certificate("greenbee-servicekey.json")
databaseURL = 'https://greenbee-project-default-rtdb.firebaseio.com/'
ref = db.reference("/")

st.title('GreenBee Innovation')

# Initialization
if 'key' not in st.session_state:
    st.session_state['key'] = 0


# Randomly fill a dataframe and cache it


@st.cache(allow_output_mutation=True)
def get_dataframe():
    return pd.DataFrame(
        # np.random.randn(50, 6),
        [("", 0, 0, 0, 0, 0)] * 12,
        columns=('Equipment Name', 'No', 'Watt', 'Using Hr', 'Total Watt', 'Watt Hr/Day'))


df = get_dataframe()


# Create row, column, and value inputs
equip_placeholder = st.empty()
no_placeholder = st.empty()
watt_placeholder = st.empty()
usinghr_placeholder = st.empty()
equip_name = equip_placeholder.text_input(
    label='Equipment Name', value="", key=0)
no = no_placeholder.number_input('No', value=0, key=1)
watt = watt_placeholder.number_input('Watt', value=0, key=2)
usinghr = usinghr_placeholder.number_input('Using Hr', value=0, key=3)

# Adding button and adding the data entered to the pandas dataframe
if st.button('Add'):
    df['Equipment Name'][st.session_state.key] = equip_name
    df['No'][st.session_state.key] = no
    df['Watt'][st.session_state.key] = watt
    df['Using Hr'][st.session_state.key] = usinghr

    df['Total Watt'][st.session_state.key] = df['No'][st.session_state.key] * \
        df['Watt'][st.session_state.key]

    df['Watt Hr/Day'][st.session_state.key] = df['No'][st.session_state.key] * \
        df['Watt'][st.session_state.key] * df['Using Hr'][st.session_state.key]
    st.session_state.key += 1
    equip_name = equip_placeholder.text_input(
        label='Equipment Name', value="", key=4)
    no = no_placeholder.number_input('No', value=0, key=5)
    watt = watt_placeholder.number_input('Watt', value=0, key=6)
    usinghr = usinghr_placeholder.number_input('Using Hr', value=0, key=7)


totalwattsum = df['Total Watt'].sum()
watthrsum = df['Watt Hr/Day'].sum()
json_obj = {
    'Load Details':
        {
            'totalwattsum': totalwattsum,
            'watthrsum': watthrsum
        }
    }

ref.set(json_obj)

st.subheader('Result')
st.write(f"Total Watt: {totalwattsum}")
st.write(f"Total Watt Hr/Day: {watthrsum}")

st.subheader('Entered Wrong Data? Delete it right away')
row_to_delete = st.text_input(
    label='Row to delete', placeholder='Enter number of row to be deleted')
if st.button(label='Delete row'):
    totalwattsum -= df['Total Watt'][int(row_to_delete)]
    watthrsum -= df['Watt Hr/Day'][int(row_to_delete)]
    json_obj = {
    'Load Details':
        {
            'totalwattsum': totalwattsum,
            'watthrsum': watthrsum
        }
    }

    ref.set(json_obj)
    df['Equipment Name'][int(row_to_delete)] = ""
    df['No'][int(row_to_delete)] = 0
    df['Watt'][int(row_to_delete)] = 0
    df['Using Hr'][int(row_to_delete)] = 0
    df['Total Watt'][int(row_to_delete)] = 0
    df['Watt Hr/Day'][int(row_to_delete)] = 0
    st.session_state.key -= 1
st.write("or")
if st.button(label="Delete All Rows"):
    for i in range(len(df)):
        df['Equipment Name'][i] = ""
        df['No'][i] = 0
        df['Watt'][i] = 0
        df['Total Watt'][i] = 0
        df['Using Hr'][i] = 0
        df['Watt Hr/Day'][i] = 0
        st.session_state.key -= 1
st.subheader('Electrical Load Data')
# And display the result!
st.dataframe(df)
if st.button('Generate Graph'):
    st.area_chart(df, x='Total Watt', y='Watt Hr/Day')

    st.set_option('deprecation.showPyplotGlobalUse', False)
    totalwattgraph = [i for i in df['Total Watt']]
    watthrdaygraph = [i for i in df['Watt Hr/Day']]

    plt.fill_between(np.arange(12), totalwattgraph, color="lightpink",
                     alpha=0.5, label='Total Watt')
    plt.fill_between(np.arange(12), watthrdaygraph, color="skyblue",
                     alpha=0.5, label='Watt Hr/Day')
    st.pyplot(plt.show())


