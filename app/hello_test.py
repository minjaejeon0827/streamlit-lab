# import streamlit as st

# st.title("설치 확인 테스트")
# st.write("이 화면이 보인다면 Streamlit 설치가 완료된 것입니다.")
# st.balloons()   # 풍선 애니메이션 (재미 요소)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목 계층
st.title("AI 이미지 분류기")              # H1 - 페이지당 보통 1개
st.header("모델 정보")                   # H2 - 섹션 구분
st.subheader("ResNet-50 FP16")         # H3 - 하위 섹션

# 텍스트
st.text("고정폭 텍스트")                  # 서식 없는 일반 텍스트
st.markdown("**굵게**, *기울임*, `코드`")  # 마크다운 문법 지원
st.markdown("""
## 지원 포맷
- JPEG, PNG, WebP
- 최대 크기: **10MB**
""")

st.write("일반 텍스트")              # 텍스트로 출력
st.write(["a", "b", "c"])         # 리스트로 출력
st.write({"key": "value"})        # JSON처럼 출력
# 아래 주석친 코드 필요 시 참고(2026.07.17 minjae)
# st.write(pd.DataFrame(...))       # 테이블로 출력
st.write(pd.DataFrame({"이름": ["a", "b", "c"], "값": [1, 2, 3]}))
st.write(plt.figure())            # 차트로 출력
# → 타입을 신경 쓰지 않고 일단 st.write()로 출력해보는 것이 디버깅에 유용

# 정보/경고/오류 박스
st.info("ℹ️ 이미지를 업로드하면 분류가 시작됩니다.")    # 파란색
st.success("✅ 추론이 완료되었습니다.")             # 초록색
st.warning("⚠️ 파일 크기가 너무 큽니다.")           # 노란색
st.error("❌ 모델 로드에 실패했습니다.")             # 빨간색

# 코드 블록 (구문 강조 포함)
st.code("""
import torch
model = torch.load("model.pth")
""", language="python")

# 수식 (LaTeX 문법)
st.latex(r"q = \text{round}\left(\frac{r}{S}\right) + Z")
# → 양자화 수식처럼 수학적 표현이 필요할 때 유용

# 텍스트 입력
name = st.text_input("이름을 입력하세요", placeholder="홍길동")
query = st.text_area("분석할 텍스트", height=150)
# text_input: 한 줄 입력 / text_area: 여러 줄 입력

# 숫자 입력
threshold = st.slider("신뢰도 임계값", min_value=0.0,
                      max_value=1.0, value=0.5, step=0.05)
batch_size = st.number_input("배치 크기", min_value=1,
                              max_value=64, value=8)
# slider: 범위 내 값을 시각적으로 선택
# number_input: 정확한 숫자를 직접 입력

# 선택
model_type = st.selectbox("모델 선택",
                           ["ResNet-50", "EfficientNet-B4", "ViT-Base"])
precisions = st.multiselect("정밀도",
                             ["FP32", "FP16", "INT8"], default=["FP16"])
# selectbox: 하나만 선택 / multiselect: 여러 개 선택 가능

# 토글/체크박스
use_gpu = st.checkbox("GPU 사용", value=True)
show_details = st.toggle("상세 정보 표시")
# checkbox와 toggle은 기능적으로 동일 (불리언 반환), 디자인만 다름

# 라디오 버튼
mode = st.radio("실행 모드", ["단일 이미지", "배치 처리"],
                horizontal=True)
# horizontal=True: 가로로 나열 (기본값은 세로)

# 버튼
if st.button("추론 시작", type="primary"):
    st.write("추론 중...")
# 버튼은 클릭된 순간에만 True를 반환하고, 다음 재실행 시 다시 False가 됨
# type="primary": 강조된 색상의 버튼 (기본 액션을 표시할 때 사용)

# 파일 업로드
uploaded = st.file_uploader("이미지 업로드",
                             type=["jpg", "jpeg", "png"],
                             accept_multiple_files=True)
# type: 허용할 확장자 제한
# accept_multiple_files=True: 여러 파일 동시 업로드 허용
# 반환값: UploadedFile 객체 (또는 리스트), 업로드 안 하면 None

# 색상 선택
color = st.color_picker("테마 색상", "#FF4B4B")