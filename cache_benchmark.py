# /cache_benchmark.py
import streamlit as st
import time
import torchvision.models as models

st.title("⚡ 캐싱 효과 비교")

# 캐싱 없는 버전
def load_model_no_cache():
    time.sleep(0.5)  # 모델 로드 시뮬레이션
    return models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)

# 캐싱 있는 버전
@st.cache_resource
def load_model_with_cache():
    time.sleep(0.5)
    return models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)

col1, col2 = st.columns(2)

with col1:
    st.subheader("캐싱 없음")
    t0 = time.time()
    _ = load_model_no_cache()
    elapsed = time.time() - t0
    st.metric("로드 시간", f"{elapsed*1000:.0f}ms")
    st.info("슬라이더 조작할 때마다 재로드됨")

with col2:
    st.subheader("캐싱 있음")
    t0 = time.time()
    _ = load_model_with_cache()
    elapsed = time.time() - t0
    st.metric("로드 시간", f"{elapsed*1000:.0f}ms")
    st.success("최초 1회만 로드, 이후 캐시 사용")

# 재실행 트리거
st.slider("이 슬라이더를 움직여 재실행 유발", 0, 100, 50)