import streamlit as st

# X 재실행 시 count가 0으로 초기화됨
# count = 0
# if st.button("카운트 증가", key="btn1"):
#     count += 1
# st.write(f"카운트: {count}")  # 항상 0 또는 1

# 1번째 클릭:
#   스크립트 처음부터 실행 → count = 0으로 초기화
#   → button이 True 반환 (클릭됐으므로) → count += 1 → count = 1
#   → "카운트: 1" 표시

# 2번째 클릭:
#   스크립트가 다시 처음부터 실행 → count = 0으로 또 초기화!
#   → button이 True 반환 → count += 1 → count = 1
#   → "카운트: 1" 표시 (변하지 않음)

# session_state로 값 유지
if "count" not in st.session_state:
    st.session_state.count = 0

# if st.button("카운트 증가", key="btn2"):
if st.button("카운트 증가"):
    st.session_state.count += 1

st.write(f"카운트: {st.session_state.count}")  # 올바르게 증가

# 딕셔너리처럼 접근
st.session_state["count"] = 0
value = st.session_state["count"]

# 속성처럼 접근 (더 많이 사용됨)
st.session_state.count = 0
value = st.session_state.count

def load_model():
    pass

# 활용 예시: 모델 로드 상태 유지
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False
    st.session_state.model = None

if not st.session_state.model_loaded:
    with st.spinner("모델 로딩 중..."):
        st.session_state.model = load_model()
        st.session_state.model_loaded = True
        
# 콜백 함수와 함께 사용하기
def increment():
    st.session_state.count += 1

st.button("증가", on_click=increment)
# on_click 콜백은 스크립트 재실행 "전"에 실행됨

# 위젯의 key를 이용한 자동 연동
st.text_input("이름", key="username")
# st.session_state.username으로 값에 바로 접근 가능
# (위젯에 key를 지정하면 session_state와 자동으로 동기화됨)

st.write(st.session_state.username)