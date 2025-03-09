import os
import openai
from dotenv import load_dotenv

# .env ファイルをロード
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


# OpenAI APIを使って質問に回答
def answer_with_openai(inputs: dict) -> dict:
    state = inputs["state"]
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": state["question"]}]
    )
    state["openai_response"] = response.choices[0].message.content
    print('answer_with_openai')
    print(state["openai_response"] ,)
    return {"state": state}


# OpenAI APIを使って回答が十分かを判定
def check_response_quality(inputs: dict) -> dict:
    print("check_response_quality!!!")
    state = inputs["state"]
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "以下の回答が十分か、それともインターネット検索が必要か判断してください。"},
            {"role": "user", "content": f"質問: {state['question']}\n"
                                         f"回答: {state['openai_response']}\n\n"
                                         "この回答で十分なら「NO」と答えてください。\n"
                                         "情報が不十分で検索が必要なら「YES」と答えてください。"}
            ]
    )
    state["need_search"] = "No" not in response.choices[0].message.content
    next = "search_with_perplexity" if state["need_search"] else "summarize_with_openai"
    state["next"] = next
    print('check_response_quality')
    print(state,)
    return {"state": state, "next": next}


# OpenAI APIで最終的な回答を要約
def summarize_with_openai(inputs: dict) -> dict:
    print('summarize_with_openai')
    state = inputs["state"]
    content_to_summarize = state["openai_response"]
    if state["need_search"]:
        content_to_summarize += "\n" + state["perplexity_response"]

    content_to_summarize = state["perplexity_response"] if state["need_search"] else state["openai_response"]

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"次の文章を50トークン以内で要約してください:\n\n{content_to_summarize}"}]
    )
    state["final_summary"] = response.choices[0].message.content
    print(state["final_summary"],)
    return {"state": state}
