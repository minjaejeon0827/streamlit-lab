# app_dashboard.py
import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# 더미 메트릭 생성 함수
def generate_metrics():
    now = datetime.now()
    timestamps = [now - timedelta(seconds=i * 5) for i in range(60, 0, -1)]
    return pd.DataFrame({
        "시간": timestamps,
        "지연시간(ms)": np.random.normal(1.8, 0.3, 60).clip(0.5, 5),
        "처리량(req/s)": np.random.normal(556, 50, 60).clip(100, 800),
        "GPU 사용률(%)": np.random.normal(75, 10, 60).clip(0, 100),
        "오류율(%)": np.random.exponential(0.1, 60).clip(0, 5),
    })


# 화면 구성(UI 구성)
st.title("📊 실시간 모델 서빙 모니터링")
st.markdown("TensorRT FP16 엔진의 서빙 지표를 실시간으로 추적합니다.")

# 자동 새로고침 설정
auto_refresh = st.sidebar.checkbox("자동 새로고침 (5초)", value=False)
refresh_interval = st.sidebar.slider("새로고침 간격(초)", 1, 30, 5)

# 데이터 생성
df = generate_metrics()
latest = df.iloc[-1]

# 현재 상태 카드
st.header("현재 상태")
col1, col2, col3, col4 = st.columns(4)

col1.metric("평균 지연시간", f"{latest['지연시간(ms)']:.2f}ms",
            f"{np.random.choice([-0.1, 0.1, 0.0]):.1f}ms")
col2.metric("처리량", f"{latest['처리량(req/s)']:.0f} req/s",
            f"{np.random.choice([-5, 5, 0]):.0f} req/s")
col3.metric("GPU 사용률", f"{latest['GPU 사용률(%)']:.1f}%",
            f"{np.random.choice([-1, 1, 0]):.1f}%")
col4.metric("오류율", f"{latest['오류율(%)']:.2f}%",
            f"{np.random.choice([-0.01, 0.01, 0]):.2f}%")

st.divider()

# 탭을 활용한 다중 시계열 차트
tab1, tab2, tab3 = st.tabs(["지연시간", "처리량", "GPU/오류"])

with tab1:
    fig = px.line(df, x="시간", y="지연시간(ms)",
                  title="지연시간 추이")
    fig.add_hline(y=2.0, line_dash="dash",
                  annotation_text="SLA 기준 (2ms)")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.line(df, x="시간", y="처리량(req/s)",
                  title="처리량 추이")
    fig.add_hline(y=500, line_dash="dash",
                  annotation_text="목표 처리량 (500 req/s)")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["시간"], y=df["GPU 사용률(%)"],
                              name="GPU 사용률", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=df["시간"], y=df["오류율(%)"],
                              name="오류율", yaxis="y2",
                              line=dict(color="red")))
    fig.update_layout(
        title="GPU 사용률 & 오류율",
        yaxis=dict(title="GPU (%)"),
        yaxis2=dict(title="오류율 (%)", overlaying="y", side="right")
    )
    st.plotly_chart(fig, use_container_width=True)

# 자동 새로고침 구현
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()