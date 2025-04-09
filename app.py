import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
from chat import start_wechat_service
from llm import GPT
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("微信智能客服")
        self.setGeometry(300, 300, 400, 200)

        self.layout = QVBoxLayout()

        self.status_label = QLabel("请先登录微信")
        self.layout.addWidget(self.status_label)

        self.api_key_label = QLabel("API Key:")
        self.layout.addWidget(self.api_key_label)

        self.api_key_input = QLineEdit()
        self.api_key_input.setText("")
        self.layout.addWidget(self.api_key_input)

        self.app_id_label = QLabel("App ID:")
        self.layout.addWidget(self.app_id_label)

        self.app_id_input = QLineEdit()
        self.app_id_input.setText("")
        self.layout.addWidget(self.app_id_input)

        self.start_button = QPushButton("启动客服")
        self.start_button.clicked.connect(self.start_service)
        self.layout.addWidget(self.start_button)

        self.check_login_button = QPushButton("检测微信登录")
        self.check_login_button.clicked.connect(self.check_wechat_login)
        self.layout.addWidget(self.check_login_button)

        self.model_input_label = QLabel("输入提示:")
        self.layout.addWidget(self.model_input_label)

        self.model_input = QLineEdit()
        self.layout.addWidget(self.model_input)

        self.call_model_button = QPushButton("调用大模型")
        self.call_model_button.clicked.connect(self.call_model_with_app_id)
        self.layout.addWidget(self.call_model_button)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def start_service(self):
        api_key = self.api_key_input.text()
        app_id = self.app_id_input.text()
        if not api_key or not app_id:
            QMessageBox.warning(self, "错误", "请输入 API Key 和 App ID")
            return
        # if not api_key:
        #     QMessageBox.warning(self, "错误", "请输入 API Key")
        #     return

        #gpt = GPT(api_key=api_key)
        # if not gpt.validate_api_key():
        #     QMessageBox.warning(self, "错误", "API Key 无效")
        #     return

        listen_list = ['Agent', '🐎']  # 监听对象列表
        threading.Thread(target=start_wechat_service, args=(api_key, app_id, "你是一个智能助手，用于回复人们的各种问题", listen_list), daemon=True).start()
        self.status_label.setText("客服已启动")

    def check_wechat_login(self):
        try:
            from wxauto import WeChat
            wx = WeChat()
            if wx.GetSessionList():
                QMessageBox.information(self, "状态", "微信已登录")
            else:
                QMessageBox.warning(self, "状态", "微信未登录")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"检测失败: {str(e)}")

    def call_model(self):
        prompt = self.model_input.text()
        if not prompt:
            QMessageBox.warning(self, "错误", "请输入提示信息")
            return

        from llm import DashscopeService
        result = DashscopeService.call_model(prompt)
        QMessageBox.information(self, "模型回复", result)

    def call_model_with_app_id(self):
        api_key = self.api_key_input.text()
        app_id = self.app_id_input.text()
        if not api_key or not app_id:
            QMessageBox.warning(self, "错误", "请输入 API Key 和 App ID")
            return

        from dashscope import Application
        from http import HTTPStatus

        # prompt = self.model_input.text()
        # if not prompt:
        #     QMessageBox.warning(self, "错误", "请输入提示信息")
        #     return

        try:
            response = Application.call(
                api_key=api_key,
                app_id=app_id,
                prompt=prompt
            )

            if response.status_code != HTTPStatus.OK:
                QMessageBox.critical(self, "错误", f"请求失败: {response.message}")
            else:
                QMessageBox.information(self, "模型回复", response.output.text)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"调用失败: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
