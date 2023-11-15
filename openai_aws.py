import json
import openai
# openai == 0.28.1 を使うこと
# AWS Lambdaのレイヤーに必要ファイルをアップロード


def lambda_handler(event, context):
    prompt = json.loads(event["body"])["prompt"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        'statusCode': 200,
        'body': response["choices"][0]["message"]["content"]
    }
