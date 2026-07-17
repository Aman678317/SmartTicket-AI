from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import uvicorn

# Import pipeline steps
from pipeline.preprocessing import preprocess_text
from pipeline.embeddings import get_embedding
from pipeline.classifier import classify_intent
from pipeline.rag import retrieve_knowledge
from pipeline.llm_generator import generate_response

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SmartTicket AI")

# Configure CORS for frontend access (Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your Vercel URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for the frontend UI
current_dir = os.path.dirname(__file__)
static_dir = os.path.join(current_dir, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class TicketRequest(BaseModel):
    ticket_text: str

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open(os.path.join(static_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/process_ticket")
async def process_ticket(request: TicketRequest):
    ticket_text = request.ticket_text
    
    # Step 1 & 2: Preprocessing
    cleaned_text = preprocess_text(ticket_text)
    
    # Step 3: Embeddings
    embedding = get_embedding(cleaned_text)
    
    # Step 4 & 5: Intent Classification & Grouping
    classification = classify_intent(cleaned_text, embedding)
    intent = classification["intent"]
    confidence = classification["confidence"]
    group = classification["group"]
    
    # Step 6: Knowledge Retrieval (RAG)
    retrieved_doc = retrieve_knowledge(intent)
    
    # Step 7: Final Response Generation
    final_response = generate_response(ticket_text, intent, retrieved_doc)
    
    return {
        "original_ticket": ticket_text,
        "cleaned_text": cleaned_text,
        "intent": intent,
        "confidence": confidence,
        "group": group,
        "retrieved_doc_title": retrieved_doc["title"] if retrieved_doc else "None",
        "final_response": final_response
    }

if __name__ == "__main__":
    print("Starting SmartTicket AI Server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
