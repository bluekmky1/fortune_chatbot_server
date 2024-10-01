from fastapi import FastAPI, Request
from logger import configure_logger
from responses import ResponseTemplates
from supabase_utils import check_and_update_fortune, update_user_data, get_user_data, create_user
from dotenv import load_dotenv
from typing import Dict, Any

# 서버 실행: uvicorn main:app --reload --host="0.0.0.0" --port 80

app = FastAPI()
logger = configure_logger()
response_templates = ResponseTemplates()

load_dotenv(verbose=True)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"요청 수신: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"응답 완료: {response.status_code}")
    return response


@app.post("/test")
def get_fortune():
    return response_templates.simple_image(
        image_url="https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
        alt_text="hello I'm Ryan"
    )


@app.post("/save/userInfo")
def save_user_field(input_data: Dict[str, Any]):
    user_id = input_data['userRequest']['user']['id']
    print(user_id)

    # 사용자 데이터 조회
    user_data = get_user_data(user_id)

    # 새로운 사용자 발견 시 생성
    if not user_data:
        create_user(user_id)
    update_user_data(user_id, "userInfo",
                     input_data['userRequest']['utterance'])

    return response_templates.simple_text(f"사용자 정보를 저장했습니다.")


@app.post("/fortune")
def get_fortune(input_data: Dict[str, Any]):
    user_id = input_data['userRequest']['user']['id']
    fortune_and_tasks = check_and_update_fortune(user_id)
    print(fortune_and_tasks)
    if fortune_and_tasks:
        return response_templates.fortune_and_tasks(fortune_and_tasks)
    # else:
    #     return response_templates.error()
