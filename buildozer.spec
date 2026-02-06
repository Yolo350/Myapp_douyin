[app]
# 应用基本信息
title = 抖音续火花工具
package.name = sparktool
package.domain = org.sparktool
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = gitignore,spec
source.exclude_dirs = tests,bin,.buildozer,.git
source.include_dirs = data/  # 确保data文件夹（图标/启动图）被打包

# 主程序入口
main.py = main.py

# 版本信息
version = 1.0.0

# 依赖配置（修复了 python-jnius 问题）
requirements = python3,kivy==2.3.0,airtest==1.4.3,pocoui==1.0.92,pyjnius,requests

# Android核心配置
android.api = 33
android.ndk = 25b
android.ndk_path =
android.sdk_path =
android.tools_path =
android.ant_path =

# 权限配置（适配高版本Android+自动化需求）
android.permissions = INTERNET,ACCESS_WIFI_STATE,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECEIVE_BOOT_COMPLETED,ACTIVITY_RECOGNITION,ACCESS_BACKGROUND_LOCATION,FOREGROUND_SERVICE,SYSTEM_ALERT_WINDOW

# 后台服务保活配置
android.services = org.kivy.android.PythonService:org.kivy.android.PythonService:foreground

# 应用图标
icon.filename = data/icon.jpg

# 启动图配置
splash.filename = data/douyin.jpg
splash.landscape_filename =
splash.duration = 3000
splash.alpha = 1.0
splash.scale = fill

# 屏幕适配
orientation = portrait
fullscreen = 0

# 依赖库补充配置
android.add_jars =
android.add_aars =
android.add_libs_armeabi-v7a =
android.add_libs_arm64-v8a =
android.add_libs_x86 =
android.add_libs_x86_64 =

# Android版本适配
android.enable_androidx = True
android.minapi = 21
android.targetapi = 33
android.ndk_api = 21
android.accept_sdk_license = True

# 构建类型
release = False
debug = True

# 新增：关键修复，确保 python-for-android 正确处理 pyjnius
p4a.source_dir = .buildozer/android/platform/python-for-android
p4a.local_recipes = .buildozer/android/platform/python-for-android/recipes
p4a.bootstrap = sdl2
p4a.ndk = 25b
p4a.api = 33
p4a.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = bin
cache_dir = .buildozer/cache
dont_use_virtualenv = False
virtualenv_dir = .buildozer/virtualenv
allow_hostpython = False
requirements_order = cython,hostpython3,other
log_dir = .buildozer/logs
log_name = buildozer.log

[toolchain]
ndk_version = 25b
ndk_path =
ndk_api = 21
compiler = clang
cxx_compiler = clang++
archs = arm64-v8a,armeabi-v7a
libraries =
include_dirs =
extra_flags =

[app:debug]
android.debug = True
android.manifest.intent_filters =
android.manifest.application_attributes = android:debuggable="true"

[app:release]
android.debug = False
android.keystore =
android.keystore_user =
android.keystore_password =
android.manifest.intent_filters =
android.manifest.application_attributes = android:debuggable="false"
