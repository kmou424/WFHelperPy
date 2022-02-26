import cv2
from flask import Flask, jsonify, render_template, request

from lib.config import ConfigManager
from lib.constants import ConfigOptions, ConfigSections
from lib.times import Time
from modules.tracker import Tracker
from lib.resource import ResourceJson

app = Flask(__name__, template_folder='web')
cfgMan = ConfigManager('config.ini', writable=True)
tracker = Tracker()
result = 0
data = {
    # Main
    ConfigOptions.TRACK_BELL_SWITCH.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_MAIN.get())
        .getBoolean(ConfigOptions.TRACK_BELL_SWITCH.get()),
    ConfigOptions.TRACK_BOSS_LIST_SWITCH.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_MAIN.get())
        .getBoolean(ConfigOptions.TRACK_BOSS_LIST_SWITCH.get()),
    # Custom
    ConfigOptions.BELL_SELECTOR_MODE.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        .getString(ConfigOptions.BELL_SELECTOR_MODE.get(), default='boss_selector'),
    ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        .getString(ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get()),
    ConfigOptions.BOSS_SELECTOR.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        .getString(ConfigOptions.BOSS_SELECTOR.get()),
    # Settings
    ConfigOptions.DEVICE_ADB_SERIAL.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_SETTINGS.get())
        .getString(ConfigOptions.DEVICE_ADB_SERIAL.get()),
    ConfigOptions.GAME_SERVER.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_SETTINGS.get())
        .getString(ConfigOptions.GAME_SERVER.get(), default='cn'),
    ConfigOptions.ENABLE_TAB_LOG_SWITCH.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_SETTINGS.get())
        .getBoolean(ConfigOptions.ENABLE_TAB_LOG_SWITCH.get()),
    'RegionChanged': False
}


@app.route("/", methods=["POST", "GET", "DELETE"])
def index():
    if request.method == 'POST':
        return jsonify(data)
    else:
        return render_template('index.html', form_visibility='hidden')


@app.route("/action", methods=["POST"])
def action():
    if request.method == 'POST':
        what = request.form['what']
        if what == 'refreshState':
            global result
            ret = result
            result = 0
            return jsonify({
                'Running': tracker.running(),
                'Status': tracker.status(),
                'Result': ret
            })
        if what == 'takeScreenshotForNow':
            screenshot = tracker.adb_tools.takeScreenShot()
            if screenshot is not None:
                # TODO: 路径完整性和可用性检查
                cv2.imwrite(format(Time.getTimeStampForNow(), "%d.png"), screenshot)
        if what == 'getBossInfoJson':
            return jsonify(ResourceJson.getBossInfo(data[ConfigOptions.GAME_SERVER.get()]))
        if what == 'getSelectedBossInfoJson':
            return jsonify(
                cfgMan
                .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
                .getString(ConfigOptions.BOSS_SELECTOR.get())
                .split(',')
            )


@app.route("/runService", methods=['POST'])
def runService():
    if request.method == "POST":
        cfgMan.save()
        global result
        result = tracker.run(cfgMan
                             .selectSection(ConfigSections.SECTION_SETTINGS.get())
                             .getString(ConfigOptions.DEVICE_ADB_SERIAL.get()))
    return jsonify(data)


@app.route("/stopService", methods=['POST'])
def stopService():
    if request.method == "POST":
        global result
        result = tracker.stop()
    return jsonify(data)


@app.route("/saveAllData", methods=['POST'])
def saveAllData():
    if request.method == "POST":
        # For main panel
        cfgMan.checkoutSection(ConfigSections.SECTION_MAIN.get())
        # TRACK_BELL_SWITCH
        cfgMan.setValue(ConfigOptions.TRACK_BELL_SWITCH.get(),
                        request.form[ConfigOptions.TRACK_BELL_SWITCH.get()])
        data[ConfigOptions.TRACK_BELL_SWITCH.get()] = cfgMan.getBoolean(ConfigOptions.TRACK_BELL_SWITCH.get())
        # TRACK_BOSS_LIST_SWITCH
        cfgMan.setValue(ConfigOptions.TRACK_BOSS_LIST_SWITCH.get(),
                        request.form[ConfigOptions.TRACK_BOSS_LIST_SWITCH.get()])
        data[ConfigOptions.TRACK_BOSS_LIST_SWITCH.get()] = cfgMan \
            .getBoolean(ConfigOptions.TRACK_BOSS_LIST_SWITCH.get())

        # For custom
        cfgMan.checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        # BELL_SELECTOR_MODE
        cfgMan.setValue(ConfigOptions.BELL_SELECTOR_MODE.get(),
                        request.form[ConfigOptions.BELL_SELECTOR_MODE.get()])
        data[ConfigOptions.BELL_SELECTOR_MODE.get()] = cfgMan.getString(ConfigOptions.BELL_SELECTOR_MODE.get())
        # BOSS_SELECTOR
        cfgMan.setValue(ConfigOptions.BOSS_SELECTOR.get(),
                        request.form[ConfigOptions.BOSS_SELECTOR.get()].replace(' ', ''))
        data[ConfigOptions.BOSS_SELECTOR.get()] = cfgMan.getString(ConfigOptions.BOSS_SELECTOR.get())
        # BELL_BOSS_SELECTOR_ADVANCED
        cfgMan.setValue(ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get(),
                        request.form[ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get()].replace(' ', ''))
        data[ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get()] = cfgMan.getString(
            ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get())

        # For settings
        cfgMan.checkoutSection(ConfigSections.SECTION_SETTINGS.get())
        # DEVICE_ADB_SERIAL
        cfgMan.setValue(ConfigOptions.DEVICE_ADB_SERIAL.get(),
                        request.form[ConfigOptions.DEVICE_ADB_SERIAL.get()])
        data[ConfigOptions.DEVICE_ADB_SERIAL.get()] = cfgMan.getString(ConfigOptions.DEVICE_ADB_SERIAL.get())
        # GAME_SERVER
        # 特判服务器是否已被修改
        data['RegionChanged'] = \
            cfgMan.getString(ConfigOptions.GAME_SERVER.get()) != request.form[ConfigOptions.GAME_SERVER.get()]
        cfgMan.setValue(ConfigOptions.GAME_SERVER.get(),
                        request.form[ConfigOptions.GAME_SERVER.get()])
        data[ConfigOptions.GAME_SERVER.get()] = cfgMan.getString(ConfigOptions.GAME_SERVER.get())
        # ENABLE_TAB_LOG_SWITCH
        cfgMan.setValue(ConfigOptions.ENABLE_TAB_LOG_SWITCH.get(),
                        request.form[ConfigOptions.ENABLE_TAB_LOG_SWITCH.get()])
        data[ConfigOptions.ENABLE_TAB_LOG_SWITCH.get()] = cfgMan.getBoolean(ConfigOptions.ENABLE_TAB_LOG_SWITCH.get())
        cfgMan.save()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=cfgMan.checkoutSection('Debug').getBoolean('enabled'), host='127.0.0.1', port=5000)
