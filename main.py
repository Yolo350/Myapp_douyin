from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.config import Config
from kivy.clock import Clock
from kivy.utils import platform
import sys
import os
import threading
import text
import time

# 1. 终端编码配置
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.system("chcp 65001 >nul")

# 2. 字体适配
if platform == 'android':
    LabelBase.register(DEFAULT_FONT, "/system/fonts/DroidSansFallback.ttf")
    Config.set('kivy', 'default_font', [DEFAULT_FONT, "/system/fonts/DroidSansFallback.ttf"])
else:
    try:
        LabelBase.register(DEFAULT_FONT, "C:/Windows/Fonts/simsun.ttc")
    except:
        LabelBase.register(DEFAULT_FONT, "C:\\Windows\\Fonts\\simsun.ttc")
    Config.set('kivy', 'default_font', [DEFAULT_FONT, "C:/Windows/Fonts/simsun.ttc"])
Config.write()

# 3. 窗口配置
Window.size = (360, 640)

# 4. 全局配置
app_config = {"selected_app": "抖音", "single_friend": "", "multi_friends": ["", "", "", "", ""], "custom_msg": ""}
loading_popup = None


# 5. 后台执行辅助类（关键修改：去掉Home键，不退回桌面）
class BackgroundExecutor:
    @staticmethod
    def move_app_to_background(package_name):
        if platform == 'android':
            try:
                from jnius import autoclass
                # 仅移到后台任务栈，不发送Home键（不退回桌面）
                ActivityManager = autoclass('android.app.ActivityManager')
                Context = autoclass('android.content.Context')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')

                activity = PythonActivity.mActivity
                am = activity.getSystemService(Context.ACTIVITY_SERVICE)
                # 核心：仅将抖音移到后台，当前前台APP保持不变
                am.moveTaskToBack(am.getRunningTasks(1).get(0).id, ActivityManager.MOVE_TASK_WITH_HOME)

                time.sleep(1.5)  # 简短缓冲，稳定后台状态
                return True
            except Exception as e:
                print(f"后台切换失败：{e}")
                return False
        return False

    @staticmethod
    def bring_app_to_foreground(package_name):
        if platform == 'android':
            try:
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                Context = autoclass('android.content.Context')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                intent = activity.getPackageManager().getLaunchIntentForPackage(package_name)
                intent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
                activity.startActivity(intent)
                return True
            except Exception as e:
                print(f"前台恢复失败：{e}")
                return False
        return False

    @staticmethod
    def get_current_foreground_app():
        if platform == 'android':
            try:
                from jnius import autoclass
                Context = autoclass('android.content.Context')
                ActivityManager = autoclass('android.app.ActivityManager')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                am = PythonActivity.mActivity.getSystemService(Context.ACTIVITY_SERVICE)
                return am.getRunningTasks(1).get(0).topActivity.packageName
            except Exception as e:
                print(f"获取前台APP失败：{e}")
        return None


# 6. Airtest核心调用
def single_spark_airtest(app_name, friend_name, custom_msg):
    try:
        print(f"后台给{app_name}好友{friend_name}续火花（不退回桌面）")
        qe = text.single_friend(app_name, friend_name, custom_msg)
        if qe == "好友不存在":
            return "好友不存在"
        else:
            return True
    except Exception as e:
        print(f"单好友续火花失败：{e}")
        return False


def multi_spark_airtest(app_name, friend_list, custom_msg):
    try:
        valid_friends = [name for name in friend_list if name.strip()]
        if not valid_friends:
            return False
        print(f"后台给{app_name}好友{valid_friends}批量续火花（不退回桌面）")
        we = text.many_friends(app_name, friend_list, custom_msg)
        if we is True:
            return True
        else:
            return we
    except Exception as e:
        print(f"多好友续火花失败：{e}")
        return False


# 7. 弹窗组件
def show_popup(title, content):
    popup_content = BoxLayout(orientation="vertical", spacing=15, padding=20)
    popup_label = Label(text=content, halign="center")
    close_btn = Button(text="好的", size_hint=(1, 0.4))
    popup_content.add_widget(popup_label)
    popup_content.add_widget(close_btn)

    popup = Popup(
        title=title,
        content=popup_content,
        size_hint=(0.7, 0.3),
        auto_dismiss=False
    )
    close_btn.bind(on_press=lambda x: popup.dismiss())
    popup.open()


def show_loading_popup(content):
    global loading_popup
    loading_content = BoxLayout(orientation="vertical", padding=30)
    loading_label = Label(text=content, halign="center", font_size=16, color=(1, 1, 1, 1))
    loading_content.add_widget(loading_label)

    loading_popup = Popup(
        title="加载中",
        content=loading_content,
        size_hint=(0.8, 0.2),
        auto_dismiss=False,
        background_color=(0, 0, 0, 0.8),
        separator_color=(1, 1, 1, 1)
    )
    loading_popup.open()


def close_loading_popup():
    global loading_popup
    if loading_popup:
        loading_popup.dismiss()
        loading_popup = None


# 8. 主UI布局
class SparkAppUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 15
        self.spacing = 10
        self._build_app_select()
        self._build_custom_msg()
        self._build_single_spark()
        self._build_multi_spark()

    # APP选择区
    def _build_app_select(self):
        app_box = BoxLayout(orientation="horizontal", spacing=10, size_hint=(1, 0.1))
        app_box.add_widget(Label(text="选择APP："))
        self.douyin_btn = ToggleButton(text="抖音", group="app", state="down", on_press=self.select_app)
        self.douyin_speed_btn = ToggleButton(text="抖音极速版", group="app", on_press=self.select_app)
        app_box.add_widget(self.douyin_btn)
        app_box.add_widget(self.douyin_speed_btn)
        self.add_widget(app_box)

    def select_app(self, instance):
        app_config["selected_app"] = instance.text

    # 自定义消息区
    def _build_custom_msg(self):
        msg_box = BoxLayout(orientation="vertical", spacing=8, size_hint=(1, 0.15))
        msg_box.add_widget(Label(text="【自定义发送消息】", bold=True))
        self.custom_msg_input = TextInput(
            hint_text="输入要发送的消息",
            multiline=False,
            text=app_config["custom_msg"]
        )
        msg_box.add_widget(self.custom_msg_input)
        msg_btn_box = BoxLayout(orientation="horizontal", spacing=10)
        msg_btn_box.add_widget(Button(text="保存", on_press=self.save_custom_msg))
        msg_box.add_widget(msg_btn_box)
        self.add_widget(msg_box)

    def save_custom_msg(self, instance):
        msg = self.custom_msg_input.text.strip()
        if not msg:
            show_popup("提示", "消息内容不能为空！")
            return
        app_config["custom_msg"] = msg
        show_popup("成功", "消息已保存！")

    # 单好友续火花区
    def _build_single_spark(self):
        single_box = BoxLayout(orientation="vertical", spacing=8, size_hint=(1, 0.25))
        single_box.add_widget(Label(text="【单好友续火花】", bold=True))
        self.single_friend_input = TextInput(hint_text="输入好友昵称", multiline=False)
        single_box.add_widget(self.single_friend_input)
        single_btn_box = BoxLayout(orientation="horizontal", spacing=10)
        single_btn_box.add_widget(Button(text="保存昵称", on_press=self.save_single_friend))
        single_btn_box.add_widget(Button(text="一键续火花", on_press=self.run_single_spark))
        single_box.add_widget(single_btn_box)
        self.add_widget(single_box)

    def save_single_friend(self, instance):
        name = self.single_friend_input.text.strip()
        if not name:
            show_popup("提示", "昵称不能为空！")
            return
        app_config["single_friend"] = name
        show_popup("成功", "昵称已保存！")

    # 单好友执行（不退回桌面）
    def run_single_spark(self, instance):
        app_name = app_config["selected_app"]
        input_name = self.single_friend_input.text.strip()
        friend_name = input_name if input_name else app_config["single_friend"]

        if not friend_name:
            show_popup("提示", "请先输入好友昵称！")
            return
        custom_msg = self.custom_msg_input.text.strip() or app_config["custom_msg"]
        if not custom_msg:
            show_popup("提示", "请先输入发送消息！")
            return

        show_loading_popup("正在后台续火花，请稍等")

        def airtest_task():
            # 无需记录/恢复前台APP，保持当前状态
            success = single_spark_airtest(app_name, friend_name, custom_msg)
            Clock.schedule_once(lambda dt: self.show_single_result(success, friend_name))

        threading.Thread(target=airtest_task, daemon=True).start()

    def show_single_result(self, success, friend_name):
        close_loading_popup()
        if success is True:
            show_popup("成功", "续火花成功！")
        elif success == "好友不存在":
            show_popup("失败", f"昵称为:'{friend_name}'的好友不存在！")
        else:
            show_popup("失败", "续火花失败，请检查权限和脚本！")

    # 多好友续火花区
    def _build_multi_spark(self):
        multi_box = BoxLayout(orientation="vertical", spacing=8, size_hint=(1, 0.55))
        multi_box.add_widget(Label(text="【多好友续火花（最多5名）】", bold=True))
        self.multi_inputs = []
        for i in range(5):
            input_box = TextInput(hint_text=f"好友昵称{i + 1}", multiline=False)
            self.multi_inputs.append(input_box)
            multi_box.add_widget(input_box)
        multi_btn_box = BoxLayout(orientation="horizontal", spacing=10)
        multi_btn_box.add_widget(Button(text="保存所有昵称", on_press=self.save_multi_friends))
        multi_btn_box.add_widget(Button(text="一键续火花", on_press=self.run_multi_spark))
        multi_box.add_widget(multi_btn_box)
        self.add_widget(multi_box)

    def save_multi_friends(self, instance):
        friend_list = [input.text.strip() for input in self.multi_inputs]
        if not any(friend_list):
            show_popup("提示", "至少填写1个好友昵称！")
            return
        app_config["multi_friends"] = friend_list
        show_popup("成功", "所有昵称已保存！")

    # 多好友执行（不退回桌面）
    def run_multi_spark(self, instance):
        app_name = app_config["selected_app"]
        input_friends = [inp.text.strip() for inp in self.multi_inputs]
        friend_list = []
        for idx, inp_name in enumerate(input_friends):
            friend_name = inp_name if inp_name else app_config["multi_friends"][idx]
            friend_list.append(friend_name)

        valid_friends = [name for name in friend_list if name.strip()]
        if not valid_friends:
            show_popup("提示", "请先填写好友昵称！")
            return
        custom_msg = self.custom_msg_input.text.strip() or app_config["custom_msg"]
        if not custom_msg:
            show_popup("提示", "请先输入发送消息！")
            return

        show_loading_popup("正在后台批量续火花，请稍等")

        def airtest_task():
            success = multi_spark_airtest(app_name, friend_list, custom_msg)
            Clock.schedule_once(lambda dt: self.show_multi_result(success))

        threading.Thread(target=airtest_task, daemon=True).start()

    def show_multi_result(self, success):
        close_loading_popup()
        if success is True:
            show_popup("成功", "后台批量续火花成功！")
        elif isinstance(success, str):
            show_popup("失败", success)
        else:
            show_popup("失败", "续火花失败，请检查权限和脚本！")


# 9. 启动APP
class SparkApp(App):
    def build(self):
        self.title = "抖音续火花工具"
        return SparkAppUI()


if __name__ == "__main__":
    SparkApp().run()
