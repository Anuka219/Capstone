from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path

app_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(app_root))

from Ai_chatbot_Capstone import SimpleChatbot

app = FastAPI(title="MEM Guide Bot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = SimpleChatbot(name="MEM Guide Bot")

class Message(BaseModel):
    message: str

class Response(BaseModel):
    response: str

@app.post("/api/chat", response_model=Response)
async def chat(msg: Message):
    """Handle chat messages."""
    if not msg.message or not msg.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        response = bot.reply(msg.message)
        return Response(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    print("Starting MEM Guide Bot backend on http://localhost:8000")
    print("API docs available at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
