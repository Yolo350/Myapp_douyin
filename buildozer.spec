[app]
# 应用基本信息
title = 抖音续火花工具
package.name = sparktool
package.domain = org.sparktool
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = gitignore,spec
source.exclude_dirs = tests,bin,.buildozer,.git
source.include_dirs = data/

# 主程序入口
main.py = main.py

# 版本信息
version = 1.0.0

# 依赖配置（已修复 python-jnius 问题）
requirements = python3,kivy==2.3.0,airtest==1.4.3,pocoui==1.0.92,pyjnius,requests

# Android核心配置
android.api = 33
android.ndk = 25b
android.minapi = 21
android.targetapi = 33
android.ndk_api = 21

# 权限配置
android.permissions = INTERNET,ACCESS_WIFI_STATE,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECEIVE_BOOT_COMPLETED,ACTIVITY_RECOGNITION,ACCESS_BACKGROUND_LOCATION,FOREGROUND_SERVICE,SYSTEM_ALERT_WINDOW

# 后台服务保活配置
android.services = org.kivy.android.PythonService:org.kivy.android.PythonService:foreground

# 应用图标与启动图
icon.filename = data/icon.jpg
splash.filename = data/douyin.jpg
splash.duration = 3000
splash.alpha = 1.0
splash.scale = fill

# 屏幕适配
orientation = portrait
fullscreen = 0

# Android版本适配
android.enable_androidx = True
android.accept_sdk_license = True

# 构建类型
release = False
debug = True

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = bin
cache_dir = .buildozer/cache
virtualenv_dir = .buildozer/virtualenv
log_dir = .buildozer/logs

[toolchain]
ndk_version = 25b
ndk_api = 21
compiler = clang
cxx_compiler = clang++
archs = arm64-v8a,armeabi-v7a
