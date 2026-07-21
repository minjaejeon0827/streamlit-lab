# app.py 소스코드
import streamlit as st
import numpy as np
import plotly.express as px

st.title("🚀 배포 테스트 앱")
n = st.slider("데이터 포인트", 10, 200, 50)
data = np.random.randn(n)
fig = px.histogram(x=data, title="정규분포 샘플")
st.plotly_chart(fig)
st.success("배포 성공!")
