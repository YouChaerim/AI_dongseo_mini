import os  # 운영체제 환경변수 등을 다루기 위한 라이브러리
from openai import OpenAI  # OpenAI GPT API 사용
import json  # JSON 데이터 다루기 위한 표준 라이브러리
import requests  # HTTP 요청용 라이브러리
from dotenv import load_dotenv  # .env 파일에서 API 키 불러오기

# 환경변수(.env) 파일 불러오기
load_dotenv()

# API 키 읽어오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# OpenAI API 클라이언트 생성
client = OpenAI(api_key=OPENAI_API_KEY)

# 챗봇 첫 메시지
START_MSG = "안녕하세요! 여행 일정 추천 및 요약 챗봇입니다.\n\n먼저 여행지부터 알려주세요!"

# 📄 GPT에 전달할 프롬프트(지침) 파일 읽기
with open("assets/schedule_prompt.txt", "r", encoding="utf-8") as f:
    content = f.read()
    # 일정 추천용 프롬프트 부분 추출
    schedule_prompt = content.split("### SCHEDULE_PROMPT_START")[1].split("### SCHEDULE_PROMPT_END")[0].strip()
    # 일정 요약용 프롬프트 부분 추출
    summary_prompt = content.split("### SUMMARY_PROMPT_START")[1].split("### SUMMARY_PROMPT_END")[0].strip()

# Google Translate API를 사용하여 언어 감지
def detect_language(text):
    url = "https://translation.googleapis.com/language/translate/v2/detect"
    params = {'q': text, 'key': GOOGLE_API_KEY}
    response = requests.post(url, data=params).json()
    return response['data']['detections'][0][0]['language']

# Google Translate API를 사용하여 번역
def translate(text, source, target):
    if source == target:
        return text
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {'q': text, 'source': source, 'target': target, 'format': 'text', 'key': GOOGLE_API_KEY}
    response = requests.post(url, data=params).json()
    return response['data']['translations'][0]['translatedText']

# OpenAI GPT API 호출 함수
def ask_gpt(system_prompt, messages):
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_prompt}] + messages
    )
    return res.choices[0].message.content.strip()

# GPT가 반환한 JSON 일정 데이터를 HTML 표로 변환
def json_to_html_table(data):
    html = ""
    for day in data:
        html += f"<h4>{day['date']} - {day['region']} (MBTI: {day['mbti']})</h4>"
        html += "<table border='1' style='border-collapse: collapse;'>"
        html += "<tr><th>시간</th><th>활동</th></tr>"
        for item in day["schedule"]:
            html += f"<tr><td>{item['time']}</td><td>{item['activity']}</td></tr>"
        html += "</table><br/>"
    return html

# ✨ 메인 챗봇 함수: 일정 추천 또는 요약 처리
def schedule_chatbot_fn(txt_val, chat_val, state_val):
    lang = detect_language(txt_val)  # 입력 언어 감지
    input_for_gpt = txt_val

    # 영어/일본어 입력이면 → 한국어로 번역 후 GPT 호출
    if lang in ["en", "ja"]:
        input_for_gpt = translate(txt_val, lang, "ko")

    # 기존 대화 기록 + 현재 입력 추가
    messages = chat_val.copy() if chat_val else []
    messages.append({"role": "user", "content": input_for_gpt})

    # "요약해줘" 요청이면 → 요약 모드
    if "요약해줘" in input_for_gpt:
        summary_prompt_md = summary_prompt + "\n\n⭐ 출력은 Markdown 스타일로 작성하세요."
        gpt_response = ask_gpt(summary_prompt_md, messages)

        # 영어/일본어 사용자면 → 결과 다시 번역
        if lang in ["en", "ja"]:
            gpt_response = translate(gpt_response, "ko", lang)

        chat_val.append({"role": "user", "content": txt_val})
        chat_val.append({"role": "assistant", "content": gpt_response})

        return "", chat_val, state_val

    else:
        # 일정 추천 모드
        gpt_response = ask_gpt(schedule_prompt, messages)

        # 영어/일본어 사용자면 → 결과 다시 번역
        if lang in ["en", "ja"]:
            gpt_response = translate(gpt_response, "ko", lang)

        try:
            # GPT 응답에서 JSON 형식 부분 추출
            json_start = gpt_response.find("[")
            json_str = gpt_response[json_start:]
            schedule_data = json.loads(json_str)  # JSON 파싱
            html_table = json_to_html_table(schedule_data)  # HTML 표로 변환
            gpt_response = html_table
        except Exception as e:
            pass  # 파싱 실패 시 GPT 응답 그대로 사용

        chat_val.append({"role": "user", "content": txt_val})
        chat_val.append({"role": "assistant", "content": gpt_response})

        return "", chat_val, state_val
