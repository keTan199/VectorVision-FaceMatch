import numpy as np
import cv2
import pandas as pd
import requests
import face_recognition as fc
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from pinecone import Pinecone, ServerlessSpec
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
google_json_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH")
sheet_id = os.getenv("GOOGLE_SHEET_ID")

# === Pinecone Initialization ===

pc = Pinecone(api_key=pinecone_api_key)

index_name = "face-data-matching"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=128,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Connect to the index
index = pc.Index(index_name)

# === Google Sheets Setup ===
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
file = google_json_path
credentials = ServiceAccountCredentials.from_json_keyfile_name(file, scope)
gc = gspread.authorize(credentials)
sheet = gc.open("Missing Person Data Base").worksheet("Facenet_model")

# === Download Image from Google Drive ===
def download_image_from_drive(file_id):
    url = f'https://drive.google.com/uc?id={file_id}'
    response = requests.get(url)
    if response.status_code == 200:
        nparr = np.frombuffer(response.content, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return None

# === Face Detection and Embedding ===
def detect_face_and_generate_embedding(cv2_img):
    face_locations = fc.face_locations(cv2_img)
    if face_locations:
        return fc.face_encodings(cv2_img, known_face_locations=[face_locations[0]])[0]
    return None

# === Pinecone Search ===
def query_pinecone_index(face_embedding):
    response = index.query(
        vector=face_embedding.tolist(),
        top_k=2,
        include_metadata=True
    )
    return response.get("matches", [])

# === Fetch Match Metadata ===
def get_match_details(user_id):
    df = pd.DataFrame(sheet.get_all_records())
    row = df[df["user_id"] == user_id]
    return row.iloc[0].to_dict() if not row.empty else None


def image_to_base64(image):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


def download_and_read_image_from_drive(file_id):
    url = f'https://drive.google.com/uc?id={file_id}'
    response = requests.get(url)
    
    if response.status_code == 200:
        image_bytes = response.content
        nparr = np.frombuffer(image_bytes, np.uint8)
        cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Decoded OpenCV image

        # Optional: encode image to .jpg bytes for storage or transfer
        success, img_encoded = cv2.imencode('.jpg', cv2_img)
        if not success:
            print("OpenCV image encoding failed")
            return None, None

        # Face encoding using face_recognition
        face_locations = fc.face_locations(cv2_img)
        if face_locations:
            face_embedding = fc.face_encodings(cv2_img, known_face_locations=[face_locations[0]])[0]
        else:
            face_embedding = None

        return cv2_img, face_embedding  # OpenCV image array and face embedding (numpy array)
    else:
        print("Failed to download the image.")
        return None, None


def constant_update_data_base(sheet_id, sheet_name):   
    #sheet_id = "1AXF9hMJr4zdAkoNlPIwmCZhJ9_E-0JD2lNoRSRKnBf4"
    #sheet_name = "Missing_Database"
    sheet_id = sheet_id
    sheet_name = sheet_name
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)

    df_2 = pd.DataFrame(sheet.get_all_records())
    if df_2.empty:
        df_2 = pd.DataFrame(columns=[
            'Timestamp', 'Type', 'Name', 'Gender', 'Age', 'Missing Since',
            'Contact Detail', 'Email Address', 'g_id', 'user_id'
        ])

    if len(df) > len(df_2):
        for i in range(len(df_2), len(df)):
            photo = df["Photo"][i]
            id = photo.split("=")[1]
            google_id = id
            id_part = id[:3]
            age_str = f"{df['Age'][i]:02d}"
            generated_id = id_part + age_str   

            # Read image and generate face encoding
            cv2encode, face_encode = download_and_read_image_from_drive(id)
            if face_encode is None:
                print(f"Face not detected in image ID {id}, skipping.")
                continue

            # Upload to Pinecone
            index.upsert([{
                "id": generated_id,
                "values": face_encode.tolist(),
                "metadata": {
                    "user_id": generated_id,
                    "google_id": google_id
                }
            }])

    
            new_data = {
            'Timestamp': [df["Timestamp"][i]],
            'Type': [df["Type"][i]],
            'Name': [df["Name"][i]],
            'Gender': [df["Gender"][i]],
            'Age': [df["Age"][i]],
            'Missing Since': [df["Missing Since"][i]],
            'Contact Detail': [df["Contact Detail"][i]],
            'Email Address': [df["Email Address"][i]],
            'g_id': [id],
            'user_id': [generated_id]}   

            data = pd.DataFrame(new_data)
            pd_concat = pd.concat([df_2, data]).reset_index(drop=True)
            columns_to_keep = [
            'Timestamp', 'Type', 'Name', 'Gender', 'Age', 'Missing Since',
            'Contact Detail', 'Email Address', 'g_id', 'user_id']
            df_2 = pd_concat[columns_to_keep]   
            set_with_dataframe(sheet, df_2, include_index=False, include_column_header=True)    


