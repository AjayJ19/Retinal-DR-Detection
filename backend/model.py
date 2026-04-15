# ============================================================
#  RETINAL DR DETECTION — MODEL LOGIC
#  Ported from Streamlit app.py to standalone module
# ============================================================

import cv2
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import timm
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
import base64
import io
import os

# ==============================================================
# CONFIGURATION
# ==============================================================

IMG_SIZE = 512
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

# Model path — relative to project root
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "best_model.pth")

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
    0: "#2ecc71",  # Green
    1: "#f1c40f",  # Yellow
    2: "#e67e22",  # Orange
    3: "#e74c3c",  # Red
    4: "#8e44ad"   # Purple
}

DR_URGENCY = {
    0: "Low Risk",
    1: "Monitor",
    2: "Consult Doctor",
    3: "Urgent Consultation",
    4: "Immediate Attention"
}

# ==============================================================
# GLOBAL MODEL SINGLETON
# ==============================================================

_model = None
_device = None


def load_model():
    """Load trained EfficientNet-B4 model (singleton)."""
    global _model, _device

    if _model is not None:
        return _model, _device

    _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Model] Loading on device: {_device}")
    print(f"[Model] Model path: {MODEL_PATH}")

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
    checkpoint = torch.load(MODEL_PATH, map_location=_device, weights_only=False)

    # Handle DataParallel weights (keys start with "module.")
    state_dict = checkpoint["model_state"]
    new_state = {}
    for k, v in state_dict.items():
        new_key = k.replace("module.", "")
        new_state[new_key] = v

    model.load_state_dict(new_state)
    model.to(_device)
    model.eval()

    _model = model
    print("[Model] Loaded successfully!")
    return _model, _device


# ==============================================================
# PREPROCESSING
# ==============================================================

def preprocess_image(pil_image):
    """
    Apply Ben Graham preprocessing to a PIL image.

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
    mask = np.zeros_like(img)
    center = (IMG_SIZE // 2, IMG_SIZE // 2)
    radius = int(IMG_SIZE * 0.9 // 2)
    cv2.circle(mask, center, radius, (1, 1, 1), -1)
    img = (img * mask).astype(np.uint8)

    # Keep original for display
    original_rgb = img.copy()

    # Normalize for model
    mean = np.array(MEAN)
    std = np.array(STD)
    normalized = (img / 255.0 - mean) / std
    normalized = normalized.astype(np.float32)

    # To tensor (H,W,C) → (1,C,H,W)
    input_tensor = torch.tensor(normalized).permute(2, 0, 1).unsqueeze(0)

    return original_rgb, input_tensor


# ==============================================================
# PREDICTION + GRAD-CAM
# ==============================================================

def predict_and_gradcam(pil_image):
    """
    Run prediction and generate Grad-CAM heatmap.

    Returns dict with:
        grade        : int (0-4)
        grade_name   : str
        description  : str
        urgency      : str
        color        : str (hex)
        confidence   : float (0-100)
        probabilities: list of 5 floats
        preprocessed_image : base64 PNG
        gradcam_image      : base64 PNG
    """

    model, device = load_model()
    original_rgb, input_tensor = preprocess_image(pil_image)
    input_tensor = input_tensor.to(device)

    # Prediction
    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.softmax(outputs, dim=1)[0].cpu().numpy()
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

    # Encode images to base64
    preprocessed_b64 = _numpy_to_base64(original_rgb)
    gradcam_b64 = _numpy_to_base64(cam_overlay)

    return {
        "grade": pred_grade,
        "grade_name": DR_CLASSES[pred_grade],
        "description": DR_DESCRIPTIONS[pred_grade],
        "urgency": DR_URGENCY[pred_grade],
        "color": DR_COLORS[pred_grade],
        "confidence": round(float(probs[pred_grade]) * 100, 2),
        "probabilities": [
            {
                "grade": i,
                "name": DR_CLASSES[i],
                "confidence": round(float(probs[i]) * 100, 2),
                "color": DR_COLORS[i]
            }
            for i in range(5)
        ],
        "preprocessed_image": preprocessed_b64,
        "gradcam_image": gradcam_b64
    }


def _numpy_to_base64(img_array):
    """Convert a numpy RGB image to base64 PNG string."""
    img = Image.fromarray(img_array)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")
