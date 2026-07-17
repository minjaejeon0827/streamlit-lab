# /app/app_basic.py
import streamlit as st
import numpy as np
import pandas as pd

st.title("📊 나의 첫 Streamlit 앱")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    n_points = st.slider("데이터 포인트 수", 10, 500, 100)
    chart_type = st.radio("차트 종류", ["라인", "바", "산점도"])
    show_stats = st.checkbox("통계 정보 표시", value=True)

# 데이터 생성
data = np.random.randn(n_points)
df = pd.DataFrame({"값": data, "인덱스": range(n_points)})

# 메트릭 표시
col1, col2, col3 = st.columns(3)
col1.metric("평균", f"{data.mean():.4f}")
col2.metric("표준편차", f"{data.std():.4f}")
col3.metric("최댓값", f"{data.max():.4f}")

# 차트 표시
st.subheader(f"{chart_type} 차트")
if chart_type == "라인":
    st.line_chart(df.set_index("인덱스"))
elif chart_type == "바":
    st.bar_chart(df.set_index("인덱스"))

# 통계 정보
if show_stats:
    with st.expander("📈 상세 통계"):
        st.dataframe(df.describe(), use_container_width=True)

if st.button("🔄 데이터 새로고침", type="primary"):
    st.rerun()