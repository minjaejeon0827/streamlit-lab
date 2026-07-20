# utils/model_utils.py 예시
import streamlit as st
import torch
import torchvision.models as models

@st.cache_resource
def load_model(model_name: str):
    if model_name == "ResNet-50":
        model = models.resnet50(
            weights=models.ResNet50_Weights.IMAGENET1K_V1
        )
    model.eval()
    return model

def predict(model, image_tensor, top_k: int = 5):
    with torch.no_grad():
        outputs = model(image_tensor)
        probs = torch.softmax(outputs, dim=1)
        top_probs, top_indices = probs.topk(top_k)
    return top_probs[0].numpy(), top_indices[0].numpy()