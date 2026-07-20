# Dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir \
    streamlit \
    numpy pandas matplotlib plotly \
    torch torchvision \
    transformers \
    pillow
EXPOSE 8501