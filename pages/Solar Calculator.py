import streamlit as st
import pandas as pd
from firebase_admin import db

watthrsum = 0
totalwattsum = 0
ref = db.reference("/Load Details/")

totalwattsum = ref.order_by_child("totalwttsum".get())
watthrsum = ref.order_by_child("watthrsum".get())
st.title("SOLAR PANEL CALCULATOR")
st.subheader("Solar Panel Details")
solar_sys_volt = st.number_input(label='Solar System Voltage (Volts DC)',
                                 value=24.0)
losses_in_wire = st.number_input(
    label='Losses in Wire, Connection, Battery (%)', value=20.0)
st.write('''
    ###### Daily Sunshine Hours
''')
with st.form(key='daily_sunshine_hr'):
    c1, c2, c3 = st.columns(3)
    with c1:
        inwinter = st.number_input("In Winter", value=5.0)
    with c2:
        insummer = st.number_input("In Summer", value=6.0)
    with c3:
        inmonsoon = st.number_input("In Monsoon", value=5.0)
    submitbtn = st.form_submit_button(label='Submit')

avg_sunshine = (inwinter+insummer+inmonsoon)/3
st.write(f"Average Daily Sunshine Hours: {round(avg_sunshine, 2)}")

st.write(f"Total Solar Power Need: {watthrsum}")

solar_power_correction = watthrsum + (watthrsum * (losses_in_wire/100))
st.write(
    f"Total Solar Power after correction factor: {solar_power_correction}")

solar_arr_size = solar_power_correction / avg_sunshine
st.write(f"Solar array size after calculating Sun Hour: {solar_arr_size}")

st.write('''
    ###### Size of Solar Panel
''')
with st.form('sizeofsolarpanel'):
    c1, c2 = st.columns(2)
    with c1:
        sizeofpanelwatt = st.number_input(label='Watts (W)', value=420.0)
    with c2:
        sizeofpanelvolt = st.number_input(label='Volts (V)', value=24.0)
    sizebtn = st.form_submit_button(label='Done')
solarpanel_conn = st.selectbox(
    label='Solar Panel Connection',
    options=('Parallel', 'Series', 'Series-Parallel'),
    index=0
)

st.subheader('Output of Solar Panel')
st.write(
    f'''
    ###### Size of solar panel: 
    {sizeofpanelwatt} Watt, {sizeofpanelvolt} Volts
    ''')

st.write(
    f'''
    ###### Type of connection for Solar Panel: 
    {solarpanel_conn}
    ''')

# losses_in_wire = st.number_input(
#     label='Losses in Wire, Connection, Battery (%)', value=20.0)

st.write(
    '''
    ###### Selection of Solar Panel Connection criteria: 
    ''')

if(solarpanel_conn == 'Series'):
    x = 1
    if(sizeofpanelwatt >= solar_arr_size):
        st.write('OK')
        y = 1
    else:
        st.write('Select Other Type of Connection')
        y = 0

elif(solarpanel_conn == 'Parallel'):
    x = 2
    if(sizeofpanelwatt >= solar_sys_volt):
        st.write('OK')
        y = 1
    else:
        st.write('Select Other Type of Connection')
        y = 0

elif(solarpanel_conn == 'Series-Parallel'):
    x = 3
    if(sizeofpanelwatt < solar_arr_size):
        if(sizeofpanelwatt < solar_sys_volt):
            st.write('OK')
            y = 1
        else:
            st.write('Select Other Type of Connection')
            y = 0
    else:
        st.write('Select Other Type of Connection')
        y = 0
else:
    st.write('')


if((solar_sys_volt % sizeofpanelvolt) == 0):
    st.write(
        '''
        ###### Selection of each solar panel efficiency: 
        OK
        ''')
else:
    st.write(
        f'''
        ###### Selection of each solar panel efficiency: 
        Select other solar voltage instead of {sizeofpanelvolt} volts''')


amphr = round(((solar_arr_size)/(sizeofpanelwatt)), 1)

st.write('''
    ###### Number of string for solar panel: 
    ''')
z = 0
if(y == 0):
    st.write('')
else:
    if(x == 1):
        z = 1
        st.write(f'{z}')
    elif(x == 2):
        z = round((amphr+0.1))
        st.write(f'{z}')
    elif(x == 3):
        z = round((amphr+0.1))
        st.write(f'{z}')
    else:
        st.write('')


st.write('''
    ###### Total watt of each solar panel string: 
    ''')
if(y == 1):
    st.write(f'{sizeofpanelwatt} watt, {(sizeofpanelwatt)/(sizeofpanelvolt)} amp')
else:
    st.write('')


st.write(
    '''
    ###### Total No. of Solar Panel in each string: 
    ''')

if((solar_sys_volt % sizeofpanelvolt) == 0):
    solarpanelineachstring = (solar_sys_volt)/(sizeofpanelvolt)
    st.write(f'{solarpanelineachstring}')
else:
    st.write('')

t = z*sizeofpanelwatt

st.subheader('Total Watts of Solar Panel: ')
st.write(f'{t} watts, {t/sizeofpanelvolt} amps')


st.subheader('Total no. of Solar Panel: ')
st.write(f'{z*solarpanelineachstring}')
