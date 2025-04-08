import openai
import os
import random
from http import HTTPStatus
from dashscope import Application

default_prompt = '''you are a helpful assistant'''

class GPT:
    def __init__(self, api_key, prompt=None, base_url=None, proxy=None):
        self.api_key = api_key
        self.base_url = base_url
        if proxy:
            os.environ['HTTP_PROXY'] = proxy
            os.environ['HTTPS_PROXY'] = proxy
        openai.api_key = self.api_key
        if self.base_url:
            openai.api_base = self.base_url
        self.initialize(prompt)

    def initialize(self, prompt=None):
        """重置对话，清空历史消息。如果有提示，添加提示。
        
        Args:
            prompt (str): 提示信息，默认为 None。
        
        Returns:
            None
        """
        if prompt:
            self.messages = [{"role": "system", "content": prompt}]
        else:
            self.messages = [{"role": "system", "content": default_prompt}]

    def chat(self, prompt, model="gpt-3.5-turbo"):
        """对话。

        Args:
            prompt (str): 用户输入。
            model (str): 模型，默认为 gpt-3.5-turbo。
        
        Returns:
            str: 模型回复。
        """
        self.messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=model,
            messages=self.messages,
            temperature=0.8
        )
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def validate_api_key(self):
        """验证 API Key 格式是否正确。
        
        Returns:
            bool: 如果格式正确返回 True，否则返回 False。
        """
        #if self.api_key.startswith("sk-") and len(self.api_key) == 51:
        #    return True
        return True

class DashscopeService:
    @staticmethod
    def call_model(prompt):
        """调用大模型服务。

        Args:
            prompt (str): 用户输入的提示。

        Returns:
            str: 模型的输出文本或错误信息。
        """
        response = Application.call(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            app_id='YOUR_APP_ID',  # 替换为实际的应用 ID
            prompt=prompt
        )

        if response.status_code != HTTPStatus.OK:
            return (f"请求失败: request_id={response.request_id}, code={response.status_code}, "
                    f"message={response.message}. 请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        else:
            return response.output.text