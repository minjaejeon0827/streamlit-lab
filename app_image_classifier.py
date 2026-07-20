import json
import time
# import pandas as pd
# import numpy as np
import streamlit as st
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import plotly.express as px
from PIL import Image

# 파이썬 패키지 설치
# pip install torch torchvision

# streamlit app_image_classifier.py 소스파일 터미널 실행 명령어
# streamlit run app_image_classifier.py --server.address=0.0.0.0

# ImageNet 클래스 레이블 (1000개 클래스 이름이 담긴 JSON)
IMAGENET_CLASSES_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"

# 클래스 이름(json) 가져오는 함수
@st.cache_data
def load_class_labels():
    import urllib.request
    with urllib.request.urlopen(IMAGENET_CLASSES_URL) as f:
        return json.load(f)

# 모델 로드
@st.cache_resource
def load_model(model_name: str):
    """모델 로드 (캐싱으로 재실행 시 재로드 방지)"""
    if model_name == "ResNet-50":
        model = models.resnet50(
            weights=models.ResNet50_Weights.IMAGENET1K_V1
        )
    elif model_name == "EfficientNet-B4":
        model = models.efficientnet_b4(
            weights=models.EfficientNet_B4_Weights.IMAGENET1K_V1
        )
    model.eval()
    return model

# 모델 전처리
def preprocess_image(image: Image.Image) -> torch.Tensor:
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    return transform(image).unsqueeze(0)  # transform -> (3, 224, 224), unsqueeze -> (1, 3, 224, 224)

# 추론 함수
def predict(model, image_tensor: torch.Tensor, top_k: int = 5):
    with torch.no_grad():
        outputs = model(image_tensor)
        probs = torch.softmax(outputs, dim=1)  # 원본 출력: 음수, 양수 섞임 -> softmax로 확률화
        top_probs, top_indices = probs.topk(top_k)
    return top_probs[0].numpy(), top_indices[0].numpy()


# 화면 구성(UI 구성)
st.title("🖼️ AI 이미지 분류기")
st.markdown("ResNet-50 또는 EfficientNet-B4로 이미지를 분류합니다.")

# 화면의 왼쪽 사이드바 구성
with st.sidebar:
    st.header("⚙️ 모델 설정")
    model_name = st.selectbox(
        "모델 선택",
        ["ResNet-50", "EfficientNet-B4"]
    )
    top_k = st.slider("상위 K개 결과", 1, 10, 5)
    show_confidence = st.checkbox("신뢰도 표시", value=True)

    st.divider()
    st.header("ℹ️ 모델 정보")
    info = {
        "ResNet-50": {"정확도": "76.1%", "크기": "97.8MB", "지연시간": "~8ms"},
        "EfficientNet-B4": {"정확도": "83.4%", "크기": "74.5MB", "지연시간": "~15ms"}
    }
    for k, v in info[model_name].items():
        st.metric(k, v)

# 메인 부분 — 모델 로드
with st.spinner(f"{model_name} 모델 로드 중..."):
    model = load_model(model_name)
    class_labels = load_class_labels()
st.success(f"✅ {model_name} 로드 완료!")

# 파일 업로드
uploaded_files = st.file_uploader(
    "이미지를 업로드하세요 (여러 장 가능)",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.divider()
        col1, col2 = st.columns([1, 1])

        with col1:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption=uploaded_file.name,
                     use_column_width=True)
            st.caption(f"크기: {image.size[0]}×{image.size[1]}px")

        with col2:
            with st.spinner("추론 중..."):
                t0 = time.time()
                tensor = preprocess_image(image)
                probs, indices = predict(model, tensor, top_k)
                elapsed = (time.time() - t0) * 1000

            st.metric("추론 시간", f"{elapsed:.1f}ms")

            # 결과 데이터프레임
            results = []
            for prob, idx in zip(probs, indices):
                results.append({
                    "클래스": class_labels[idx],
                    "신뢰도": float(prob)
                })

            # 바 차트
            fig = px.bar(
                x=[r["신뢰도"] for r in results],
                y=[r["클래스"] for r in results],
                orientation="h",
                title="Top-K 분류 결과",
                labels={"x": "신뢰도", "y": "클래스"},
                color=[r["신뢰도"] for r in results],
                color_continuous_scale="Blues"
            )
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            # 최고 예측 강조
            best = results[0]
            st.success(
                f"**예측 결과**: {best['클래스']} "
                f"({best['신뢰도']*100:.1f}%)"
            )
else:
    st.info("👆 이미지를 업로드해 분류를 시작하세요.")
    # 샘플 이미지 사용 버튼
    if st.button("샘플 이미지로 테스트"):
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg",
            caption="샘플 이미지"
        )