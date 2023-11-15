import openai
from dotenv import dotenv_values

config = dotenv_values(".env")

openai.api_key = config["OPENAI_API_KEY"]

# ファイルをアップロードする
file_object = openai.File.create(
    file=open("ikeda-01.jsonl", "rb"),  # ファイル名を必要に応じて書き換える
    purpose='fine-tune'
)

print(file_object)

file_id = file_object.id

# ジョブを始める
job_response = openai.FineTuningJob.create(
    training_file=file_id, model="gpt-3.5-turbo-0613")

print(job_response)

job_id = job_response.id
