# ============================================================
#  RETINAL DISEASE DETECTION — STREAMLIT WEB APP
#  File: app.py
#  Run: streamlit run app.py
# ============================================================

import cv2
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import timm
import albumentations as A
from albumentations.pytorch import ToTensorV2
import streamlit as st
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
import matplotlib.pyplot as plt
import io


# ==============================================================
# CONFIGURATION
# ==============================================================

IMG_SIZE   = 512
MEAN       = [0.485, 0.456, 0.406]
STD        = [0.229, 0.224, 0.225]
MODEL_PATH = "best_model.pth"

DR_CLASSES = {
    0: "No DR",
    1: "Mild DR",
    2: "Moderate DR",
    3: "Severe DR",
    4: "Proliferative DR"
}

DR_DESCRIPTIONS = {
    0: "No signs of diabetic retinopathy detected. The retina appears healthy.",
    1: "Mild non-proliferative DR detected. Small microaneurysms present. Monitor regularly.",
    2: "Moderate non-proliferative DR detected. More widespread vascular changes. Consult a specialist.",
    3: "Severe non-proliferative DR detected. Significant vascular damage. Urgent specialist consultation recommended.",
    4: "Proliferative DR detected. Abnormal new blood vessel growth. Immediate medical attention required."
}

DR_COLORS = {
    0: "#2ecc71",   # Green
    1: "#f1c40f",   # Yellow
    2: "#e67e22",   # Orange
    3: "#e74c3c",   # Red
    4: "#8e44ad"    # Purple
}

DR_URGENCY = {
    0: "✅ Low Risk",
    1: "⚠️ Monitor",
    2: "⚠️ Consult Doctor",
    3: "🚨 Urgent Consultation",
    4: "🚨 Immediate Attention"
}


# ==============================================================
# MODEL LOADING (cached so it only loads once)
# ==============================================================

@st.cache_resource
def load_model():
    """
    Load trained EfficientNet-B4 model.
    @st.cache_resource ensures model loads only once,
    not on every user interaction.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Build same architecture as training
    model = timm.create_model(
        "efficientnet_b4",
        pretrained=False,
        num_classes=0,
        drop_rate=0.3
    )
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(model.num_features, 5)
    )

    # Load saved weights
    checkpoint = torch.load(MODEL_PATH, map_location=device, weights_only=False)

    # Handle DataParallel weights (keys start with "module.")
    state_dict = checkpoint["model_state"]
    new_state  = {}
    for k, v in state_dict.items():
        new_key = k.replace("module.", "")   # Remove DataParallel prefix
        new_state[new_key] = v

    model.load_state_dict(new_state)
    model.to(device)
    model.eval()

    return model, device


# ==============================================================
# PREPROCESSING
# ==============================================================

def preprocess_image(pil_image):
    """
    Apply Ben Graham preprocessing to a PIL image.

    Args:
        pil_image : PIL.Image uploaded by user

    Returns:
        original_rgb : numpy array for display
        input_tensor : torch.Tensor for model
    """

    # Convert PIL to numpy BGR for OpenCV
    img = np.array(pil_image.convert("RGB"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Resize
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)

    # BGR → RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Ben Graham enhancement
    img = cv2.addWeighted(
        img, 4,
        cv2.GaussianBlur(img, (0, 0), 10), -4,
        128
    )

    # Circular mask
    mask   = np.zeros_like(img)
    center = (IMG_SIZE // 2, IMG_SIZE // 2)
    radius = int(IMG_SIZE * 0.9 // 2)
    cv2.circle(mask, center, radius, (1, 1, 1), -1)
    img = (img * mask).astype(np.uint8)

    # Keep original for display
    original_rgb = img.copy()

    # Normalize for model
    mean = np.array(MEAN)
    std  = np.array(STD)
    normalized = (img / 255.0 - mean) / std
    normalized = normalized.astype(np.float32)

    # To tensor (H,W,C) → (1,C,H,W)
    input_tensor = torch.tensor(normalized).permute(2, 0, 1).unsqueeze(0)

    return original_rgb, input_tensor


# ==============================================================
# PREDICTION + GRAD-CAM
# ==============================================================

def predict_and_gradcam(pil_image, model, device):
    """
    Run prediction and generate Grad-CAM heatmap.

    Returns:
        pred_grade   : int, predicted DR grade (0-4)
        probs        : list of 5 confidence scores
        cam_overlay  : numpy array, heatmap overlaid on image
        original_rgb : numpy array, preprocessed original
    """

    original_rgb, input_tensor = preprocess_image(pil_image)
    input_tensor = input_tensor.to(device)

    # Prediction
    with torch.no_grad():
        outputs = model(input_tensor)
        probs   = torch.softmax(outputs, dim=1)[0].cpu().numpy()
        pred_grade = int(outputs.argmax(dim=1).item())

    # Grad-CAM
    target_layers = [model.blocks[-1][-1]]
    cam = GradCAM(model=model, target_layers=target_layers)
    grayscale_cam = cam(
        input_tensor=input_tensor,
        targets=[ClassifierOutputTarget(pred_grade)]
    )[0]

    original_float = original_rgb / 255.0
    cam_overlay = show_cam_on_image(original_float, grayscale_cam, use_rgb=True)

    return pred_grade, probs, cam_overlay, original_rgb


# ==============================================================
# STREAMLIT UI
# ==============================================================

def main():

    # ── Page config ───────────────────────────────────────────
    st.set_page_config(
        page_title="Retinal DR Detection",
        page_icon="🔬",
        layout="wide"
    )

    # ── Header ────────────────────────────────────────────────
    st.title("🔬 AI-Powered Retinal Disease Detection")
    st.markdown(
        "Upload a **retinal fundus image** to detect the severity of "
        "**Diabetic Retinopathy** using EfficientNet-B4."
    )
    st.markdown("---")

    # ── Sidebar info ──────────────────────────────────────────
    with st.sidebar:
        st.header("About This App")
        st.markdown("""
        **Model:** EfficientNet-B4

        **Dataset:** APTOS 2019 (3,662 images)

        **Test Kappa:** 0.8612

        **Test Accuracy:** 79.82%

        ---
        **DR Severity Scale:**
        - 🟢 Grade 0 — No DR
        - 🟡 Grade 1 — Mild
        - 🟠 Grade 2 — Moderate
        - 🔴 Grade 3 — Severe
        - 🟣 Grade 4 — Proliferative

        ---
        ⚠️ *This tool is for screening
        assistance only. Always consult
        a qualified ophthalmologist.*
        """)

    # ── File uploader ─────────────────────────────────────────
    uploaded_file = st.file_uploader(
        "Upload Retinal Fundus Image",
        type=["jpg", "jpeg", "png"],
        help="Upload a high-quality retinal fundus photograph"
    )

    if uploaded_file is not None:

        # Load image
        pil_image = Image.open(uploaded_file)

        # Show uploaded image
        col_upload, col_info = st.columns([1, 2])
        with col_upload:
            st.subheader("Uploaded Image")
            st.image(pil_image, use_container_width=True)

        with col_info:
            st.subheader("Image Details")
            st.write(f"**Filename:** {uploaded_file.name}")
            st.write(f"**Size:** {pil_image.size[0]} × {pil_image.size[1]} pixels")
            st.write(f"**Format:** {pil_image.format or 'PNG/JPG'}")

        st.markdown("---")

        # Analyze button
        if st.button("🔍 Analyze Image", type="primary", use_container_width=True):

            with st.spinner("Analyzing retinal image..."):

                # Load model
                model, device = load_model()

                # Run prediction + Grad-CAM
                pred_grade, probs, cam_overlay, original_rgb = predict_and_gradcam(
                    pil_image, model, device
                )

            # ── Results ───────────────────────────────────────
            st.markdown("---")
            st.subheader("📊 Analysis Results")

            # Main result box
            grade_color  = DR_COLORS[pred_grade]
            grade_name   = DR_CLASSES[pred_grade]
            grade_urgency = DR_URGENCY[pred_grade]
            confidence   = probs[pred_grade] * 100

            st.markdown(
                f"""
                <div style="
                    background-color: {grade_color}22;
                    border-left: 6px solid {grade_color};
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                ">
                    <h2 style="color: {grade_color}; margin: 0;">
                        Grade {pred_grade}: {grade_name}
                    </h2>
                    <p style="font-size: 18px; margin: 8px 0;">
                        {grade_urgency} &nbsp;|&nbsp; Confidence: <b>{confidence:.1f}%</b>
                    </p>
                    <p style="margin: 0; color: #555;">
                        {DR_DESCRIPTIONS[pred_grade]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # ── Image columns ─────────────────────────────────
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Preprocessed Image")
                st.image(original_rgb, use_container_width=True,
                         caption="Ben Graham enhanced retinal image")

            with col2:
                st.subheader("Grad-CAM Heatmap")
                st.image(cam_overlay, use_container_width=True,
                         caption="Red = regions influencing prediction")

            # ── Confidence chart ──────────────────────────────
            st.subheader("Confidence per DR Grade")

            fig, ax = plt.subplots(figsize=(10, 3))
            colors = [DR_COLORS[i] for i in range(5)]
            bars   = ax.bar(list(DR_CLASSES.values()), probs * 100, color=colors)
            ax.set_ylabel("Confidence (%)")
            ax.set_ylim(0, 100)
            ax.set_title("Model Confidence Distribution")
            for bar, p in zip(bars, probs):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 1,
                    f"{p*100:.1f}%",
                    ha="center", va="bottom", fontsize=9
                )
            plt.tight_layout()
            st.pyplot(fig)

            # ── Disclaimer ────────────────────────────────────
            st.markdown("---")
            st.warning(
                "⚠️ **Medical Disclaimer:** This AI tool is intended for "
                "screening assistance only and does not replace professional "
                "medical diagnosis. Please consult a qualified ophthalmologist "
                "for any medical decisions."
            )

    else:
        # Show instructions when no image uploaded
        st.info("👆 Upload a retinal fundus image above to get started.")

        st.markdown("### How to use:")
        st.markdown("""
        1. Click **Browse files** and upload a retinal fundus image (JPG or PNG)
        2. Click **Analyze Image**
        3. View the DR severity grade, confidence score, and Grad-CAM heatmap
        4. The heatmap shows which retinal regions the model focused on
        """)


if __name__ == "__main__":
    main()
