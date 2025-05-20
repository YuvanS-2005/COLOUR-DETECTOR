import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# Load color dataset once using caching
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

color_data = load_colors()

# Find closest color name using Euclidean distance
def get_color_name(R, G, B, color_data):
    min_dist = float('inf')
    closest_color = None
    for _, row in color_data.iterrows():
        try:
            d = ((R - int(row['R']))**2 + (G - int(row['G']))**2 + (B - int(row['B']))**2) * 0.5
            if d < min_dist:
                min_dist = d
                closest_color = row
        except Exception as e:
            continue
    return closest_color if closest_color is not None else pd.Series({
        'color_name': 'Unknown',
        'hex': '#000000'
    })

# Streamlit UI
st.title("🎨 Color Detection from Image (No OpenCV)")
st.markdown("Upload an image and click on a point to identify the closest matching color from the dataset.")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.write("Click on the image below to detect a color:")
    
    coords = streamlit_image_coordinates(image, key="click_image")

    if coords is not None:
        x, y = int(coords['x']), int(coords['y'])
        st.write(f"📍 Clicked Coordinates: ({x}, {y})")

        image_np = np.array(image)
        if 0 <= y < image_np.shape[0] and 0 <= x < image_np.shape[1]:
            r, g, b
