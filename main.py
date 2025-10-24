from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils.youtube_utils import extract_video_id, fetch_transcript
from utils.qa_pipeline import get_answer

app = FastAPI(title="🎥 YouTube Q&A with LLM")

# ✅ Allow frontend access (React, Streamlit, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class YouTubeQuery(BaseModel):
    url: str
    question: str

@app.post("/youtube_qa")
async def youtube_qa(query: YouTubeQuery):
    """Main API endpoint."""
    video_id = extract_video_id(query.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL.")
    
    try:
        transcript = fetch_transcript(video_id)
        if not transcript:
            raise HTTPException(status_code=404, detail="No transcript found.")
        
        answer = get_answer(transcript, query.question, video_id)
        return {"video_id": video_id, "question": query.question, "answer": answer}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

