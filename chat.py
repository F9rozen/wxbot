from llm import GPT
from wxauto import WeChat
import os
import time
from dotenv import load_dotenv
from dashscope import Application
from http import HTTPStatus

# 读取相关环境变量
load_dotenv()

def start_wechat_service(api_key, app_id, prompt, listen_list, wait=5):
    """启动微信智能客服服务，使用 Dashscope API 进行回复。"""
    wx = WeChat()
    processed_messages = set()  # 存储已处理消息的唯一标识

    # 初始化 processed_messages，忽略历史消息
    for i in listen_list:
        wx.AddListenChat(who=i)  # 添加监听对象
    initial_msgs = wx.GetListenMessage()
    for chat in initial_msgs:
        msg = initial_msgs.get(chat)
        for i in msg:
            processed_messages.add(i.id)  # 将历史消息标记为已处理

    while True:
        #if wx.CheckNewMessage():
        msgs = wx.GetListenMessage()
        for chat in msgs:
            msg = msgs.get(chat)   # 获取消息内容
            for i in msg:
                if i.id not in processed_messages:  # 检查消息是否已处理
                    processed_messages.add(i.id)  # 标记消息为已处理
                    if i.type == 'friend':
                        try:
                            response = Application.call(
                                api_key=api_key,
                                app_id=app_id,
                                prompt=i.content
                            )

                            if response.status_code == HTTPStatus.OK:
                                reply = response.output.text
                            else:
                                reply = f"错误: {response.message}"
                        except Exception as e:
                            reply = f"调用失败: {str(e)}"

                        chat.SendMsg(reply)  # 回复
        time.sleep(wait)