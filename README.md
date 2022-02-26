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
2. **本软件使用GPL-3.0协议开源并发布, 使用前请仔细了解协议相关事项**



### TODO

- [x] 自动坐铃铛车
- [ ] 自动开(灵)车和招募
- [x] 坐车Boss筛选器 (选择性坐车)
- [x] **支持多区服 (国服/台服)**
- [ ] 定时休息
- [x] ~~运行日志 (现在的是残废版, 只能在终端) **print警告**~~
- [ ] 自动换队 (根据属性/Boss指定) ~~为了写简单点还是根据属性指定吧, 反正也大差不差 (逃~~
- [ ] 坐互关列表车
- [ ] 自动长草
- [ ] 自动清理单向关注
- [ ] ~~其他功能莫多莫多~~



### 如何安装

#### 1. 环境安装与配置

```shell
# 安装前请准备 python3 python-pip git
foo@foobar: /<directory># git clone https://github.com/kmou424/WFHelperPy
foo@foobar: /<directory># cd WFHelperPy
foo@foobar: /<directory>/WFHelperPy# pip install -r requirements.txt
```

#### 2. 获取模板图片(必需)

```shell
# 为了方便后续模板更新, 模板仓库放在了gitee
# 仓库地址: https://gitee.com/kmou424/wfhelperpy_template
foo@foobar: /<directory>/WFHelperPy# git clone https://gitee.com/kmou424/wfhelperpy_template template
```

#### 3. 运行并访问控制面板

```shell
foo@foobar: /<directory>/WFHelperPy# python wfhelper.py
# 例如:
# foo@foobar: /<directory>/WFHelperPy# python wfhelper.py
# * Serving Flask app "wfhelper" (lazy loading)
# * Environment: production
#   WARNING: This is a development server. Do not use it in a production deployment.
#   Use a production WSGI server instead.
# * Debug mode: off
# * Restarting with watchdog (windowsapi)
# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
# 访问 http://127.0.0.1:5000/ 即可进入控制面板
```



### 更新

#### 检查并更新模板图片

```shell
# 检查更新前请确保完成过第一次的获取模板图片
foo@foobar: /<directory>/WFHelperPy# python template_updater.py
```

- 此方法虽然也可以用来第一次获取所有模板图片, 但是速度会**非常非常慢**, 远远不如Git

#### 更新主程序

```shell
foo@foobar: /<directory>/WFHelperPy# git pull
```



### 其他

#### 检查模板在当前设备界面上的匹配度

```shell
foo@foobar: /<directory>/WFHelperPy# python template_test.py <模板区服> <模板图片名>
# 例如:
# foo@foobar: /<directory>/WFHelperPy# python template_test.py cn Login_interface_sign
# Screenshot: 0.42681159999999996 Seconds
# {'result': (383.0, 871.5), 'rectangle': ((342, 835), (342, 908), (424, 835), (424, 908)), 'confidence': 0.9637399911880493}
# Match image: 0.027701500000000046 Seconds
```

#### 为特殊设备/区服自制模板图片

```shell
# 生成普通模板
foo@foobar: /<directory>/WFHelperPy# python template_generator.py <模板区服> <模板图片名> <左上角坐标x> <左上角坐标y> <右下角坐标x> <右下角坐标y>
# 执行后会自动截取设备画面, 用坐标截取并生成单通道图片模板, 保存至 template/<模板区服>/<模板图片名>.png
# 对应的坐标可以在lib/constants.py内查找

# 生成Boss头像模板(用于检测Boss)
# 需要在"领主战"->"某个Boss"->点击对应难度旁边绿色的"i"(info)图标来打开Boss信息对话框才能截取
foo@foobar: /<directory>/WFHelperPy# python template_boss_generator.py <模板区服> <Boss头像模板名>
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