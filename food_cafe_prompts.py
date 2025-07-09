import random
from food_cafe_recommend import recommend_food_cafe

# 안내 메시지(입력 예시)
STEP1_GUIDE = "입력 예시: 서울, 부산, 제주도"
STEP2_GUIDE = "입력 예시: 한식, 중식, 일식, 양식, 기타, 카페, 랜덤, 끝"

# 1단계: 여행지 질문
STEP1_QUESTIONS = [
    "여행지가 어딘지 알려주세요.!",
    "목적지가 어딘지 알려주세요.!",
    "어디로 가시는지 알려주세요.!",
    "즐거운 휴가 어디로 가는지 알려주세요.!"
]

# 2단계: 음식 종류 선택
STEP2_QUESTIONS = [
    "양식,일식,중식,한식,기타(이탈리아, 브라질, 인도 등),카페 무엇이든 원하시는 종류를 말해주세요.! 고르시기 힘드시면 사랑스러운 딸깍이가 랜덤으로 뽑아드릴께요.! :)",
    "오늘은 무엇을 드시고 싶으신가요?? 말씀해주시면 가게 정보를 알려드릴게요.! 고르시기 힘드시면 사랑스러운 딸깍이가 랜덤으로 뽑아드릴께요.! :)"
]
STEP2_RANDOM_FALLBACK = [
    "배가 많이 고프시죠!! 빠르게 사랑하는 고객님이 있으신 지역에서 맛집을 뽑아서 알려드릴게요.! 고르시기 힘드시면 사랑스러운 딸깍이가 랜덤으로 뽑아드릴께요.! :)"
]
STEP3_ANSWERS = [
    "{food_type}로 선택하셨군요.!! 종아요!!! 딸깍이가 현지인들이 이 가는 가게로 선정해봤어요.!",
    "{food_type}으로 고르셨군요.! 사랑스러운 고객님이 선택하신 종류에 맞춰 그 지역 사람들이 가는 맛집 리스트를 선정해봤어요.!"
]
STEP3_RANDOM_ANSWER = [
    "사랑스러운 딸깍이가 랜덤으로 선정해봤어요.!! 마음에 드셨나요? 마음에 안드시면 다시 랜덤이라고 말씀해주시면 딸깍이가 다시 선정해드릴게요.! :)"
]
STEP4_END = [
    "이 딸깍이를 사용해주셔서 너무 기뻐요~ 제가 선정한 리스트 중에 하나라도 마음에 드셔서 다행이에요~ 좋은 국내 여행 되시길 바랄게요.!! 다음에 또 이용 해주세요!!! 딸깍이가 항상 기다릴게요.! :) (수정할 사항이 있으면 나중에 딸깍이를 통해 알려주세요. 딸깍이가 잘못된 정보가 있는지 확인 후 실시간으로 수정해드릴게요.!)",
    "선정을 다 하셨군요.! 다음에도 딸깍이를 이용해주세요 언제든지 어디서도 딸깍만 해주시면 일정,관광명소,카페,맛집,숙소 정보를 제공해 드릴게요.!! 좋은 여행 되세요.! :) (수정할 사항이 있으면 나중에 딸깍이를 통해 알려주세요. 딸깍이가 잘못된 정보가 있는지 확인 후 실시간으로 수정해드릴게요.!)",
    "다 끝나셨네요~!! 수정할 사항이 있으면 나중에 딸깍이를 통해 알려주세요. 딸깍이가 잘못된 정보가 있는지 확인 후 실시간으로 수정해드릴게요.! 사용해주셔서 정말 감사합니다.! 다음에 또 이용해 주세요.! 좋은 여행 되시길 바랄게요.!"
]

def food_cafe_chatbot(user_msg, chat_history, state):
    if chat_history is None:
        chat_history = []
    if user_msg.strip():
        chat_history.append({"role": "user", "content": user_msg})

    # "끝" 또는 "그만" 입력 시 바로 마무리 멘트
    if user_msg.strip() in ["끝", "그만"]:
        bot_msg = random.choice(STEP4_END)
        chat_history.append({"role": "assistant", "content": bot_msg})
        state = {"step": 1, "region": None, "food_type": None}
        return "", chat_history, state

    if state is None or not state:
        state = {"step": 1, "region": None, "food_type": None}
        bot_msg = random.choice(STEP1_QUESTIONS) + f"\n\n<small style='color:#888;'>{STEP1_GUIDE}</small>"
        chat_history.append({"role": "assistant", "content": bot_msg})
        return "", chat_history, state

    # STEP 1: 지역 선택
    if state["step"] == 1:
        region = user_msg.strip()
        if region not in ["서울", "부산", "제주도"]:
            bot_msg = f"정확한 지역명(서울/부산/제주도) 중에서 입력해주세요!\n\n<small style='color:#888;'>{STEP1_GUIDE}</small>"
            chat_history.append({"role": "assistant", "content": bot_msg})
            return "", chat_history, state
        state["region"] = region
        state["step"] = 2
        bot_msg = random.choice(STEP2_QUESTIONS) + f"\n\n<small style='color:#888;'>{STEP2_GUIDE}</small>"
        chat_history.append({"role": "assistant", "content": bot_msg})
        return "", chat_history, state

    # STEP 2, 3: 음식 종류 선택 → 추천 반복!
    if state["step"] in [2, 3]:
        food_type = user_msg.strip()
        state["food_type"] = food_type
        state["step"] = 3  # 반복 입력
        if food_type == "랜덤":
            bot_msg = random.choice(STEP2_RANDOM_FALLBACK)
            chat_history.append({"role": "assistant", "content": bot_msg})
        else:
            bot_msg = random.choice(STEP3_ANSWERS).format(food_type=food_type)
            region = state["region"]
            recs = recommend_food_cafe(region, food_type)
            chat_history.append({"role": "assistant", "content": bot_msg})
            for card_html in recs:
                chat_history.append({"role": "assistant", "content": card_html})
        # 다음 입력 계속 음식 선택(종료 전까지)
        return "", chat_history, state


    # 예외: 이상한 state일 경우 (초기화)
    bot_msg = random.choice(STEP1_QUESTIONS) + f"\n\n<small style='color:#888;'>{STEP1_GUIDE}</small>"
    chat_history.append({"role": "assistant", "content": bot_msg})
    state = {"step": 1, "region": None, "food_type": None}
    return "", chat_history, state
