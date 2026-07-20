import streamlit as st
import pandas as pd
import numpy as np

# 데이터프레임
df = pd.DataFrame({
    "클래스": ["고양이", "개", "새"],
    "확률": [0.85, 0.12, 0.03]
})
st.dataframe(df, use_container_width=True)   # 인터랙티브 (정렬, 검색 가능)
st.table(df)                                  # 정적 테이블 (인터랙션 없음)

# 차트 (내장 - 별도 라이브러리 불필요)
st.line_chart(np.random.randn(50, 3))     # 선 그래프
st.bar_chart(df.set_index("클래스"))        # 막대 그래프
st.area_chart(np.random.randn(50))        # 영역 그래프

# 지도
map_data = pd.DataFrame({
    "lat": [37.5665], "lon": [126.9780]   # 서울 좌표
})
st.map(map_data)

# Matplotlib
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(np.random.randn(100))
st.pyplot(fig)
# 주의: fig 객체를 명시적으로 만들어서 전달해야 함

# Plotly (인터랙티브 차트에 권장)
import plotly.express as px
fig = px.bar(df, x="클래스", y="확률", title="분류 결과")
st.plotly_chart(fig, use_container_width=True)
# 마우스 호버 시 값 표시, 확대/축소 등 인터랙션 자동 지원

# 이미지/비디오/오디오
from PIL import Image
image = Image.open("sample.jpg")
st.image(image, caption="업로드된 이미지", use_column_width=True)
# 주석친 코드 필요 시 참고(2026.07.17 minjae)
# st.video("sample.mp4")
# st.audio("sample.mp3")

# JSON/메트릭
st.json({"model": "ResNet-50", "accuracy": 0.761})

col1, col2, col3 = st.columns(3)
col1.metric("정확도", "76.1%", "+0.5%")
col2.metric("지연시간", "1.8ms", "-0.3ms")
col3.metric("처리량", "556 img/s", "+12 img/s")

# 컬럼 분할 - 가로로 화면을 나눔
col1, col2 = st.columns(2)
with col1:
    st.header("원본 이미지")
    # 아래 주석친 코드 필요 시 참고(2026.07.17 minjae)
    # st.image("original.jpg")
with col2:
    st.header("분류 결과")
    # 아래 주석친 코드 필요 시 참고(2026.07.17 minjae)
    # st.bar_chart(results)
    
# 비율 지정 컬럼
col1, col2, col3 = st.columns([1, 2, 1])  # 1:2:1 비율
# 가운데 컬럼이 양쪽보다 2배 넓게 표시됨

# 탭 - 같은 화면 안에서 여러 뷰를 전환
tab1, tab2, tab3 = st.tabs(["이미지 분류", "텍스트 분석", "모델 정보"])
with tab1:
    st.write("이미지 분류 UI")
with tab2:
    st.write("텍스트 분석 UI")
    
# 사이드바 - 메인 화면과 분리된 영역 (보통 설정용)
with st.sidebar:
    st.header("설정")
    model = st.selectbox("모델", ["ResNet-50", "ViT"])
    threshold = st.slider("임계값", 0.0, 1.0, 0.5)
    
# 확장/축소 섹션 - 기본적으로 접혀 있다가 클릭 시 펼쳐짐
with st.expander("고급 설정"):
    st.slider("배치 크기", 1, 64, 8)
    st.checkbox("GPU 사용")
# 화면을 깔끔하게 유지하면서도 고급 옵션을 제공할 때 유용

# 컨테이너 (동적 업데이트)
placeholder = st.empty()
with st.container():
    st.write("컨테이너 내부 콘텐츠")
    
import time

# 프로그레스 바 - 진행률을 정확히 알 수 있을 때
progress = st.progress(0)
status = st.empty()

for i in range(100):
    progress.progress(i + 1)
    status.text(f"처리 중: {i+1}/100")
    time.sleep(0.01)

status.success("완료!")

# 스피너 - 작업이 얼마나 걸릴지 모를 때
with st.spinner("모델 로드 중..."):
    time.sleep(2)
st.success("로드 완료!")

# 상태 표시 - 여러 단계로 이루어진 작업의 진행 상황을 단계별로 보여줄 때
with st.status("추론 실행 중...", expanded=True) as status_obj:
    st.write("전처리 중...")
    time.sleep(1)
    st.write("모델 추론 중...")
    time.sleep(1)
    st.write("후처리 중...")
    time.sleep(0.5)
    status_obj.update(label="완료!", state="complete")