import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

assistant = client.beta.assistants.create(
    name="Study Q&A Assistant",
    instructions="You are a helpful tutor. Use the knowledge in the attached files to answer questions. Cite sources where possible.",
    model="gpt-4o-mini",
    tools=[{"type": "file_search"}]
)
print("✅ Assistant создан:")
print("Assistant ID:", assistant.id)
