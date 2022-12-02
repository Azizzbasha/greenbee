import streamlit as st
# from firebase_admin import db

# ref = db.reference("/Load Details/")
totalwattsum = 0
watthrsum = 0
# totalwattsum = ref.order_by_child("totalwttsum".get())
# watthrsum = ref.order_by_child("watthrsum".get())
st.title('BATTERY BANK CALCULATOR')
st.subheader("Battery Bank Load Details")

bttry_bank_volt = st.number_input(
    label='Battery Bank\'s Voltage: (Volts DC)', value=24)
rsrv_day = st.number_input(
    label='Reserve days (No. of days battery gives current)', value=15)
loss = st.number_input(
    label='Loose connection / Wire loss factor (%)', value=20)
bttry_eff = st.number_input(label='Battery Effeciency (%)', value=100)
bttry_aging = st.number_input(label='Battery Aging (%)', value=100)
dod = st.number_input(label='Depth of discharge (%)', value=50)

with st.form('temp'):
    c1, c2 = st.columns(2)
    with c1:
        temperature = st.number_input(
            label='Battery Operating Temperature ', value=80)
    with c2:
        temp_unit = st.selectbox(
            label='Temperature Units',
            options=('C', 'F'),
            index=0,
            label_visibility='hidden'
        )
    st.form_submit_button('Submit')

# THE BATTERY BANK REQUIRED

st.write('''
    ###### Each Battery Rating
''')
with st.form('eachbatteryrating'):
    c1, c2 = st.columns(2)
    with c1:
        bttry_rating_amphr = st.number_input(
            label='Ampere-Hour (Amp.Hr)', value=150.0)
    with c2:
        bttry_rating_volts = st.number_input(label='Volts (V)', value=12.0)
    sizebtn = st.form_submit_button(label='Done')

battery_conn = st.selectbox(
    label='Batteries connection for battery bank',
    options=('Parallel', 'Series', 'Series-Parallel'),
    index=0
)


st.subheader('Battery Bank Ouytput')
st.write(f'Type of connection for Batteries: {battery_conn}')


st.subheader('Battery Calculations')

st.write(f'Total KW.Hr/Day : {watthrsum} Watt.Hr/Day')

total_amphr = watthrsum / bttry_bank_volt
st.write(f'Total Amp.Hr : {total_amphr} Amp.Hr')

avg_load = (total_amphr * (1 + (loss / 100))) / (bttry_eff / 100)
st.write(f'Average Load : {avg_load} Amp.Hr')

storage_req = avg_load * rsrv_day
st.write(f'Storage Required : {storage_req} Amp.Hr')

battery_aging = (storage_req) * (1+(bttry_aging/100))
st.write(f'Battery aging : {battery_aging} Amp.Hr')
