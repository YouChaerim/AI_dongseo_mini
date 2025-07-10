import gradio as gr
import json
import random

REGIONS = ["서울", "부산", "제주"]
MBTIS = ["J", "P"]

# 일정 데이터 로드 함수
def load_schedule(mbti, region):
    filename = f"assets/schedule_{mbti.lower()}.json"
    with open(filename, encoding="utf-8") as f:
        schedules = json.load(f)
    return schedules[region]

# 딸깍투 시나리오 메시지
START_MSG = "안녕하세요! 저는 MBTI P형과 J형 계획을 짜주는 일을 하는 딸깍이 동생 딸깍투에요~!"
REGION_MSG = "부산, 제주, 서울 중 하나를 골라서 말해주세요! :)"
MBTI_MSG = "다음은 J형인지 P형인지 알려주세요~!"

J_MSG = """J형이시군요.!! 아주 계획적이시네요~ 저도 계획적인 사람 좋아해요.!
지금부터 딸깍투가 일정을 바로 만들어 드릴게요! :)
(예상치 못한 날씨와 식사 장소 예매 오류를 예상하여 안정적인 여행을 위해 휴식 시간과 예비 플랜도 포함할게요!)"""
P_MSG = """P형이시군요.!! 역시 여행은 즉흥적이게 가야 재밌죠~ 
성향에 맞게 가게, 카페, 장소는 마음에 드시는 걸로 선택해서 갈 수 있게 3가지~5가지로 만들어 드릴게요! :)"""

END_MSG = """완성된 일정표는 마음에 드셨나요?? 딸깍투가 엄청 노력해서 만들었어요!
한 번 봐보시고 마음에 안드시면 '다시 만들어줘'라고 말해주세요. 그러면 다시 만들어 드릴게요! :)
제가 만들어드린 일정은 마음에 드셨는지 모르겠지만, 즐거운 여행되시고 행복한 하루 되시길 바랄게요! :)"""

def pretty_j_schedule(schedule):
    # J형: 일자별 표 출력
    html = ""
    for day in [d for d in schedule if "일차" in d]:
        html += f"<h4>🗓️ {day}</h4><table border=1 style='width:100%;border-radius:8px;overflow:hidden;font-size:15px;margin-bottom:16px;'><tr><th>시간</th><th>장소</th><th>활동</th><th>체크리스트</th></tr>"
        for s in schedule[day]:
            html += f"<tr><td>{s['시간']}</td><td>{s['장소']}</td><td>{s['활동']}</td><td>{s['체크리스트']}</td></tr>"
        html += "</table>"
    # 예비계획
    html += "<h4>📌 예비 플랜</h4><table border=1 style='width:100%;border-radius:8px;overflow:hidden;font-size:15px;'><tr><th>상황</th><th>대체</th><th>설명</th><th>체크리스트</th></tr>"
    for e in schedule["예비계획"]:
        html += f"<tr><td>{e['상황']}</td><td>{e['대체']}</td><td>{e['설명']}</td><td>{e['체크리스트']}</td></tr>"
    html += "</table>"
    return html

def pretty_p_schedule(schedule):
    # P형: 시간대별 옵션/장소/식사 표
    html = ""
    for part in ["아침", "점심", "오후카페", "저녁", "마무리카페"]:
        data = schedule[part]
        html += f"<h4>🕗 {part}</h4><ul>"
        for item in data["일정"]:
            html += f"<li>{item['option']} → <b>{item['place']}</b></li>"
        html += "</ul><b>추천 식사/카페</b><ul>"
        k = "식사" if "식사" in data else "카페"
        for food in data[k]:
            html += f"<li>{food['place']} ({food['phone']})</li>"
        html += "</ul>"
    return html

# 챗봇 동작 로직 (상태 기반)
def schedule_chatbot_fn(msg, history, state):
    history = history or []
    state = state or {"step": 0}

    # 첫 시작
    # if state["step"] == 0:
    #     history.append({"role": "assistant", "content": START_MSG})
    #     history.append({"role": "assistant", "content": REGION_MSG})
    #     state["step"] = 1
    #     return "", history, state

    # 지역 입력받기
    if state["step"] == 1:
        region = None
        msg_clean = msg.replace(" ", "")
        for r in REGIONS:
            if r in msg_clean:
                region = r
        if not region:
            history.append({"role": "assistant", "content": "다시 한 번 부산, 제주, 서울 중 하나를 입력해주세요!"})
            return "", history, state
        state["region"] = region
        history.append({"role": "user", "content": msg})
        history.append({"role": "assistant", "content": MBTI_MSG})
        state["step"] = 2
        return "", history, state

    # MBTI 입력받기
    if state["step"] == 2:
        mbti = None
        msg_upper = msg.upper()
        if "J" in msg_upper:
            mbti = "J"
            history.append({"role": "user", "content": msg})
            history.append({"role": "assistant", "content": J_MSG})
        elif "P" in msg_upper:
            mbti = "P"
            history.append({"role": "user", "content": msg})
            history.append({"role": "assistant", "content": P_MSG})
        else:
            history.append({"role": "assistant", "content": "J 또는 P 중에 선택해서 입력해주세요!"})
            return "", history, state
        state["mbti"] = mbti
        # (여기서 바로 일정 제공!!)
        region, mbti = state["region"], state["mbti"]
        sched = load_schedule(mbti, region)
        if mbti == "J":
            html = pretty_j_schedule(sched)
        else:
            html = pretty_p_schedule(sched)
        history.append({"role": "assistant", "content": html})
        history.append({"role": "assistant", "content": END_MSG})
        state["step"] = 4  # 바로 "다시 만들어줘" 대기 단계로 이동
        return "", history, state

    # 일정 제공
    if state["step"] == 3:
        region, mbti = state["region"], state["mbti"]
        sched = load_schedule(mbti, region)
        if mbti == "J":
            html = pretty_j_schedule(sched)
        else:
            html = pretty_p_schedule(sched)
        history.append({"role": "assistant", "content": html})
        history.append({"role": "assistant", "content": END_MSG})
        state["step"] = 4
        return "", history, state

    # 다시 만들기 요청
    if state["step"] == 4:
        if "다시" in msg:
            state["step"] = 3
            history.append({"role": "user", "content": msg})
            return schedule_chatbot_fn("", history, state)
        history.append({"role": "assistant", "content": "추가로 궁금하신 점이 있다면 말씀해주세요! :)"})
        return "", history, state

    return "", history, state

# Gradio Blocks (이전 코드에 이 부분만 붙이면 됩니다)
def run_schedule_chatbot():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("## 📅 딸깍투 맞춤 여행 일정 챗봇")
        chatbot = gr.Chatbot(show_label=False)
        state = gr.State(value={"step": 0})
        with gr.Row():
            txt = gr.Textbox(placeholder="입력하세요...", show_label=False, scale=4)
            btn = gr.Button("전송", scale=1)
        btn.click(schedule_chatbot_fn, [txt, chatbot, state], [txt, chatbot, state])
        txt.submit(schedule_chatbot_fn, [txt, chatbot, state], [txt, chatbot, state])

    return demo

# 기존 페이지에 아래처럼 추가:
# (예시: 일정 버튼 클릭 시 run_schedule_chatbot().launch() 실행)
if __name__ == "__main__":
    run_schedule_chatbot().launch()
