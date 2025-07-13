import os  # 운영체제 환경변수 등을 다루기 위한 라이브러리
from openai import OpenAI  # OpenAI GPT API를 사용하기 위한 라이브러리
import requests  # HTTP 요청용 라이브러리
from dotenv import load_dotenv  # .env 파일에서 API 키 불러오는 라이브러리

# .env 파일 내용을 읽어 환경변수로 설정
load_dotenv()

# 환경변수에서 API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# OpenAI API 클라이언트 생성 (API 키로 인증)
client = OpenAI(api_key=OPENAI_API_KEY)

START_MSG_FOOD = "안녕하세요! 맛집/카페 추천 챗봇입니다.\n\n방문하실 지역과 음식 종류(한식, 중식, 일식, 양식)를 알려주세요!"

# 📄 GPT에 전달할 "맛집/카페 추천 프롬프트" 텍스트 파일 읽어오기
with open("assets/food_cafe_prompt.txt", "r", encoding="utf-8") as f:
    food_cafe_prompt = f.read()

# 입력 텍스트의 언어가 무엇인지 감지하는 함수 (Google Translate API 사용)
def detect_language(text):
    url = "https://translation.googleapis.com/language/translate/v2/detect"
    params = {'q': text, 'key': GOOGLE_API_KEY}
    response = requests.post(url, data=params).json()
    return response['data']['detections'][0][0]['language']

# 텍스트를 source 언어에서 target 언어로 번역하는 함수 (Google Translate API 사용)
def translate(text, source, target):
    if source == target:
        return text  # 같은 언어면 번역 안함
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {'q': text, 'source': source, 'target': target, 'format': 'text', 'key': GOOGLE_API_KEY}
    response = requests.post(url, data=params).json()
    return response['data']['translations'][0]['translatedText']

# GPT에게 질문을 보내고 답변을 받아오는 함수
def ask_gpt(system_prompt, messages):
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_prompt}] + messages
    )
    return res.choices[0].message.content.strip()  # GPT 답변 내용만 반환

# "맛집/카페 챗봇"의 핵심 함수: 대화 상태 관리 + 다국어 처리 + GPT 호출
def food_cafe_chatbot(txt_val, chat_val, state_val):
    lang = detect_language(txt_val)  # 입력 언어 감지 (예: ko, en, ja)
    input_text = txt_val

    # 입력이 영어 또는 일본어이면 → 한국어로 번역하여 GPT에게 전달
    if lang in ["en", "ja"]:
        input_text = translate(txt_val, lang, "ko")

    # 기존 대화 히스토리에 현재 입력 추가
    messages = chat_val.copy() if chat_val else []
    messages.append({"role": "user", "content": input_text})

    # GPT API 호출 (맛집/카페 추천 응답 받기)
    gpt_response = ask_gpt(food_cafe_prompt, messages)

    # GPT 응답이 다국어 사용자면 → 다시 원래 언어로 번역
    if lang in ["en", "ja"]:
        gpt_response = translate(gpt_response, "ko", lang)

    # 대화 기록에 현재 입력/응답 추가
    chat_val.append({"role": "user", "content": txt_val})
    chat_val.append({"role": "assistant", "content": gpt_response})

    # 결과 반환: 입력칸 비우기, 대화 기록, 상태 그대로
    return "", chat_val, state_val
