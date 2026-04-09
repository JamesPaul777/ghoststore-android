[app]
title = GhostStore
package.name = ghoststore
package.domain = org.ghoststore
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0.0
requirements = python3,kivy==2.3.0,zstandard,cryptography,pillow,numpy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.3.0
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET
android.api = 33
android.minapi = 21
android.ndk = 27c
android.sdk = 33
android.archs = arm64-v8a
android.allow_backup = True
android.logcat_filters = *:S python:D
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653

[buildozer]
log_level = 2
warn_on_root = 1