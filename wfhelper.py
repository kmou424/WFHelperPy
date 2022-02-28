import cv2
from flask import Flask, jsonify, render_template, request

from lib.config import ConfigManager
from lib.constants import ConfigOptions, ConfigSections, ConfigValues
from lib.times import Time
from modules.tracker import Tracker
from lib.resource import ResourceJson

app = Flask(__name__, template_folder='web')
cfgMan = ConfigManager('config.ini', writable=True)
tracker = Tracker()
result = 0
data = {
    # Main
    ConfigOptions.GAMING_MODE_MAIN.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_MAIN.get())
        .getString(ConfigOptions.GAMING_MODE_MAIN.get(), default='room_guest'),
    ConfigOptions.TRACK_BELL_SWITCH.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_MAIN.get())
        .getBoolean(ConfigOptions.TRACK_BELL_SWITCH.get()),
    ConfigOptions.TRACK_BOSS_LIST_SWITCH.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_MAIN.get())
        .getBoolean(ConfigOptions.TRACK_BOSS_LIST_SWITCH.get()),
    ConfigOptions.ROOM_CREATOR_SWITCH.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_MAIN.get())
        .getBoolean(ConfigOptions.ROOM_CREATOR_SWITCH.get()),
    # Custom
    ConfigOptions.BELL_SELECTOR_MODE.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        .getString(ConfigOptions.BELL_SELECTOR_MODE.get(), default='boss_selector'),
    ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        .getString(ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get()),
    ConfigOptions.ROOM_CREATOR_GHOST_MODE.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        .getString(ConfigOptions.ROOM_CREATOR_GHOST_MODE.get(), ConfigValues.COMMON_ENABLE.get()),
    ConfigOptions.ROOM_CREATOR_GHOST_ESCAPE_TIME.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        .getString(ConfigOptions.ROOM_CREATOR_GHOST_ESCAPE_TIME.get(), '5'),
    ConfigOptions.RECRUITMENT_MODE.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        .getString(ConfigOptions.RECRUITMENT_MODE.get(), 'true_false_false'),
    ConfigOptions.ROOM_CREATOR_BOSS_SELECTOR.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        .getString(ConfigOptions.ROOM_CREATOR_BOSS_SELECTOR.get()),
    ConfigOptions.COMMON_BOSS_SELECTOR.get():
        cfgMan
        .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        .getString(ConfigOptions.COMMON_BOSS_SELECTOR.get()),
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
        if what == 'getStoredBossInfoJson':
            return jsonify(
                {
                    ConfigOptions.COMMON_BOSS_SELECTOR.get(): cfgMan
                    .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
                    .getString(ConfigOptions.COMMON_BOSS_SELECTOR.get())
                    .split(','),
                    ConfigOptions.ROOM_CREATOR_BOSS_SELECTOR.get(): cfgMan
                    .checkoutSection(ConfigSections.SECTION_CUSTOM.get())
                    .getString(ConfigOptions.ROOM_CREATOR_BOSS_SELECTOR.get())
                }
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
        # GAMING_MODE_MAIN
        cfgMan.setValue(ConfigOptions.GAMING_MODE_MAIN.get(),
                        request.form[ConfigOptions.GAMING_MODE_MAIN.get()])
        data[ConfigOptions.GAMING_MODE_MAIN.get()] = cfgMan.getString(ConfigOptions.GAMING_MODE_MAIN.get())
        # TRACK_BELL_SWITCH
        cfgMan.setValue(ConfigOptions.TRACK_BELL_SWITCH.get(),
                        request.form[ConfigOptions.TRACK_BELL_SWITCH.get()])
        data[ConfigOptions.TRACK_BELL_SWITCH.get()] = cfgMan.getBoolean(ConfigOptions.TRACK_BELL_SWITCH.get())
        # TRACK_BOSS_LIST_SWITCH
        cfgMan.setValue(ConfigOptions.TRACK_BOSS_LIST_SWITCH.get(),
                        request.form[ConfigOptions.TRACK_BOSS_LIST_SWITCH.get()])
        data[ConfigOptions.TRACK_BOSS_LIST_SWITCH.get()] = cfgMan \
            .getBoolean(ConfigOptions.TRACK_BOSS_LIST_SWITCH.get())
        # ROOM_CREATOR_SWITCH
        cfgMan.setValue(ConfigOptions.ROOM_CREATOR_SWITCH.get(),
                        request.form[ConfigOptions.ROOM_CREATOR_SWITCH.get()])
        data[ConfigOptions.ROOM_CREATOR_SWITCH.get()] = cfgMan \
            .getBoolean(ConfigOptions.ROOM_CREATOR_SWITCH.get())

        # For custom
        cfgMan.checkoutSection(ConfigSections.SECTION_CUSTOM.get())
        # BELL_SELECTOR_MODE
        cfgMan.setValue(ConfigOptions.BELL_SELECTOR_MODE.get(),
                        request.form[ConfigOptions.BELL_SELECTOR_MODE.get()])
        data[ConfigOptions.BELL_SELECTOR_MODE.get()] = cfgMan.getString(ConfigOptions.BELL_SELECTOR_MODE.get())
        # BELL_BOSS_SELECTOR_ADVANCED
        cfgMan.setValue(ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get(),
                        request.form[ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get()].replace(' ', ''))
        data[ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get()] = cfgMan.getString(
            ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get())
        # ROOM_CREATOR_GHOST_MODE
        cfgMan.setValue(ConfigOptions.ROOM_CREATOR_GHOST_MODE.get(),
                        request.form[ConfigOptions.ROOM_CREATOR_GHOST_MODE.get()])
        data[ConfigOptions.ROOM_CREATOR_GHOST_MODE.get()] = cfgMan.getString(
            ConfigOptions.ROOM_CREATOR_GHOST_MODE.get())
        # ROOM_CREATOR_GHOST_ESCAPE_TIME
        cfgMan.setValue(ConfigOptions.ROOM_CREATOR_GHOST_ESCAPE_TIME.get(),
                        str(request.form[ConfigOptions.ROOM_CREATOR_GHOST_ESCAPE_TIME.get()]))
        data[ConfigOptions.ROOM_CREATOR_GHOST_ESCAPE_TIME.get()] = cfgMan.getString(
            ConfigOptions.ROOM_CREATOR_GHOST_ESCAPE_TIME.get())
        # RECRUITMENT_MODE
        cfgMan.setValue(ConfigOptions.RECRUITMENT_MODE.get(),
                        request.form[ConfigOptions.RECRUITMENT_MODE.get()])
        data[ConfigOptions.RECRUITMENT_MODE.get()] = cfgMan.getString(
            ConfigOptions.RECRUITMENT_MODE.get())
        # ROOM_CREATOR_BOSS_SELECTOR
        cfgMan.setValue(ConfigOptions.ROOM_CREATOR_BOSS_SELECTOR.get(),
                        request.form[ConfigOptions.ROOM_CREATOR_BOSS_SELECTOR.get()])
        data[ConfigOptions.ROOM_CREATOR_BOSS_SELECTOR.get()] = cfgMan.getString(
            ConfigOptions.ROOM_CREATOR_BOSS_SELECTOR.get())
        # COMMON_BOSS_SELECTOR
        cfgMan.setValue(ConfigOptions.COMMON_BOSS_SELECTOR.get(),
                        request.form[ConfigOptions.COMMON_BOSS_SELECTOR.get()].replace(' ', ''))
        data[ConfigOptions.COMMON_BOSS_SELECTOR.get()] = cfgMan.getString(ConfigOptions.COMMON_BOSS_SELECTOR.get())

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
