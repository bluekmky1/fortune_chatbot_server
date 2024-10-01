from datetime import datetime
import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def gpt_fortune_and_tasks(user_data):
    prompt = f"""
    다음은 사용자의 개인 정보입니다:
    - 생년월일 및 성별: {user_data['userInfo']}
    - 출생지: 한국

    다음은 오늘 날짜입니다:
    - {datetime.now()}

    사용자의 개인정보를 바탕으로 사주를 분석하고, 분석한 사주정보를 바탕으로 최대한 정확하게 오늘의 운세를 본 뒤, 오늘의 운세를 바탕으로 운세가 올라갈 것 같은 할 일 3가지를 추천해줘.
    다음 json 형식으로 반환해줘.

    {{
    "todayFortune" : "오늘의 운세",
    "todoDesc" :[
        {{
        "todo" : "할일 1",
        "desc" : "할일 설명 1"
        }},
        {{
        "todo" : "할일 2",
        "desc" : "할일 설명 2"
        }},
        {{
        "todo" : "할일 3",
        "desc" : "할일 설명 3"
        }}
      ]
    }}
    """
    # GPT API 호출
    response = client.chat.completions.create(
        model="gpt-4o",  # gpt-4o 엔진 사용
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return json.loads(response.choices[0].message.content)
