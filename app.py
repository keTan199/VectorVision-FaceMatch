import streamlit as st
import numpy as np
import cv2
from PIL import Image

from utils import (
    detect_face_and_generate_embedding,
    query_pinecone_index,
    get_match_details,
    download_image_from_drive,
    constant_update_data_base,
    download_and_read_image_from_drive
)

# Page configuration
st.set_page_config(page_title="Face Matching App", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .centered-heading {
        text-align: center;
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 1em;
    }
    .stImage > img {
        border-radius: 10px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="centered-heading">🔍 Face Matching - Missing Persons Project</div>', unsafe_allow_html=True)

# Register Complaint and Update Database Buttons - Right aligned and equal size
spacer, btn_col1, btn_col2 = st.columns([6, 1, 1])

with btn_col1:
    st.markdown(
        """
        <a href="https://forms.gle/vQboAKC6vS2k2WrL8" target="_blank">
            <button style="width: 100%; padding: 0.5em 1em; font-size: 1em;">📝 Register for Complaint</button>
        </a>
        """,
        unsafe_allow_html=True
    )

with btn_col2:
    if st.button("🔄 Update Database"):
        with st.spinner("Updating database with new entries..."):
            try:
                constant_update_data_base()
                st.success("✅ Database successfully updated.")
            except Exception as e:
                st.error(f"❌ Failed to update database: {str(e)}")


# Columns for image upload
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Upload Photo")
    uploaded_image = st.file_uploader("📤 Choose an image", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")

    if uploaded_image:
        image = Image.open(uploaded_image).convert("RGB")
        resized_uploaded_img = image.resize((500, 500))
        
        # Convert to OpenCV format
        cv2_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        face_embedding = detect_face_and_generate_embedding(cv2_img)

        if face_embedding is not None:
            matches = query_pinecone_index(face_embedding)

            if matches:
                match = matches[0]
                user_id = match["metadata"]["user_id"]
                score = match["score"]
                match_details = get_match_details(user_id)

                if match_details:
                    # Show uploaded and matched images first
                    st.markdown("### 🖼️ Uploaded Image vs Matched Image")
                    col_uploaded, col_matched = st.columns(2)

                    with col_uploaded:
                        st.image(resized_uploaded_img, caption="Uploaded Image (500x500)", use_container_width=True)

                    with col_matched:
                        database_img = download_image_from_drive(match["metadata"]["google_id"])
                        if database_img is not None:
                            try:
                                database_img_pil = Image.fromarray(cv2.cvtColor(database_img, cv2.COLOR_BGR2RGB)).convert("RGB")
                                resized_match_img = database_img_pil.resize((500, 500))
                                st.image(resized_match_img, caption="Matched Image (500x500)", use_container_width=True)
                            except Exception as e:
                                st.error(f"Error processing matched image: {str(e)}")
                        else:
                            st.warning("⚠️ Matched image not found.")

                    # Now show match details
                    st.markdown("### 🔍 Match Details")
                    match_info = {
                        "Field": ["Name", "Gender", "Age", "Missing Since", "Contact", "Match Score"],
                        "Value": [
                            match_details.get("Name", "N/A"),
                            match_details.get("Gender", "N/A"),
                            match_details.get("Age", "N/A"),
                            match_details.get("Missing Since", "N/A"),
                            match_details.get("Contact Detail", "N/A"),
                            f"{score:.4f}"
                        ]
                    }
                    st.table(match_info)
                else:
                    st.warning("⚠️ Match metadata not found.")
            else:
                st.info("No matches found.")
        else:
            st.error("😢 No face detected.")
