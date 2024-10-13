from ninja import Router
from openai import OpenAI
import json

from .schemas import TaskInput
import helpers
from decouple import config

router = Router()


@router.post("", auth=helpers.api_auth_not_required)
def tasks(request, payload: TaskInput):
    result = generate_tasks(payload.topic)

    return 200, result


def generate_tasks(temat, jezyk="polski"):
    client = OpenAI(api_key=config('OPENAI_API_KEY', cast=str))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a task generator. Always respond in JSON format in {jezyk}."},
            {"role": "user", "content": f"Rozłóż następujące zadanie na mniejsze 3 taski: {temat}"}
            # {"role": "system", "content": f"You are a topic generator. Always respond in JSON format in {jezyk}."},
            # {"role": "user", "content": f"Stwórz 3 tematy które mogą znaleźć się w kursie programoania o następującej tematyce: {temat}"}
        ]
    )

    result = response.choices[0].message.content

    try:
        json_data = json.loads(result)
        return json_data
    except json.JSONDecodeError:
        return {"error": "Model nie zwrócił poprawnego formatu JSON", "response": result}

