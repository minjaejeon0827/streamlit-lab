# 앱 코드에서 접근
import streamlit as st

openai_key = st.secrets["api"]["openai_key"]
db_password = st.secrets["database"]["password"]

# 또는 딕셔너리처럼
db_config = st.secrets["database"]