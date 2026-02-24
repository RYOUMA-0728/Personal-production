from openai import OpenAI
import base64
from pydantic import BaseModel, Field
import json
import time

# --- モデル定義 ---

class Pet(BaseModel):
  name: str =  Field(..., description='動物の名前')
  animal: str =  Field(..., description='動物の細かい種類')
  color: str =  Field(..., description='色合い')


class Human(BaseModel):
  name: str =  Field(..., description='人物の名前')
  sex: str =  Field(..., description='人物の性別')
  wear: str =  Field(..., description='来ている服装')
  color: str =  Field(..., description='服装の色')


class ObjectList(BaseModel):
  humans: list[Human]
  animals: list[Pet]


# --- ユーティリティ関数 ---

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def answer(pet: Pet) -> list[dict]:
  objects = ObjectList(
    humans = [],
    animals = [
      Pet(
        name = pet.name,
        animal = pet.animal,
        color = pet.color
      )
    ]
  )
  return [
    {
      "role": "assistant",
      "content": json.dumps(objects.model_dump())
    }
  ]


def question(message: str, image_path: str) -> list[dict]:
  return [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": message
        },
        {
          "type": "image_url",
          "image_url":  {
            "url": f"data:image/jpeg;base64,{encode_image(image_path)}"
          }
        }
      ]
    },
  ]


# --- メイン処理 ---

client = OpenAI(
  base_url='http://10.146.102.96:11434/v1/',
  api_key='dummy'
)


# アプリの役割を決める「システムプロンプト」
'''
SYSTEM_PROMPT = """
## やるべきこと
渡された画像に写っているもの（人間または動物）を説明してください。
## 制約条件
- 人間や動物の名前が分かれば出力をしてください。分からない場合は回答する必要はありません。
- 動物については種類も回答してください。
## 文字の長さ
日本語で200文字以内で答えてください。
"""

msgs = [
  {
    "role": "system",
    "content": SYSTEM_PROMPT
  }
]
'''

msgs = []

#  見本をインコンテキスト学習
'''
msgs += question('これは何ですか？', './img/IMG_0052.JPG')
msgs += answer(Pet(name='', animal='チワワ', color='白'))

msgs += question('これは何ですか？','./img/IMG_0129.JPG')
msgs += answer(Pet(name='', animal='ヨークシャーテリア', color='灰色'))

msgs += question('これは何ですか？','./img/IMG_0249.JPG')
msgs += answer(Pet(name='こうめちゃん', animal='トイプードル', color='灰色'))

msgs += question('これは何ですか？','./img/IMG_0338.JPG')
msgs += answer(Pet(name='ルイくん', animal='ミニチュアシュナウザー', color='灰色'))

msgs += question('これは何ですか？','./img/IMG_0427.JPG')
msgs += answer(Pet(name='リンちゃん', animal='チワワ', color='黒'))

msgs += question('これは何ですか？','./img/IMG_0008.JPG')
msgs += answer(Pet(name='こうめちゃん', animal='ヨークシャーテリア', color='茶'))

msgs += question('これは何ですか？','./img/IMG_0014.JPG')
msgs += answer(Pet(name='', animal='ポメラニアン', color='白'))
'''

# 本命の質問
msgs += question('これは何ですか？', './img/IMG_0585.JPG')


# 開始時刻を記録
start_time = time.perf_counter()


# 生成AIに問合せ
completion = client.beta.chat.completions.parse(
  temperature=0,
  model='gemma3:27b',
  messages=msgs,
#  response_format=ObjectList
)


# 終了時刻を記録
end_time = time.perf_counter()


# 経過時間を計算
elapsed_time = end_time - start_time
print(f"実行時間: {elapsed_time:.6f} 秒")
print('--------------------------------------------')


# テキスト出力
print(completion.choices[0].message.content)


# JSON出力
'''
json_data = json.loads(completion.choices[0].message.content)
print("人間")
for data in json_data["humans"]:
  print(data)
#  print(f"  {data['name']}, {data['sex']}, {data['wear']}, {data['color']}")
print("動物")
for data in json_data["animals"]:
  print(data)
#  print(f"  {data['name']}, {data['animal']}, {data['color']}")
'''
