import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import pandas as pd

# Load model
model = load_model(r'C:/Users/Admin/app/casting_defect_model.h5')

# Streamlit UI (styling and titles)
st.set_page_config(page_title="Casting Defect Detection", page_icon="🔍", layout="centered")
st.title("🔍 Casting Defect Detection App")
st.write("Welcome to the Casting Defect Detection app. Upload casting images to check for defects.")

# Upload multiple images
uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Initialize empty list for saving results
results = []

if uploaded_files:
    # Loop through all uploaded files
    for uploaded_file in uploaded_files:
        # Convert the uploaded image to RGB (in case it has an alpha channel)
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)

        # Preprocess the image for prediction
        img = img.resize((224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Prediction
        prediction = model.predict(img_array)
        score = prediction[0][0]

        # Prepare result
        if score > 0.5:
            result = "No Defect"
            st.success(f"✅ No Defect Detected for {uploaded_file.name} | Confidence: {score:.4f}")
        else:
            result = "Defect"
            st.error(f"❌ Defect Detected for {uploaded_file.name} | Confidence: {score:.4f}")

        # Append result to list
        results.append([uploaded_file.name, result, score])

    # Save all results to CSV when button is clicked
    if st.button("Save Results to CSV"):
        # Convert list of results to DataFrame
        df = pd.DataFrame(results, columns=['Image', 'Prediction', 'Score'])
        df.to_csv('detection_results.csv', mode='a', header=False, index=False)
        st.write(f"Results saved to detection_results.csv")
