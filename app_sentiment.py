# app_sentiment.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from transformers import pipeline


@st.cache_resource
def load_sentiment_model():
    return pipeline(
        "sentiment-analysis",
        model="snunlp/KR-FinBert-SC",   # 한국어 금융 감성 분석
        return_all_scores=True
    )


# 화면 구성(UI 구성)
st.title("💬 AI 텍스트 감성 분석기")
st.markdown("KR-FinBert-SC로 한국어 금융 텍스트의 감성을 분석합니다.")

with st.sidebar:
    st.header("⚙️ 설정")
    batch_mode = st.checkbox("배치 모드")
    show_scores = st.checkbox("전체 점수 표시", value=True)

# 모델 로드 (사이드바 설정과 무관하게 항상 한 번만 로드)
with st.spinner("모델 로드 중..."):
    model = load_sentiment_model()
st.success("✅ 모델 로드 완료!")

if not batch_mode:
    # 단일 텍스트 분석
    text = st.text_area(
        "분석할 텍스트를 입력하세요",
        placeholder="예: 오늘 주가가 크게 올랐습니다.",
        height=120
    )

    if st.button("분석 시작", type="primary") and text:
        with st.spinner("분석 중..."):
            raw = model(text) # [[{...}]] [{...}]
        
        if isinstance(raw[0], list):
            results = raw[0]
        else:
            results = raw

        # 결과 시각화
        labels = [r["label"] for r in results]
        scores = [r["score"] for r in results]
        best = max(results, key=lambda x: x["score"])

        col1, col2 = st.columns([1, 2])
        with col1:
            color_map = {"positive": "green", "negative": "red",
                         "neutral": "gray"}
            color = color_map.get(best["label"].lower(), "blue")
            st.markdown(
                f"<h2 style='color:{color}'>"
                f"{best['label'].upper()}</h2>",
                unsafe_allow_html=True
            )
            st.metric("신뢰도", f"{best['score']*100:.1f}%")

        with col2:
            if show_scores:
                fig = go.Figure(go.Bar(
                    x=scores,
                    y=labels,
                    orientation="h",
                    marker_color=["green" if l == "positive"
                                  else "red" if l == "negative"
                                  else "gray" for l in labels]
                ))
                fig.update_layout(
                    title="전체 레이블 점수",
                    xaxis_title="점수",
                    yaxis_title="레이블",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
    elif not text:
        st.info("👆 텍스트를 입력하고 '분석 시작' 버튼을 눌러주세요.")

else:
    # 배치 처리
    uploaded = st.file_uploader(
        "텍스트 파일 업로드 (.txt, 한 줄당 하나의 텍스트 / .csv ,로 구분)",
        type=["txt", "csv"]
    )
    if uploaded:
        texts = uploaded.read().decode("utf-8").strip().split("\n")
        st.write(f"총 {len(texts)}개 텍스트 감지")

        if st.button("배치 분석 시작", type="primary"):
            progress = st.progress(0)
            results_list = []

            for i, text in enumerate(texts):
                raw = model(text)
                
                if isinstance(raw[0], list):
                    result = raw[0]
                else:
                    result = raw
                
                best = max(result, key=lambda x: x["score"])
                results_list.append({
                    "텍스트": text[:50] + "..." if len(text) > 50 else text,
                    "감성": best["label"],
                    "신뢰도": f"{best['score']*100:.1f}%"
                })
                progress.progress((i + 1) / len(texts))

            df = pd.DataFrame(results_list)
            st.dataframe(df, use_container_width=True)

            # 감성 분포 파이 차트
            sentiment_counts = df["감성"].value_counts()
            fig = go.Figure(go.Pie(
                labels=sentiment_counts.index,
                values=sentiment_counts.values,
                hole=0.4
            ))
            fig.update_layout(title="감성 분포")
            st.plotly_chart(fig)

            # CSV 다운로드
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "📥 결과 CSV 다운로드",
                csv, "sentiment_results.csv", "text/csv"
            )
    else:
        st.info("👆 .txt 파일을 업로드해 배치 분석을 시작하세요.")