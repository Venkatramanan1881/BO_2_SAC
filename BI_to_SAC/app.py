import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(
    layout="wide"
)

if "login" not in st.session_state:
    st.session_state.login = False
if "dash_list" not in st.session_state:
    st.session_state.dash_list = []
if"sac_login" not in st.session_state:
    st.session_state.sac_login = False
if"running" not in st.session_state:
    st.session_state.running = False


# st.logo(f"logo/maventic.png",
# icon_image = "logo/maventic_analytics.png")



st.session_state.pages = {
                        "Menu":[
                            st.Page("pages/webi.py", title="Webi", icon=":material/pie_chart:", default=True),
                            st.Page("pages/lumira.py", title="Lumira", icon=":material/analytics:"),
                        ]
                    }
# st.session_state.pages = st.navigation([st.Page(login)])
pages = st.navigation(st.session_state.pages)

pages.run()