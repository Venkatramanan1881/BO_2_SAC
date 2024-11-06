import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import css




def login():
    if np.random.randint(0, 2) == 0:
        return True, ['Dashboard', 'Dashboard 2', 'Dashboard 3', 'Dashboard 4', 'Dashboard 5']
    else:
        return False, []

@st.dialog("Creating Dashboard")
def convert_dashboard():
    for i in webi_dash_list:
        with st.container():
            pbar = st.progress(0, text=f"Converting {i} to SAC")
            for j in range(100):
                time.sleep(0.01)
                pbar.progress(j+1, text=f"Converting {i} to SAC")
            pbar.progress(100, text=f"Converted {i} to SAC")
            st.toast(f"Converted {i} to SAC")
    # st.balloons()
    st.success("Converted Dashboard to SAC")
    time.sleep(3)
    st.rerun()


st.subheader("WEBI to SAC")

if st.session_state.login == False:
    col = st.columns(2)
    with col[0]:
        with st.container(border=True, height=420):
            st.subheader("BO Credentials")
            bo_system = st.text_input("BO System")
            bo_username = st.text_input("BO Username")
            bo_password = st.text_input("BO Password", type="password")
            bo_auth = st.selectbox("Authentication", ["secEnterprise", "secLDAP", "secWinAD", "secSAPR3"])
    with col[1]:
        with st.container(border=True, height=420):
            st.subheader("SAC Credentials")
            sac_url = st.text_input("Login URL")
            sac_username = st.text_input("Username")
            sac_password = st.text_input("Password", type="password")
            st.markdown(css.edit_button, unsafe_allow_html=True)
            st.markdown('<span id="button-edit"></span>', unsafe_allow_html=True)
            if st.button("Login"):
                status, dash_list = login()
                if status == True:
                    st.session_state.dash_list = dash_list
                    st.session_state.login = True
                    st.rerun()
                else:
                    st.session_state.login = False
                    st.toast("Login Failed Check Credentials")
                

else:

    webi_dash_list = st.multiselect("Select Dashboard to Convert", st.session_state.dash_list)

    if webi_dash_list != []:
        if st.button("Convert"):
            convert_dashboard()

