import sys
sys.path.append(sys.path[0].split('BI_to_SAC')[0] + 'BI_to_SAC')
import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import css 
import lumira_functions as lf
import zipfile


def extract_zip(file_path):
    extracted_files = {}
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            with zip_ref.open(file_name) as file:
                extracted_files[file_name] = file.read()
                
    return extracted_files


import os

def save_uploadedfile(uploadedfile):
    global file_name
    zip_path = os.path.join("lumira_files", uploadedfile.name.split('.')[0] + ".zip")

    # Save the uploaded zip file
    with open(zip_path, "wb") as f:
        f.write(uploadedfile.getbuffer())
    
    # Extract the contents of the zip file
    extracted_files = extract_zip(zip_path)

    # Initialize paths for extracted files
    content_xml_path = os.path.join("lumira_files", "content.xml")
    custom_css_path = os.path.join("lumira_files", "custom.css")

    for file_name, content in extracted_files.items():
        if file_name.endswith(".biapp"):
            # Save content.xml
            with open(content_xml_path, "wb") as f:
                f.write(content)
        elif file_name.endswith(".css"):
            # Save custom.css
            with open(custom_css_path, "wb") as f:
                f.write(content)

    return 1


def login():
    if np.random.randint(0, 2) == 0:
        return True
    else:
        return True



# @st.dialog("Creating Dashboard")
def convert_dashboard(model_name):
    with st.container():
        lf.start(model_name)
        st.toast("Converted Dashboard to SAC")
        st.success("Converted Dashboard to SAC")
        time.sleep(3)
        st.rerun()

st.subheader("Lumira to SAC") 



if st.session_state.sac_login == False:
    col = st.columns([1,2,1])
    with col[1]:
        with st.container(border=True, height=420):
            st.subheader("SAC Credentials")
            sac_url = st.text_input("Login URL")
            sac_username = st.text_input("Username")
            sac_password = st.text_input("Password", type="password")
            st.markdown(css.edit_button, unsafe_allow_html=True)
            st.markdown('<span id="button-edit"></span>', unsafe_allow_html=True)
            if st.button("Login"):
                status = login()
                if status == True:
                    st.session_state.sac_login = True
                    st.rerun()
                else:
                    st.session_state.sac_login = False
                    st.toast("Login Failed Check Credentials")
                


else:
    c = st.columns([1,3,1])
    with c[1]:
        zip_file = st.file_uploader("Upload Lumira Dashboard's Zip file", type=["lumx", "zip"])
        


    if zip_file is not None:
        model_name = zip_file.name.split('.')[0]

        save_uploadedfile(zip_file)
        with c[1]:
            if st.button("Convert"):
                convert_dashboard(model_name)


