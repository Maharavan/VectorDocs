<p align="center">
  <img src="assets/logo.png" alt="VectorDocs Logo" width="120"/>
</p>

<h1 align="center">VectorDocs 🧠🤖</h1>

<p align="center">
  <b>Hybrid Retrieval-Augmented Document Intelligence Assistant</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/RAG-Embeddings%20%2B%20BM25-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Framework-Streamlit-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Vector%20Store-FAISS-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LLM-GPT--4o--mini-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

<p align="center">
  <a href="https://github.com/Maharavan/VectorDocs/stargazers">
    <img src="https://img.shields.io/github/stars/Maharavan/VectorDocs?style=social" />
  </a>
  <a href="https://github.com/Maharavan/VectorDocs/forks">
    <img src="https://img.shields.io/github/forks/Maharavan/VectorDocs?style=social" />
  </a>
</p>

---

## 🚀 Overview

**VectorDocs** is a **session-aware Retrieval-Augmented Generation (RAG) assistant** that allows users to upload documents (**PDF / TXT / JSON**) and interact with them conversationally.

Unlike basic vector-only RAG systems, VectorDocs uses a **hybrid retrieval pipeline** combining semantic embeddings, keyword search, and cross-encoder reranking to deliver **accurate, grounded answers with reduced hallucinations**.

---

## 🧠 Why VectorDocs?

Traditional RAG systems often:

* Miss exact keywords (IDs, logs, error codes)
* Retrieve loosely related chunks
* Hallucinate when context is weak

**VectorDocs solves this by design.**

### 🔬 Hybrid Retrieval Pipeline

```
FAISS (Semantic Recall)
      +
BM25 (Keyword Precision)
      ↓
Cross-Encoder Reranking
      ↓
Hallucination-Guarded Answering
```

---

## ✨ Features

| Feature                | Description                          |
| ---------------------- | ------------------------------------ |
| 📂 Session Isolation   | Independent document index per chat  |
| 🔍 Hybrid Retrieval    | FAISS + BM25                         |
| 🧠 Reranking           | `ms-marco-MiniLM-L-6-v2`             |
| 🛡 Hallucination Guard | Context-validated answers            |
| 🗂 File Support        | PDF, TXT, JSON                       |
| 💾 Local Cache         | Persistent FAISS + BM25              |
| 💬 Chat Sessions       | Switch chats without losing progress |
| 🧩 Modular Codebase    | Easy to extend                       |

---

## 🏗 Architecture

```
User
 ↓
Streamlit UI
 ↓
Loader & Chunker
 ↓
Hybrid Retrieval Engine
  ├─ FAISS
  ├─ BM25
  └─ Cross-Encoder
 ↓
LLM (Answer + Validation)
```

---

## 📁 Project Structure

```
VectorDocs/
│── app/
│   ├── main.py
│   ├── components/
│   └── utility/
│── loader/
│── vector_store/
│── embeddings/
│── assets/
│   ├── logo.png
│   └── screenshots/
│── data/
│── LICENSE
│── README.md
│── requirements.txt
```

---

## ⚙️ Installation & Run (Local)

### 1️⃣ Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate     # Linux / Mac
.venv\Scripts\activate        # Windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the App

```bash
streamlit run app/main.py
```

Open 👉 **[http://localhost:8501](http://localhost:8501)**

---

## 🐳 Run with Docker Image

Pull the published image directly from Docker Hub:

```bash
docker pull mahar628/vectordocs:latest
```

Run the application:

```bash
docker run --rm -p 8501:8501 mahar628/vectordocs:latest
```

Open 👉 **[http://localhost:8501](http://localhost:8501)**

---

## 🔑 Setting `OPENAI_API_KEY` (Streamlit UI)

VectorDocs allows you to **set the OpenAI API key directly from the Streamlit web interface**.

### 🧭 Steps

1. Launch the app
2. In the **sidebar**, find **“OpenAI API Key”**
3. Paste your key:

   ```
   sk-********************************
   ```
4. Press **Enter / Save**

### 🔐 Security Notes

* Stored only in **Streamlit session state**
* Isolated per browser session
* Never written to disk or source code
* Cleared on app restart

---

## 📤 Uploading Documents

Supported formats:

* 📄 PDF
* 📜 TXT
* 🧾 JSON

### Workflow

1. Upload files from the **sidebar**
2. Files are:

   * Parsed
   * Chunked
   * Indexed using **FAISS + BM25**
3. Uploads can be incremental — indexes update automatically

---

## 💬 Chat-Based Sessions

Each chat session maintains:

* Independent document uploads
* Separate FAISS + BM25 indexes
* Its own conversation history

You can switch between chats without losing progress.

---

## 🖼 UI Preview

<p align="center">
  <img src="assets/screenshots/home.png" width="100%" />
</p>

---

## 📝 Featured Article

I wrote about the motivation behind VectorDocs, the problems I encountered with existing **Chat-with-PDF applications**, and why I decided to build my own document Q&A system.

👉 **[Why I Stopped Trusting Chat-with-PDF Apps and Built My Own](https://medium.com/@maharavan10/why-i-stopped-trusting-chat-with-pdfs-apps-and-built-my-own-e5d3859f3b4b)**

> Explore the journey behind VectorDocs — from the limitations of existing PDF chat tools to building a more transparent and controllable document intelligence application.

---

## 📜 License

Licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---

⭐ **Star the repository if you find this project useful!**
