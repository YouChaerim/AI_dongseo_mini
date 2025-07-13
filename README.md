# 🛫 Travel Recommend Bot

맛집, 숙소, 항공권 정보를 통합 추천해주고 일정표를 자동으로 만들어주는  
파이썬 기반 웹 챗봇/대시보드 프로젝트  
(Gradio/Streamlit + 카카오로컬API + Skyscanner API + Fly.io 배포)

---

## 📂 프로젝트 파일 구조 및 설명

.
├── README.md # 프로젝트 설명서 (이 파일)
├── api_kakao.py # 카카오 API를 사용하여 장소(맛집, 숙소 등)를 검색하는 파일
├── food_cafe_chatbot.py # 맛집/카페 추천 챗봇 기능을 담당하는 파일
├── logic.py # 여러 파일에서 공통으로 사용하는 데이터(예: 지역, 카테고리)와 함수가 있는 파일
├── main_gradio.py # Gradio UI로 전체 서비스를 실행하는 메인 파일
├── schedule_chatbot.py # 일정 추천 챗봇 기능을 담당하는 파일
├── styles
│ └── custom.css # 사용자 인터페이스의 디자인(스타일)을 설정하는 CSS 파일
├── assets
│ └── food_cafe_prompt.txt # 맛집 및 카페 챗봇 사용시 GPT API에 제공해 줄 프롬포트
│ └── schedule_prompt.txt # 일정 챗봇 사용시 GPT API에 제공해 줄 프롬포트

---

## 개발 환경 세팅

### 🔸 Anaconda(Conda) 설치

#### [공식 다운로드 아카이브](https://repo.anaconda.com/archive/)

- **Windows:**  
  `Anaconda3-2024.10-1-Windows-x86_64.exe`
- **Mac:**  
  - **Intel:** `Anaconda3-2024.10-1-MacOSX-x86_64.pkg`
  - **Apple Silicon(M1/M2/M3):** `Anaconda3-2024.10-1-MacOSX-arm64.pkg`

---

### 🔸 Conda 가상환경 생성

```
bash
conda create -n mini python=3.10
conda activate mini
```
---
## 설치 명령어

```
pip install gradio requests python-dotenv
pip install openai googletrans==4.0.0-rc1
```

---
## 실행 명령어

### gradio 실행
- python main_gradio.py