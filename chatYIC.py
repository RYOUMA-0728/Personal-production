import streamlit as st
from openai import OpenAI
import requests
import json

# 定数設定
SYSTEM_ACTIONS = ["使用する", "使用しない"]
SYSTEM_ROLE = "system"    # 優先的に反映されるプロんプト。最新のOpen AI APIではDeveloperに変更されている
USER_ROLE = "user"        # 人間が入力したプロンプト
AI_ROLE = "assistant"     # AIが入力したプロンプト
SERVER = "10.146.102.96"  # ollamaサーバ
#SERVER = "localhost"

# ollamaのモデル取得
if "LLM_MODELS" not in st.session_state:
  st.session_state.LLM_MODELS = []
  obj = json.loads(requests.get("http://" + SERVER + ":11434/api/tags").text)
  for model in obj['models']:
    st.session_state.LLM_MODELS.append(model['name'])

# 画面左側のSidebar設定
selected_model = st.sidebar.selectbox("LLM 切り替え", st.session_state.LLM_MODELS, index=0)
system_prompt_enabled = st.sidebar.selectbox("System プロンプト", SYSTEM_ACTIONS, index=1)
if system_prompt_enabled == "使用する":
  system_prompt = st.sidebar.text_area("AIへの最優先指示", "", height=400)
else:
  system_prompt = ""

# 保存ボタンが押されたらチャットログを初期化。systemプロンプトが設定されていたらチャットログに反映する
if st.sidebar.button("保存"):
  st.session_state.chat_log = []
  if system_prompt:
    st.session_state.chat_log.append({"role": SYSTEM_ROLE, "content": system_prompt})

# Streamlitが起動した直後なら複数のHTTPセッションで使えるチャットログを初期化
if "chat_log" not in st.session_state:
  st.session_state.chat_log = []

# OpenAIクライアント初期化
client = OpenAI(
  base_url="http://" + SERVER + ":11434/v1/",
  api_key="dummy"
)

# 生成AIの応答処理（関数定義）
def chat_completions():
  response = client.chat.completions.create(
    messages=st.session_state.chat_log,
    model=selected_model,
    stream=True,
  )
  return response

# タイトル
st.title("ChatYIC")

# チャット処理
user_msg = st.chat_input("ここにメッセージを入力")
if user_msg:
  # 過去のチャット履歴表示 (systemプロンプトは除外)
  for chat in st.session_state.chat_log:
    if chat["role"] == SYSTEM_ROLE:
      continue
    with st.chat_message(chat["role"]):
      st.text(chat["content"])

  # ユーザー入力表示
  with st.chat_message(USER_ROLE):
    st.text(user_msg)

  # チャットログにユーザ入力を追加
  st.session_state.chat_log.append({"role": USER_ROLE, "content": user_msg})

  # 生成AI応答











  # チャットログにAI応答を追加
  

  # インコンテキスト学習しているログの内容を表示
  print(st.session_state.chat_log)
