# 🎥 YouTube Q&A Chatbot with LLM

This is a **YouTube Q&A Chatbot** powered by a Large Language Model (LLM) and FastAPI.  
Users can enter a YouTube video URL and ask questions — the system generates accurate answers using the video transcript.

---

## 🔹 Features

- Ask questions about any YouTube video.
- Extracts video transcript automatically.
- Generates answers using an LLM (Hugging Face API or other supported models).
- **Clean and responsive UI** similar to ChatGPT:
  - Fixed input box at the bottom
  - Scrollable chat messages
  - Enter key or send button to submit queries
- Frontend built with **HTML, CSS, and JavaScript**
- Backend built with **FastAPI** and Python
- CORS enabled for frontend-backend communication

---

## 📂 Project Structure


## ⚡ How it Works

1. **User enters a YouTube URL** and their question in the chatbot UI.
2. Frontend sends a POST request to the FastAPI backend at `/youtube_qa`.
3. Backend uses `youtube_utils.py` to:
   - Extract the video ID from the URL
   - Fetch the transcript of the video
4. The transcript and user query are sent to `qa_pipeline.py` which:
   - Uses an LLM to generate a relevant answer
5. Backend returns the answer as JSON
6. Frontend displays the user question and bot answer in the chat window.

---

## 🖼️ Screenshots

### Chatbot UI Form Example 1
![Chatbot Form 1](static/images/form1.png)

### Chatbot UI Form Example 2
![Chatbot Form 2](static/images/form.png)

---

## 💻 Installation

1. Clone the repository:
```bash
git clone https://github.com/aliahmad552/youtube-transcript-rag.git
cd youtube-transcript-rag
