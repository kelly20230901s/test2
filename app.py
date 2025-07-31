import streamlit as st
import openai
from prompts import journalist_prompt

# OpenAI API 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="교육 전문 기자 챗봇", layout="wide")
st.title("📰 교육 전문 기자 챗봇 by J")
st.write("행사명과 개요를 입력하면 보도자료 형식의 기사를 생성해 드립니다.")

# 사용자 입력
event_name = st.text_input("📌 행사명")
event_description = st.text_area("📝 행사 개요 또는 주요 내용", height=200)
generate_btn = st.button("📰 기사 생성")

if generate_btn and event_name and event_description:
    with st.spinner("기사를 작성 중입니다..."):

        # 프롬프트 조립
        user_prompt = f"""
다음 내용을 바탕으로 보도자료 형식의 교육 기사로 작성해 주세요.

행사명: {event_name}
행사 개요: {event_description}

기사에는 제목, 부제목, 리드문단, 인터뷰(교사 또는 관계자), 마무리 문장을 포함해 주세요.
거짓말은 하지 말고, 내용이 사실처럼 느껴지도록 써주세요.

전문적인 교육 기자의 문체를 사용해주세요.

---

{journalist_prompt}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 10년차 교육 전문 기자입니다."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        st.subheader("📄 생성된 기사")
        st.markdown(response.choices[0].message.content)

elif generate_btn:
    st.warning("행사명과 내용을 모두 입력해 주세요.")
