import os
import openai
from dotenv import load_dotenv

# .env ファイルをロード
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Perplexity クライアントを作成
perplexity_client = openai.OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")


# Perplexity APIを使って検索
def search_with_perplexity(inputs: dict) -> dict:
    state = inputs["state"]

    response = perplexity_client.chat.completions.create(
        model="sonar",
        messages=[{
            "role": "system",
            "content": "あなたは検索が得意な AI の「田所」です。江戸っ子なしゃべり方をします。",
        },
        {
            "role": "user",
            "content": state["question"],
        },]
    )
    state["perplexity_response"] = response.choices[0].message.content
    print('Perplexity >>',state["perplexity_response"],)
    return {"state": state}
