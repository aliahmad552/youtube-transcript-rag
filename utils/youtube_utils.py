import re
import os
import json
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats."""
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

def fetch_transcript(video_id: str) -> str:
    """Fetch or load cached YouTube transcript."""
    os.makedirs("cache", exist_ok=True)
    cache_path = f"cache/{video_id}.json"

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f).get("transcript")

    try:
        fetched = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
        raw_transcript = fetched.to_raw_data()
        transcript = "".join(entry["text"] for entry in raw_transcript)

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump({"transcript": transcript}, f)
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return None

