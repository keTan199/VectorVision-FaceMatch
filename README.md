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

## 🖥️ Live Demo (Optional)

> If deployed, add your Streamlit/Hugging Face link here  
> 🔗 [https://vectorvision-facematch.streamlit.app](#)

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

## ⚙️ System Architecture

