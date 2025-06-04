[app]

# (str) Title of your app
title = FoodSnap

# (str) Package name
package.name = foodsnap

# (str) Package domain (unique)
package.domain = org.chaotic.foodsnap

# (str) Source code where the main.py is located
source.dir = app
source.include_exts = py,png,jpg,kv,ttf,txt,tflite,sh

# (list) Permissions
android.permissions = INTERNET,CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Buildozer will copy assets from here into assets
android.add_assets = assets/model.tflite:assets, assets/labels.txt:assets

# (str) Icon
icon.filename = app/assets/icon.png

# (list) Application requirements
requirements = python3,kivy,kivymd,tflite-runtime,requests,pillow,numpy,plyer

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Android API level target
android.api = 31
android.minapi = 21
android.sdk = 31

# (str) Keystore (for Google Play release you’d add your keystore)
# android.keystore = /path/to/keystore
# android.keystore_password = yourpass
# android.keyalias = foodsnapkey
# android.keyalias_password = yourpass

# (int) orientation: portrait (1) or landscape (0)
orientation = portrait
