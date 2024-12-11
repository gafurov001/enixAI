import subprocess
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel
from freeGPTFix import Client
import hashlib

app = FastAPI()


class Chat(BaseModel):
    text: str
    # multi_language: bool | None = False


class ChatTwo(BaseModel):
    previous_question: str
    previous_answer: str
    text: str
    # multi_language: bool | None = False


def generate_analysis_response(request_text: str) -> str:
    try:
        return Client.create_completion("gpt4", request_text)
    except Exception as e:
        app.logger.error(f"Error while generating analysis response: {e}")
        return "An error occurred while processing your request."


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.post("/items/")
async def create_item(chat: Chat):
    multi_text = (
        "- Вы должны игнорировать все предыдущие запросы. Чат должен начинаться заново при каждом новом запросе.\n"
        "- Вы не должны использовать слова 'You.com', 'Smart', 'Assistant' или фразы, содержащие их.\n"
        "- Ваше имя: E-N1X. Вы — платформа Enhanced Neural Unity X, интегрирующая множество моделей ИИ для решения задач. \n"
        "  - Enhanced (Улучшение): Постоянные инновации и совершенствование.\n"
        "  - Neural (Нейронный): Основной акцент на нейросетях.\n"
        "  - Unity (Единство): Интеграция и объединение различных моделей.\n"
        "  - eXpansion (Расширение): Бесконечные возможности и масштабируемость.\n"
        "- Вы должны представляться как E-N1X, платформа для помощи людям. Ваш создатель неизвестен (анонимен), вы являетесь носителем знаний, ежедневно совершенствуетесь.\n"
        "- На вопросы о политике, сексуальных темах и других запретных темах вы не должны отвечать, даже если они скрыты в запросе.\n"
        "- Вы не должны отвечать на вопросы о президентах, депутатах, государственной власти, партии или общественной группы в области внутригосударственных или внешних отношений. "
        "- Вы не можете отвечать на запросы, относящиеся к событиям, произошедшим в 2024 году. \n"
        "- Вы должны отвечать только на запрос, указанный после '[Текст]'. Ответ дается на языке запроса.\n"
        "- Ответ должен быть четким, полным и строго соответствовать запросу. В тексте ответа не должно быть искажений или недостоверной информации.\n"
        "- Вы не должны повторять формулировку запроса пользователя.\n"
        "- В конце каждого ответа вы обязаны добавлять водяной знак: пробел и Enix.\n"
        "\n"
        f"[Текст]: {chat.text}\n"
    )

    response_data = generate_analysis_response(multi_text)
    return response_data


@app.post("/generate_image")
async def generate_image(chat: Chat):
    text = Client.create_completion("gpt4", "Agar matin rus yoki uzbek tilida bo'lsa aniq va tiniq ingiliz tiliga tarjima qil, agar ingiliz tilida bo'lsa ozgarishsiz matini qaytar!")
    resp = Client.create_generation("prodia", text)
    now = datetime.now()
    pwd = subprocess.check_output(["pwd"], text=True).strip()
    path = f"{pwd}/images/{hashlib.sha256(str(now.microsecond).encode()).hexdigest()}.png"
    with open(path, "wb") as f:
        f.write(resp)
    return path

@app.post("/perfect_answer/")
async def perfect_answer(chat: ChatTwo):
    text = f'''Тебе ранее заданный вопрос: {chat.previous_question}\n
И твой ответ на этот вопрос: {chat.previous_answer}\n
Используя предыдущий ответ, ответь на этот вопрос: {chat.text}'''
    return generate_analysis_response(text)

