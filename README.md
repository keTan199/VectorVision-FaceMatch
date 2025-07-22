# 🔍 VectorVision-FaceMatch

**VectorVision-FaceMatch** is an AI-powered web application built with Streamlit that helps identify missing persons by matching uploaded face images against a central database. The system uses **face recognition technology**, **vector similarity search with Pinecone**, and **Google Sheets as a dynamic database**.

---

## 🎯 Project Objective

Finding missing persons is a complex problem that requires collaboration between citizens and law enforcement. The goal of **VectorVision-FaceMatch** is to:

- Provide a **simple interface** for uploading images of found individuals.
- Automatically **detect faces**, generate **face embeddings**, and search for matches in an existing database.
- Connect match results with a structured database that holds personal metadata like name, age, gender, and contact details.
- Allow for **real-time database updates** via a linked Google Form.

This tool is useful for humanitarian organizations, public volunteers, and police departments to **accelerate the identification process**.

---

## 🧠 How It Works

### 🔗 Data Collection

1. A Google Form allows citizens to **register missing persons**, including uploading a photo.
2. The responses go to a **Google Sheet**, which also contains a public **Google Drive** image link.

### 🧠 Face Recognition + Matching

1. User uploads a photo via the Streamlit app.
2. Face is detected using the `face_recognition` library.
3. A **128-d vector face embedding** is generated.
4. That embedding is compared against stored vectors in **Pinecone**, using **cosine similarity**.
5. The top match is retrieved along with metadata from the Google Sheet.

### 🔁 Database Update

- Clicking the `🔄 Update Database` button fetches **new entries** from the Google Sheet.
- It extracts face embeddings from newly submitted photos and **inserts them into Pinecone**.

---

## 📦 Features

| Feature | Description |
|--------|-------------|
| 👤 Face Detection & Embedding | Uses `face_recognition` to detect faces and generate 128-d embeddings |
| 📁 Pinecone Vector DB | Stores face embeddings and allows real-time similarity search |
| 🗂️ Google Sheets | Maintains structured metadata for all records |
| 📸 Google Drive Image Fetch | Images are accessed directly from Drive using shared links |
| 🌐 Streamlit Web UI | Clean, user-friendly interface to upload images and view results |
| 📊 Match Score | Displays similarity score along with match details |
| 🔄 Auto Database Sync | Updates embeddings and metadata in one click |

---

## 🖼️ App Interface Preview

### 📌 Project Layout

![Project Layout](https://drive.google.com/uc?export=view&id=1i6Gz-4q4lyf7LAVSKRxAVhq8A2AP7lKr)

### 🔍 Search Result Example

![Search Result](https://drive.google.com/uc?export=view&id=1lTdItMMTOHK24NDfLfeKxHmXRx303xMK)

---

## ⚙️ System Architecture

The system follows a modular architecture combining client-side user interaction with backend face processing and vector search. Here's a breakdown:

### 1. User Interface (Frontend)
- Built using **Streamlit**
- Allows users to:
  - Upload face images
  - View match results
  - Trigger database updates

### 2. Face Detection & Embedding
- Uses `face_recognition` to:
  - Detect a single face in the uploaded image
  - Generate a 128-dimensional vector (embedding)

### 3. Vector Similarity Search
- Embeddings are compared against a **Pinecone** vector database
- Uses **cosine similarity** to find the closest matches

### 4. Metadata Management
- A **Google Sheet** acts as a structured backend database
- Stores:
  - Names, age, gender, last seen location, contact info
  - Google Drive image file IDs (publicly shared)

### 5. Image Access
- Images submitted via Google Form are uploaded to **Google Drive**
- The system fetches these using direct image URLs

### 6. Auto-Sync & Update
- On clicking "🔄 Update Database":
  - New Google Sheet rows are fetched
  - Corresponding images are processed
  - Embeddings are added to the Pinecone database

