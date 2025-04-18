from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from backend.api.schema.payload import Payload
from backend.utils.CharmAssistantWrapper import CharmAssistantWrapper
import json

app = FastAPI()
assistant = CharmAssistantWrapper()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/prompt")
async def prompt(payload: Payload) -> Response:
    message = assistant.run_prompt(payload.prompt, payload.context, payload.auth)
    return {
        "message": message,
    }
