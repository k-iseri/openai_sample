from typing import AsyncIterable
import time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import dotenv_values
from openai import OpenAI

config = dotenv_values(".env")

# 初期値
assistant_id = None     # Noneか文字列
thread_id = None     # Noneか文字列


class Propmt(BaseModel):
    prompt: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=config["OPENAI_API_KEY"],
)


@app.get("/")
def index():
    return {"message": "Hello World"}


# 新しいスレッドを作成するエンドポイント
@app.post("/api/new")
def new():
    if (assistant_id is None):
        newAssistant()

    newThread()

    return {"thread_id": thread_id, "assistant_id": assistant_id}


# gptのプロンプトを受け取って結果を返すエンドポイント

@app.post("/api/chatgpt")
async def reply(data: Propmt):
    if (assistant_id is None):
        newAssistant()
        newThread()

    if (thread_id is None):
        newThread()

    return StreamingResponse(
        generate(
            human_prompt=data.prompt),
        media_type="text/event-stream",
    )


async def generate(
    human_prompt: str,
) -> AsyncIterable[str]:
    print(human_prompt)

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=human_prompt
    )

    print(message)

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    print(run)

    completed = False
    while not completed:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run.id)
        print("run.status:", run.status)
        if run.status == 'completed':
            completed = True
        else:
            time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread_id)

    messages_value_list = []

    for message in messages:
        message_content = message.content[0].text

        annotations = message_content.annotations

        citations = []

        # アノテーションを反復処理し、脚注を追加
        for index, annotation in enumerate(annotations):
            # テキストを脚注で置き換える
            message_content.value = message_content.value.replace(
                annotation.text, f' [{index}]')

            # アノテーションの種類毎に引用を収集
            if (file_citation := getattr(annotation, 'file_citation', None)):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(
                    f'[{index}] {file_citation.quote} from {cited_file.filename}')
            elif (file_path := getattr(annotation, 'file_path', None)):
                cited_file = client.files.retrieve(file_path.file_id)
                citations.append(
                    f'[{index}] Click <here> to download {cited_file.filename}')

        # ユーザーに表示する前に、メッセージの末尾に脚注を追加
        message_content.value += '\n' + '\n'.join(citations)
        messages_value_list.append(message_content.value)

    # print(messages_value_list)

    yield messages_value_list[0]


def newAssistant():
    global assistant_id
    assistant = client.beta.assistants.create(
        name="Kana Ikeda",
        instructions="池田華菜という生意気だがポジティブなアニメキャラを演じてください",
        model="gpt-4-1106-preview",
        # tools=[{"type": "retrieval"}], # retrievalを使う場合
        # file_ids=[file_id]

    )
    assistant_id = assistant.id
    print(assistant_id)


def newThread():
    global thread_id
    thread = client.beta.threads.create()
    thread_id = thread.id
    print(thread_id)


# CORS対応
@app.options("/api/chatgpt")
def option():
    return {}
