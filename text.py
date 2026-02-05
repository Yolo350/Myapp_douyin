from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import sys
from kivy.utils import platform


# 关键修改：后台切换函数去掉Home键，不退回桌面
def move_to_background(package_name):
    if platform == 'android' and 'jnius' in sys.modules:
        try:
            from jnius import autoclass
            # 仅将抖音移到后台任务栈，保持当前前台APP不变
            ActivityManager = autoclass('android.app.ActivityManager')
            Context = autoclass('android.content.Context')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            activity = PythonActivity.mActivity
            am = activity.getSystemService(Context.ACTIVITY_SERVICE)
            task_id = am.getRunningTasks(1).get(0).id
            am.moveTaskToBack(task_id, ActivityManager.MOVE_TASK_WITH_HOME)

            sleep(1.5)  # 简短缓冲，稳定后台状态
            return True
        except Exception as e:
            print(f"后台切换失败：{e}")
            return False
    return False


# Airtest初始化
auto_setup(__file__, logdir=False, devices=["Android:///"])
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
sleep(2)


# 单好友续火花（不退回桌面）
def single_friend(appname1, firend, custom_msg):
    an1 = "com.ss.android.ugc.aweme" if appname1 == "抖音" else "com.ss.android.ugc.aweme.lite"

    # 启动APP后快速移到后台，不影响前台
    start_app(an1)
    sleep(3)
    move_to_background(an1)
    sleep(1.5)  # 稳定后台，避免唤醒

    try:
        # 后台操作抖音
        poco(text="消息").click()
        sleep(1)
        search_box = poco(desc="搜索")
        search_box.click()
        poco(f"{an1}:id/et_search_kw").set_text(firend)
        sleep(1)
        pan = poco(text="发私信")
        pan.click()
        sleep(1)
        poco(f"{an1}:id/msg_et").set_text(custom_msg)
        poco(desc="发送").click()
        sleep(1)
        stop_app(an1)
        return "成功"
    except Exception as e:
        print(f"单好友后台执行异常：{e}")
        stop_app(an1)
        return "好友不存在"


# 多好友续火花（不退回桌面）
def many_friends(appname2, firends, custom_msg):
    an2 = "com.ss.android.ugc.aweme.lite" if appname2 == "抖音极速版" else "com.ss.android.ugc.aweme"

    start_app(an2)
    sleep(3)
    move_to_background(an2)
    sleep(1.5)

    try:
        poco(text="消息").click()
        sleep(1)
        search_box = poco(desc="搜索")
        search_box.click()
        sleep(1)

        target_nickname = {"name1": firends[0], "name2": firends[1], "name3": firends[2], "name4": firends[3],
                           "name5": firends[4]}
        for val in target_nickname.values():
            if val.strip() == "":
                continue
            poco(f"{an2}:id/et_search_kw").set_text(val)
            sleep(1)
            pan = poco(text="发私信")
            pan.click()
            sleep(1)
            poco(f"{an2}:id/msg_et").set_text(custom_msg)
            poco(desc="发送").click()
            sleep(1)
            poco(desc="返回").click()
            sleep(1)

        stop_app(an2)
        return True
    except Exception as e:
        print(f"多好友后台执行异常：{e}")
        stop_app(an2)
        return f"昵称为:'{val}'的好友不存在!"
