# pages/1_이미지_분류.py
import streamlit as st
from utils.model_utils import load_model, predict

st.set_page_config(page_title="이미지 분류", page_icon="🖼️")
st.title("🖼️ 이미지 분류")
# ... 이미지 분류 UI