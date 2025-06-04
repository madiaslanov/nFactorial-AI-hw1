import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Note(BaseModel):
    id: int = Field(..., ge=1, le=10)
    heading: str = Field(..., example="Mean Value Theorem")
    summary: str = Field(..., max_length=150)
    page_ref: Optional[str] = Field(None, description="Page reference in source PDF")

def generate_notes():
    system = (
        "You are a study summarizer. "
        "Return exactly 10 unique notes that will help prepare for the exam. "
        "Each note must contain: id (1 to 10), heading (short title), summary (concise, max 150 chars), and optional page_ref. "
        "Respond *only* with valid JSON of this format: {\"notes\": [Note, Note, ...]}."
    )
    user_prompt = "Based on the uploaded study materials, generate 10 revision notes as described."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"}
    )

    data = json.loads(response.choices[0].message.content)
    notes = [Note(**item) for item in data["notes"]]

    print("\n✅ Сгенерированные заметки:")
    for note in notes:
        print(f"[{note.id}] {note.heading} (p. {note.page_ref})\n→ {note.summary}\n")

if __name__ == "__main__":
    generate_notes()
