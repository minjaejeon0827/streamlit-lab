# app.py (메인 페이지)
import streamlit as st

st.set_page_config(
    page_title="AI 추론 데모",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 AI 추론 데모")
st.markdown("""
## 환영합니다!

이 앱은 다음 기능을 제공합니다:

| 페이지 | 기능 |
|--------|------|
| 🖼️ 이미지 분류 | ResNet, EfficientNet으로 이미지 분류 |
| 💬 텍스트 분석 | 감성 분석, 텍스트 분류 |
| 📊 모델 정보 | 성능 벤치마크 및 비교 |

**사이드바에서 페이지를 선택하세요.**
""")

"""
Streamlit cloud로 배포하는 방법

준비물: 내가 완성한 프로젝트 폴더(my-ai-app)
 - app.py(메인, 엔트리 파일)
 - requirements.txt
 - pages 폴더 
 
배포 절차
1. GitHub 저장소 준비
   a. 깃허브 계정
   b. 리포지토리 하나 생성
   c. git init, add, commit, push
2. Streamlit Cloud 계정 필요
3. Create app
   참고: https://share.streamlit.io/ Create app 클릭
   a. GitHub 계정 연동 필요
"""