from fastapi import FastAPI
from openai import OpenAI
import os
from pydantic import BaseModel

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

class PromptRequest(BaseModel):
    prompt: str
    model: str = "deepseek/deepseek-r1-distill-qwen-7b"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate")
async def generate_completion(request: PromptRequest):
    try:
        messages = [{"role": "user", "content": request.prompt}]
        response = client.chat.completions.create(
            model=request.model,
            messages=messages,
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}


