from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)


st.title("21-6 提出課題用Webアプリ")

st.write("##### 動作モード1: 旅行プラン探し")
st.write("入力フォームに気になる都市を入力し、「実行」ボタンを押すことで旅行プランを提案できます。")
st.write("##### 動作モード2: 飲食店探し")
st.write("都市とジャンルを入力することで、おすすめの飲食店を提案できます。")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["旅行プラン探し", "飲食店探し"]
)

st.divider()

if selected_item == "旅行プラン探し":
    input_message = st.text_input(label="旅行プランを検索する都市を入力してください。")

else:
    city = st.text_input(label="飲食店を検索する都市を入力してください。")
    genre = st.text_input(label="ジャンルを入力してください。（例：イタリアン、中華、等）")

if st.button("実行"):
    st.divider()

    if selected_item == "旅行プラン探し":
        if input_message:
            st.write(f"都市名: **{input_message}**")

            messages = [
                SystemMessage(content="You are a helpful travel planner assistant."),
                HumanMessage(content=f"{input_message}の旅行プランを提案してください。"),
            ]

            with st.spinner("旅行プランを検索中..."):
                result = llm.invoke(messages)
                st.write(f"旅行プラン候補: {result.content}")

        else:
            st.error("都市名を入力してから「実行」ボタンを押してください。")

    else:
        if city and genre:
            try:
                messages = [
                    SystemMessage(content="You are a helpful restaurant finder assistant."),
                    HumanMessage(content=f"{city}の{genre}を提供する飲食店を提案してください。"),
                ]

                with st.spinner("飲食店を検索中..."):
                    result = llm.invoke(messages)
                    st.write(f"飲食店候補: {result.content}")

            except ValueError as e:
                st.error("都市名とジャンルは文字列で入力してください。")

        else:
            st.error("都市名とジャンルをどちらも入力してください。")