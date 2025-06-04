import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ASSISTANT_ID = "asst_26tDokOOEKfkYT2xJJnJ68rasst_qNcdXrPtnsDuzfxZdt0K3WMQ"

pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Madi_s_Resume.pdf")

print("📦 Загружаем PDF...")
uploaded_file = client.files.create(
    file=open(pdf_path, "rb"),
    purpose="assistants"
)
print(f"✅ Файл загружен с id: {uploaded_file.id}")

assistant = client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)
client.beta.assistants.update(
    assistant_id=ASSISTANT_ID,
    tools=[{"type": "retrieval"}],
    files=[uploaded_file.id]
)
print("✅ Файл добавлен к ассистенту")

def ask_question(question: str):
    # Создаём поток (thread)
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
        stream=False
    )

    while run.status not in ["completed", "failed"]:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    answer_content = messages.data[-1].content[0]
    answer_text = answer_content.text.value
    print("🧠 Ответ:\n", answer_text)

    annotations = answer_content.text.annotations
    if annotations:
        print("\n📚 Источники:")
        for ann in annotations:
            chunk_id = ann.file_citation.chunk_id if ann.file_citation else "Unknown chunk"
            file_ref = ann.file_citation.file_id if ann.file_citation else "Unknown file"
            print(f"– chunk: {chunk_id} from file: {file_ref}")
    else:
        print("\n❌ Нет ссылок на PDF.")

if __name__ == "__main__":
    question = input("Задай вопрос: ")
    ask_question(question)
