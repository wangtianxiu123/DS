import os
from openai import OpenAI
import httpx
import streamlit as st

# Streamlit 页面设置
st.title("Chat with OpenAI")

# 输入 API Key
api_key = st.text_input("请输入你的 API Key:", type="password")

# 输入用户消息
user_input = st.text_input("请输入内容:")

if st.button("发送"):
    if api_key and user_input:
        # 初始化 OpenAI 客户端
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.lkeap.cloud.tencent.com/v1",
            http_client=httpx.Client()
        )

        # 发送聊天请求
        stream = client.chat.completions.create(
            model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
            messages=[{'role': 'user', 'content': user_input}],
            stream=True,
            extra_body={"enable_search": True}
        )

        # 用于存储完整响应的文本
        full_text = ""
        original_response = ""  # 用于存储原始响应

        # 处理流式响应并逐字返回
        with st.empty():  # 创建一个空的占位符
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_text += chunk.choices[0].delta.content
                    st.text(full_text)  # 实时更新文本

        # 获取原始响应（假设 API 返回的原始内容在 stream 的最后一部分）
        original_response = stream.choices[0].message['content'] if stream.choices else "无原始响应"

        # 打印完整的文本和原始响应
        st.success("完整响应: " + full_text)
        st.info("原始响应: " + original_response)
    else:
        if not api_key:
            st.warning("请输入 API Key！")
        if not user_input:
            st.warning("请输入内容！")

