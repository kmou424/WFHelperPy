## WFHelperPy

**WFHelperPy** 是一个使用 Python 开发的 World Flipper 护肝工具

它的诞生是 ~~因为坐共斗车蹲铃铛实在是太肝了~~ 为了让广大弹批能放下手机, 能够腾出更多的时间在工作和生活上, 而不是像[小k](http://github.com/kmou424)一样, 沉迷游戏, 工作爱情两边误 (草)

Features:

- 安全 *(纯脚本, 无读写内存机制)*
- 使用 ADB 控制设备 ~~(好像不太能算特点)~~
- 简洁 *(原因竟是内容少)*
- 易用, User Friendly

~~现在没有QQ群, 等有人用了再建群吧~~



### 安装说明

1. 目前仅支持屏幕分辨率为**720x1280**的设备 (或其他宽高比为 **9:16** 的手机)
2. 控制面板是网页端, 很简易, 也很烂(指技术力), 目前还不支持手机端页面 ~~(绝对不可能是我懒得写)~~
2. **环境要求: Python 3.7.x (3.6.x - 3.8.x 应该都可以)，git**
2. **本软件使用GPL-3.0协议开源并发布, 使用前请仔细了解协议相关事项**



### TODO

- [x] 自动坐铃铛车
- [x] 自动开(灵)车和招募
- [x] 坐车Boss筛选器 (选择性坐车)
- [x] **支持多区服 (国服/台服)**
- [ ] 定时休息
- [x] ~~运行日志 (现在的是残废版, 只能在终端) **print警告**~~
- [ ] 自动换队 (根据属性/Boss指定) ~~为了写简单点还是根据属性指定吧, 反正也大差不差 (逃~~
- [x] 坐互关列表车
- [ ] 自动长草
- [ ] 自动清理单向关注
- [ ] ~~其他功能莫多莫多~~



### 如何安装

#### 1-1. 环境安装与配置

```bash
# 安装前请准备 python3 python-pip git
# 国内用户可选择使用Gitee镜像: https://gitee.com/kmou424/WFHelperPy
$ git clone https://github.com/kmou424/WFHelperPy
$ cd WFHelperPy
# 执行安装脚本
# 将会在本地生成虚拟环境并自动拉取远程模板仓库
$ python install.py
```

安装完成后，程序并不能马上开始运行，请接着往下看。

#### 1-2. (可选) 对于安卓模拟器 (Windows)

如果你是安卓模拟器用户，请将WFHelperPy目录下的`tools`目录内的`Lib/site-packages/adbutils/binaries/adb.exe`复制出来，并替换掉模拟器安装目录下的**模拟器自带的adb**。

以夜神模拟器为例，夜神模拟器自带的adb为模拟器安装目录下的`bin/nox_adb.exe`，我们将`Lib/site-packages/adbutils/binaries/adb.exe`复制出来并重命名为`nox_adb.exe`，覆盖掉夜神模拟器安装目录内的adb。

#### 2. 创建一个会话并开始运行

```bash
# 你可以使用下面的命令来创建一个会话
$ python create.py <panel_port> <session_name>
# panel_port: 你想要的控制面板的端口号
# session_name: 会话名称(自由填写)
# 如下面这样
$ python create.py 5000 main
# 执行这条命令后，程序将会在当前目录下的runners目录中自动创建一个main.sh/.bat的文件
# 相关联的配置文件则是在当前目录下的configs中，文件名为main.ini(首次运行会话时会自动创建)
$ .\runners\main.bat
# Linux/MacOS: ./runners/main.sh
# 注意: 请不要cd到runners目录下执行
# 执行后:
# * Serving Flask app "wfhelper" (lazy loading)
# * Environment: production
#   WARNING: This is a development server. Do not use it in a production deployment.
#   Use a production WSGI server instead.
# * Debug mode: off
# * Restarting with watchdog (windowsapi)
# * Running on http://<IP>:5000/ (Press CTRL+C to quit)
# 看到形似以上内容的输出时，你就可以通过输出内容中显示的地址: <IP>:5000 来访问控制面板
# 此处的 "5000" 是你在创建会话时指定的端口
```

#### 2-3.  多开会话

截至目前版本，WFHelperPy已经完全支持了多开会话，每一个会话的配置文件都是独立的。你可以通过不同的会话连接不同的设备以实现多开控制。

```bash
# 你可以使用下面的命令来创建第二个乃至第n个会话
$ python create.py <panel_port> <seesion_name>
# panel_port: 你想要的控制面板的端口号
# session_name: 会话名称(自由填写)
# 同理，以这样的命令创建的会话，用法依然和 "2. 创建一个会话并开始运行" 中的相同
# 如这下面这样
$ python create.py 5001 main2
$ .\runners\main2.bat
# Linux/MacOS: ./runners/main2.sh
# 注意: 请不要cd到runners目录下执行
# 待到服务启动完成，你同样可以通过输出内容中显示的地址: <IP>:5001 来访问控制面板
```



### 更新

**每次使用软件之前请尽量先执行以下两项更新后再启动**

#### 检查并更新模板图片

```bash
$ python template_updater.py
```

#### 更新主程序

```bash
$ git pull
```



### 其他

#### 检查模板在当前设备界面上的匹配度

```bash
$ python template_test.py <ADB Serial> <模板区服> <模板图片名>
# 例如:
# $ python template_test.py 127.0.0.1:5555 cn Login_interface_sign
# Screenshot: 0.42681159999999996 Seconds
# {'result': (383.0, 871.5), 'rectangle': ((342, 835), (342, 908), (424, 835), (424, 908)), 'confidence': 0.9637399911880493}
# Match image: 0.027701500000000046 Seconds
```

#### 为特殊设备/区服自制模板图片

```bash
# 生成普通模板
$ python template_generator.py <ADB Serial> <模板区服> <模板图片名> <左上角坐标x> <左上角坐标y> <右下角坐标x> <右下角坐标y>
# 执行后会自动截取设备画面, 用坐标截取并生成单通道图片模板, 保存至 template/<模板区服>/<模板图片名>.png
# 对应的坐标可以在lib/constants.py内查找

# 生成Boss头像模板(用于检测Boss)
# 需要在"领主战"->"某个Boss"->点击对应难度旁边绿色的"i"(info)图标来打开Boss信息对话框才能截取
$ python template_boss_generator.py <ADB Serial> <模板区服> <Boss头像模板名>
# 执行后会自动截取设备画面, 用坐标截取并生成单通道Boss头像模板, 保存至 template/<模板区服>/boss/Boss_<Boss头像模板名>.png
# Boss头像模板名 = <BossID>_<Boss难度>
```



### 感谢

- [zdhxiong](https://github.com/zdhxiong)/**[mdui](https://github.com/zdhxiong/mdui)**
- [openatx](https://github.com/openatx)/**[adbutils](https://github.com/openatx/adbutils)**
- [NetEaseGame](https://github.com/NetEaseGame)/**[aircv](https://github.com/NetEaseGame/aircv)**
- [pallets](https://github.com/pallets)/**[flask](https://github.com/pallets/flask)**
- [opencv](https://github.com/opencv)/**[opencv-python](https://github.com/opencv/opencv-python)**
- [numpy](https://github.com/numpy)/**[numpy](https://github.com/numpy/numpy)**
- [psf](https://github.com/psf)/**[requests](https://github.com/psf/requests)**



### 开源协议

[GPL-3.0](LICENSE)