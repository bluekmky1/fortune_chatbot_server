from datetime import datetime, timedelta
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
from gpt_utils import gpt_fortune_and_tasks
from dateutil.parser import parse

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_user(user_id):
    # 새로운 사용자를 추가
    supabase.table('user').insert({
        "id": user_id,
        "userInfo": None,
        "fortuneId": None,
    }).execute()


def update_user_data(user_id, field, value):
    supabase.table('user').update({field: value}).eq("id", user_id).execute()


def get_user_data(user_id):
    response = supabase.table("user").select("*").eq("id", user_id).execute()
    return response.data[0] if response.data else None


def delete_old_fortune_and_tasks(fortune_id):
    # 할 일 삭제
    supabase.table('todo').delete().eq('fortuneId', fortune_id).execute()
    # 운세 삭제
    supabase.table('fortune').delete().eq('id', fortune_id).execute()


def update_fortune_and_tasks(user_id, fortune_and_tasks):
    user_data = get_user_data(user_id)
    fortune_id = user_data.get('fortuneId')

    # 기존 운세와 할 일 삭제
    if fortune_id:
        delete_old_fortune_and_tasks(fortune_id)

    # 새로운 운세 추가
    fortune_response = supabase.table('fortune').insert({
        "fortune": fortune_and_tasks['todayFortune'],
    }).execute()

    new_fortune_id = fortune_response.data[0]['id']
    supabase.table('user').update(
        {"fortuneId": new_fortune_id}).eq("id", user_id).execute()

    # 새로운 할 일 추가
    todo_data = [
        {
            'fortuneId': new_fortune_id,
            'todo': task['todo'],
            'description': task['desc'],
        } for task in fortune_and_tasks['todoDesc']
    ]
    supabase.table('todo').insert(todo_data).execute()


def check_and_update_fortune(user_id):
    user_data = get_user_data(user_id)
    if not user_data:
        return None

    fortune_id = user_data.get('fortuneId')
    if not fortune_id:
        # 운세가 없으면 새로 생성
        new_fortune_and_tasks = gpt_fortune_and_tasks(user_data)
        update_fortune_and_tasks(user_id, new_fortune_and_tasks)
        return new_fortune_and_tasks

    # 운세 날짜를 확인하여 어제의 것인지 검사
    fortune_data = supabase.table("fortune").select(
        "*").eq("id", fortune_id).execute().data[0]

    fortune_date = parse(fortune_data['createdAt'])
    today = datetime.now()

    if fortune_date.date() == (today - timedelta(days=1)).date():
        # 운세가 어제의 것이라면 새로 생성
        new_fortune_and_tasks = gpt_fortune_and_tasks(user_data)
        update_fortune_and_tasks(user_id, new_fortune_and_tasks)
        return new_fortune_and_tasks

    # 어제의 것이 아니면 기존 운세 반환
    return {
        "todayFortune": fortune_data['fortune'],
        "todoDesc": [
            {"todo": t['todo'], "desc": t['description']}
            for t in supabase.table("todo").select("*").eq("fortuneId", fortune_id).execute().data
        ]
    }
