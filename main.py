from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import openai
import os
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

app = FastAPI()

# CORS for frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or replace "*" with your frontend domain on Netlify
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()

        response = openai.ChatCompletion.create(
            model=body.get("model", "mistralai/mistral-7b-instruct"),
            messages=body["messages"],
            temperature=body.get("temperature", 0.85),
            max_tokens=body.get("max_tokens", 150)
        )

        return response
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
