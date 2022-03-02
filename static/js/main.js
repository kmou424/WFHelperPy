var bell_boss_selector_advanced_dialog = new mdui.Dialog(
  $('#bell_boss_selector_advanced')
);

class Log {
  static #DEBUG = true;
  static o(obj) {
    if (this.#DEBUG) {
      console.log('[Exec] ' + obj);
    }
  }
}

class BossInfo {
  static BOSS_LEVEL_NAME_TABLE = {
    'prim': '初级',
    'mid': '中级',
    'high': '高级',
    'highp': '高级+',
    'super': '超级',
  };
  constructor(item) {
    this.item = item;
  }
  getName() {
    return this.item['name'];
  }
  getId() {
    return this.item['id'];
  }
  getType() {
    return this.item['type'];
  }
  getEndTime() {
    return this.item['end'];
  }
  getLevels() {
    return this.item['levels'].split(' ');
  }
  getOriginalLevels() {
    return this.item['levels'];
  }
}

class CheckBoxCommon {
  static isChecked(obj) {
    return obj.prop('checked');
  }
  static check(obj) {
    obj.prop('checked', true);
  }
  static uncheck(obj) {
    obj.prop('checked', false);
  }
  static updateCheck(obj, is_checked) {
    obj.prop('checked', is_checked);
  }
}

class EditText {
  static update(obj, text) {
    obj.val(text);
  }
}

class DialogManager {
  // 铃铛Boss高级筛选器
  static showBellSelectorAdvanced(is_save) {
    if (is_save == null) return;
    bell_boss_selector_advanced_dialog.toggle();
    if (!is_save) {
      EditText.update($('#bell_boss_selector_advanced_edittext'), '');
    }
  }
  static appendBossInfoHelper(obj, boss_info) {
    obj.html(
      obj.html() +
        '<tr>' +
        '<th>' +
        boss_info.getName() +
        '</th>' +
        '<td>' +
        boss_info.getId() +
        '</td>' +
        '</tr>'
    );
  }
}

class ServerStatus {
  constructor(is_running) {
    this.running = is_running;
  }
  updateRunning(is_running) {
    this.running = is_running;
  }
  getRunning() {
    if (this.running == null) {
      return false;
    }
    return this.running;
  }

  static checkResult(server_result) {
    switch (server_result) {
      case 1:
        Utils.showSnackbar('开始运行', 500, 'left-top');
        break;
      case 2:
        Utils.showSnackbar('启动失败', 500, 'left-top');
        break;
      case 3:
        Utils.showSnackbar('已停止', 500, 'left-top');
        break;
      case 4:
        Utils.showSnackbar('停止失败', 500, 'left-top');
        break;
      case 5:
        Utils.showSnackbar(
          '已向服务端提交停止请求, 等待当前任务完成后停止',
          4000,
          'left-top'
        );
        break;
    }
  }

  static checkStatus(server_status) {
    // 传回状态小于0时(即异常状态), 就把运行按钮改为红色叹号以警示用户
    if (server_status < 0 || server_status == 1) {
      $('#toolbar_run_btn').find('i').text('info_outline');
      $('#toolbar_run_btn').find('i').addClass('mdui-text-color-red');
    }
    switch (server_status) {
      case -1:
        Utils.showSnackbar('设备连接失败', 1000, 'left-top');
        break;
      case -2:
        Utils.showSnackbar('ADB 出现异常, 任务自动终止', 1000, 'left-top');
        break;
      case -3:
        Utils.showSnackbar('不支持的设备分辨率', 1000, 'left-top');
        break;
    }
  }
}

var server_status = new ServerStatus(null);

class Utils {
  static showSnackbar(str, sTimeout, mPosition) {
    mdui.snackbar({
      message: str,
      position: mPosition,
      timeout: sTimeout,
    });
  }
}

class KRequest {
  static post(act, data, func) {
    $.ajax({
      type: 'POST',
      dataType: 'json',
      url: act,
      data: data,
      success: function (result) {
        if (func != null) {
          func(result);
        }
      },
      error: function () {},
    });
  }
  static updatePage(act, data) {
    Log.o('UpdatePage');
    this.post(act, data, Updater.run);
  }
}

class ChipRadioGroup {
  static custom_click_chip_value = ['bell_boss_selector_advanced'];
  static custom_click_chip_check_fun = [DialogManager.showBellSelectorAdvanced];
  static custom_click_chip_check_fun_arg = [true];
  static RADIO_CHIP_TEMPLATE =
    '<div\
        class="radio-chip mdui-chip mdui-shadow-0"\
        value="##VALUE##"\
        levels="##LEVELS##"\
        ischecked="false"\
        style="margin-right: 4px"\
     >\
        <span class="mdui-chip-icon">\
          <i class="mdui-icon material-icons">radio_button_unchecked</i>\
        </span>\
        <span class="mdui-chip-title">##NAME##</span>\
     </div>';
  static addBoss(obj, level_obj, boss) {
    // 目前暂不支持活动Boss
    if (boss.getType() == 'special') return;
    var radio_chip = $(
      ChipRadioGroup.RADIO_CHIP_TEMPLATE.replace('##VALUE##', boss.getId())
        .replace('##LEVELS##', boss.getOriginalLevels())
        .replace('##NAME##', boss.getName())
    );
    obj.find('div.radio-group').append(radio_chip);
    ChipRadioGroup.findChipByValue(obj, boss.getId()).click(function () {
      if (!server_status.getRunning()) {
        ChipRadioGroup.addLevels(level_obj, $(this).attr('levels'));
        ChipRadioGroup.initRadio(level_obj, undefined);
        ChipRadioGroup.bindClick();
      }
    });
  }
  static addLevels(obj, levels) {
    var root = obj.find('div.radio-group');
    root.empty();
    levels = levels.split(' ');
    for (var i = 0; i < levels.length; ++i) {
      var radio_chip = $(
        ChipRadioGroup.RADIO_CHIP_TEMPLATE.replace('##VALUE##', levels[i])
          .replace('##LEVELS##', 'null')
          .replace('##NAME##', BossInfo.BOSS_LEVEL_NAME_TABLE[levels[i]])
      );
      root.append(radio_chip);
    }
  }
  static initRadio(obj, value) {
    var target = 0;
    obj
      .find('div.radio-group')
      .children('div.radio-chip')
      .each(function () {
        if ($(this).attr('value') == value) target = $(this);
        ChipRadioGroup.uncheck($(this));
      });
    if (target == 0) {
      ChipRadioGroup.check(obj.find('div.radio-chip').first());
    } else {
      ChipRadioGroup.check(target);
    }
  }
  static getChecked(obj) {
    var ret = 0;
    obj
      .find('div.radio-group')
      .children('div.radio-chip')
      .each(function () {
        if ($(this).attr('ischecked') == 'true') {
          ret = $(this).attr('value');
        }
      });
    return ret;
  }
  static findChipByValue(obj, value) {
    var ret = value;
    obj
      .find('div.radio-group')
      .children('div.radio-chip')
      .each(function () {
        if ($(this).attr('value') == value) {
          ret = $(this);
        }
      });
    return ret;
  }
  static bindClick() {
    $('.radio-chip').click(function () {
      if (!server_status.getRunning()) {
        $(this)
          .parent()
          .children('div.radio-chip')
          .each(function () {
            var uncheck_ret = ChipRadioGroup.uncheck($(this));
          });
        ChipRadioGroup.check($(this));
      }
    });
  }
  static bindCustomClick() {
    $('.radio-chip').click(function () {
      if (!server_status.getRunning()) {
        // 判断本次check操作是不是需要执行check函数的Chip
        if (
          ChipRadioGroup.custom_click_chip_value.includes($(this).attr('value'))
        ) {
          var idx = ChipRadioGroup.custom_click_chip_value.indexOf(
            $(this).attr('value')
          );
          if (ChipRadioGroup.custom_click_chip_check_fun[idx] != null) {
            ChipRadioGroup.custom_click_chip_check_fun[idx](
              ChipRadioGroup.custom_click_chip_check_fun_arg[idx]
            );
          }
        }
      }
    });
  }
  static checkAll(obj) {
    obj
      .find('div.radio-group')
      .children('div.radio-chip')
      .each(function () {
        ChipRadioGroup.check($(this));
      });
  }
  static uncheckAll(obj) {
    obj
      .find('div.radio-group')
      .children('div.radio-chip')
      .each(function () {
        ChipRadioGroup.uncheck($(this));
      });
  }
  static check(obj) {
    var ret = true;
    if (obj.hasClass('mdui-color-grey-300'))
      obj.removeClass('mdui-color-grey-300');
    obj.addClass('mdui-color-pink-400');
    if (obj.find('span.mdui-chip-icon').hasClass('mdui-color-grey-400'))
      obj.find('span.mdui-chip-icon').removeClass('mdui-color-grey-400');
    obj.find('span.mdui-chip-icon').addClass('mdui-color-pink-400');
    obj.find('span.mdui-chip-icon').find('i').text('check_circle');
    if (obj.attr('ischecked') == 'true') {
      ret = false;
    }
    obj.attr('ischecked', 'true');
    return ret;
  }
  static uncheck(obj) {
    var ret = true;
    if (obj.hasClass('mdui-color-pink-400'))
      obj.removeClass('mdui-color-pink-400');
    obj.addClass('mdui-color-grey-300');
    if (obj.find('span.mdui-chip-icon').hasClass('mdui-color-pink-400'))
      obj.find('span.mdui-chip-icon').removeClass('mdui-color-pink-400');
    obj.find('span.mdui-chip-icon').addClass('mdui-color-grey-400');
    obj.find('span.mdui-chip-icon').find('i').text('radio_button_unchecked');
    if (obj.attr('ischecked') == 'false') {
      ret = false;
    }
    obj.attr('ischecked', 'false');
    return ret;
  }
}

class OutlineCollapseCard {
  static ROOT_TEMPLATE =
    '<div class="mdui-collapse-item outline-collapse-card mdui-ripple">\
        <div class="mdui-collapse-item-header outline-collapse-card-header">\
            <label value=""></label>\
            <div class="outline-collapse-card-header-arrow mdui-collapse-item-arrow">\
                <i class="mdui-icon material-icons">keyboard_arrow_down</i>\
            </div>\
        </div>\
        <div class="mdui-collapse-item-body">\
            <div class="mdui-row-md-5 outline-collapse-card-body">\
            </div>\
            <a>##TEMPLATE1##</a>\
        </div>\
    </div>';
  static CHECKBOX_ROOT_TEMPLATE =
    '<div class="mdui-col">\
        <label class="mdui-checkbox">\
            <input type="checkbox" value=""/>\
            <i class="mdui-checkbox-icon"></i>\
            ##TEMPLATE2##\
        </label>\
     </div>';
  static addBoss(container, boss) {
    var end_time = '长期有效';
    var name_prefix = '';
    if (boss.getType() == 'special') {
      end_time = boss.getEndTime();
      name_prefix = '<b style="color: red">[活动]</b>';
    }
    var root = $(
      this.ROOT_TEMPLATE.replace(
        '##TEMPLATE1##',
        '将结束于 <b>' + end_time + '</b>'
      )
    );
    root
      .find('div.outline-collapse-card-header label')
      .html(name_prefix + boss.getName());
    root
      .find('div.outline-collapse-card-header label')
      .attr('value', boss.getId());
    var row_root = root.find(
      'div.mdui-collapse-item-body div.outline-collapse-card-body'
    );
    var levels = boss.getLevels();
    for (var i = 0; i < levels.length; ++i) {
      var checkbox_root = $(
        this.CHECKBOX_ROOT_TEMPLATE.replace(
          '##TEMPLATE2##',
          BossInfo.BOSS_LEVEL_NAME_TABLE[levels[i]]
        )
      );
      checkbox_root.find('label input').attr('value', levels[i]);
      row_root.append(checkbox_root);
    }
    container.append(root);
  }
  static getCheckedAsStrList(container) {
    Log.o('getCheckedAsStrList');
    var res = '';
    container.children('div.outline-collapse-card').each(function () {
      var temp =
        $(this).find('div.outline-collapse-card-header label').attr('value') +
        '_';
      $(this)
        .find('div.mdui-collapse-item-body div.outline-collapse-card-body')
        .children('div.mdui-col')
        .each(function () {
          var checkbox = $(this).find('label input');
          if (CheckBoxCommon.isChecked(checkbox))
            res += temp + checkbox.attr('value') + ',';
        });
    });
    if (res.length > 0) {
      if (res.charAt(res.length - 1) == ',') {
        res = res.substring(0, res.length - 1);
      }
    }
    return res;
  }
}

class SwitchPreference {
  static bindClick() {
    Log.o('SwitchPreferenceClick');
    $('.switch-preference').click(function () {
      if (!server_status.getRunning()) {
        var switch_widget = $(this).find('label').find('input');
        switch_widget.prop('checked', !switch_widget.prop('checked'));
      }
    });
  }
  static update(obj, is_checked) {
    obj.prop('checked', is_checked);
  }
}

class UIManager {
  static bindRunButtonClick() {
    Log.o('RunButtonClickListener');
    $('#toolbar_run_btn').click(function () {
      if (server_status.getRunning()) {
        KRequest.updatePage('/stopService', null);
      } else {
        UIManager.updateRunButton(false, 1);
        mdui.dialog({
          title: '确认',
          content: '要开始运行吗?',
          buttons: [
            {
              text: '取消',
            },
            {
              text: '开始运行',
              onClick: function () {
                KRequest.updatePage('/runService', null);
              },
            },
          ],
        });
      }
    });
  }
  static bindSaveButtonClick() {
    Log.o('SaveButtonClickListener');
    $('#toolbar_save_btn').click(function () {
      if (!server_status.getRunning()) {
        var mData = {
          'GamingModeMain': ChipRadioGroup.getChecked($('#gaming_mode_main')),
          'TrackBellSwitch': $('#track_bell_switch').prop('checked'),
          'TrackBossListSwitch': $('#track_boss_list_switch').prop('checked'),
          'RoomCreatorSwitch': $('#room_creator_switch').prop('checked'),
          'BellSelectorMode': ChipRadioGroup.getChecked(
            $('#bell_selector_mode')
          ),
          'BellBossSelectorAdvanced': $(
            '#bell_boss_selector_advanced_edittext'
          ).val(),
          'RoomCreatorGhostMode': ChipRadioGroup.getChecked(
            $('#room_creator_ghost_mode')
          ),
          'RoomCreatorGhostEscapeTime': $(
            '#room_creator_ghost_escape_time'
          ).val(),
          'RoomCreatorBossSelector':
            ChipRadioGroup.getChecked($('#room_creator_boss')) +
            '_' +
            ChipRadioGroup.getChecked($('#room_creator_boss_level')),
          'RecruitmentMode':
            CheckBoxCommon.isChecked($('#double_follow_chekbox')) +
            '_' +
            CheckBoxCommon.isChecked($('#single_follow_chekbox')) +
            '_' +
            CheckBoxCommon.isChecked($('#random_chekbox')),
          'CommonBossSelector': OutlineCollapseCard.getCheckedAsStrList(
            $('#common_boss_selector')
          ),
          'DeviceADBSerial': $('#device_adb_serial').val(),
          'GameServer': ChipRadioGroup.getChecked($('#server_selector')),
          'EnableTabLogSwitch': $('#enable_tab_log_switch').prop('checked'),
        };
        KRequest.updatePage('/saveAllData', mData);
        Utils.showSnackbar('已保存', 500, 'left-top');
      }
    });
  }
  static initBossInfo(result) {
    Log.o('initBossInfo');
    // Clean up
    $('#common_boss_selector').empty();
    $('#room_creator_boss').find('div.radio-group').empty();
    $('#room_creator_boss_level').find('div.radio-group').empty();
    for (var i = 0; i < result.length; ++i) {
      var boss = new BossInfo(result[i]);
      OutlineCollapseCard.addBoss($('#common_boss_selector'), boss);
      ChipRadioGroup.addBoss(
        $('#room_creator_boss'),
        $('#room_creator_boss_level'),
        boss
      );
      DialogManager.appendBossInfoHelper(
        $('#bell_boss_selector_advanced_boss_name_id_table'),
        boss
      );
    }
    Action.sendAction(Action.ACTION_GET_SELECTED_BOSS);
    ChipRadioGroup.bindClick();
  }
  static updateBossInfo(result) {
    Log.o('updateBossInfo');
    $('#common_boss_selector')
      .children('div.outline-collapse-card')
      .each(function () {
        var boss_name =
          $(this).find('div.outline-collapse-card-header label').attr('value') +
          '_';
        $(this)
          .find('div.mdui-collapse-item-body div.outline-collapse-card-body')
          .children('div.mdui-col')
          .each(function () {
            var checkbox = $(this).find('label input');
            if (
              result['CommonBossSelector'].includes(
                boss_name + checkbox.attr('value')
              )
            ) {
              CheckBoxCommon.check(checkbox);
            } else {
              CheckBoxCommon.uncheck(checkbox);
            }
          });
      });
    // 房主选项 初始化
    // 0: Boss ID, 1: Boss Level
    var room_creator_boss_selector =
      result['RoomCreatorBossSelector'].split('_');

    ChipRadioGroup.initRadio(
      $('#room_creator_boss'),
      room_creator_boss_selector[0]
    );
    ChipRadioGroup.addLevels(
      $('#room_creator_boss_level'),
      $(
        ChipRadioGroup.findChipByValue(
          $('#room_creator_boss'),
          ChipRadioGroup.getChecked($('#room_creator_boss'))
        )
      ).attr('levels')
    );
    ChipRadioGroup.initRadio(
      $('#room_creator_boss_level'),
      room_creator_boss_selector[1]
    );
    ChipRadioGroup.bindClick();
  }
  static updateEnabled(is_running) {
    var enableWidgetList = [
      '#toolbar_save_btn',
      '.mdui-switch input',
      '.mdui-checkbox input',
      '.mdui-textfield-input',
    ];
    for (var i = 0; i < enableWidgetList.length; ++i) {
      $(enableWidgetList[i]).attr('disabled', is_running);
    }
  }

  static updateRunButton(is_running, status) {
    // 传回状态是正常(0)时，才更新运行按钮状态为运行/停止
    if (status != 0) return;
    if (is_running) {
      $('#toolbar_run_btn').find('i').text('stop');
      $('#toolbar_run_btn').find('i').addClass('mdui-text-color-red');
    } else {
      $('#toolbar_run_btn').find('i').text('play_arrow');
      $('#toolbar_run_btn').find('i').removeClass('mdui-text-color-red');
    }
  }

  static updateTab(result) {
    $('#tab_log').attr('disabled', !result['EnableTabLogSwitch']);
  }
}

class Updater {
  static run(result) {
    // 主要运行模式
    ChipRadioGroup.initRadio($('#gaming_mode_main'), result['GamingModeMain']);

    // 铃铛开关
    SwitchPreference.update($('#track_bell_switch'), result['TrackBellSwitch']);

    // 关注列表进房开关
    SwitchPreference.update(
      $('#track_boss_list_switch'),
      result['TrackBossListSwitch']
    );

    // 开车开关
    SwitchPreference.update(
      $('#room_creator_switch'),
      result['RoomCreatorSwitch']
    );

    // 铃铛模式
    ChipRadioGroup.initRadio(
      $('#bell_selector_mode'),
      result['BellSelectorMode']
    );

    // 铃铛高级筛选器文本框
    EditText.update(
      $('#bell_boss_selector_advanced_edittext'),
      result['BellBossSelectorAdvanced']
    );

    // 灵车开关
    ChipRadioGroup.initRadio(
      $('#room_creator_ghost_mode'),
      result['RoomCreatorGhostMode']
    );

    // 灵车 - 跳车时间
    EditText.update(
      $('#room_creator_ghost_escape_time'),
      result['RoomCreatorGhostEscapeTime']
    );

    // 招募模式
    var recruitment_mode = result['RecruitmentMode'];
    if (recruitment_mode != '' && recruitment_mode != undefined) {
      recruitment_mode = recruitment_mode.split('_');
      CheckBoxCommon.updateCheck(
        $('#double_follow_chekbox'),
        recruitment_mode[0] == 'true'
      );
      CheckBoxCommon.updateCheck(
        $('#single_follow_chekbox'),
        recruitment_mode[1] == 'true'
      );
      CheckBoxCommon.updateCheck(
        $('#random_chekbox'),
        recruitment_mode[2] == 'true'
      );
    }

    // 设备serial文本框
    EditText.update($('#device_adb_serial'), result['DeviceADBSerial']);

    // 区服
    ChipRadioGroup.initRadio($('#server_selector'), result['GameServer']);

    // 判断区服修改(刷新对应服务器的内容)
    if (result['RegionChanged']) {
      Log.o('GameServer Changed');
      Action.sendAction(Action.ACTION_GET_BOSS_INFO_JSON);
    } else {
      Action.sendAction(Action.ACTION_GET_SELECTED_BOSS);
    }

    // 测试功能按钮
    SwitchPreference.update(
      $('#enable_tab_log_switch'),
      result['EnableTabLogSwitch']
    );
    UIManager.updateTab(result);
    Action.sendAction(Action.ACTION_REFRESH_STATE);
  }

  static refreshState(result) {
    server_status.updateRunning(result['Running']);
    ServerStatus.checkResult(result['Result']);
    ServerStatus.checkStatus(result['Status']);
    UIManager.updateEnabled(server_status.getRunning());
    UIManager.updateRunButton(server_status.getRunning(), result['Status']);
  }
}

class Action {
  static ACTION_REFRESH_STATE = 0;
  static ACTION_TAKESCREENSHOT_FOR_NOW = 1;
  static ACTION_GET_BOSS_INFO_JSON = 2;
  static ACTION_GET_SELECTED_BOSS = 3;
  static #ACTION_STRING = [
    'refreshState',
    'takeScreenshotForNow',
    'getBossInfoJson',
    'getStoredBossInfoJson',
  ];
  static #ACTION_FUNC = [
    Updater.refreshState,
    null,
    UIManager.initBossInfo,
    UIManager.updateBossInfo,
  ];
  static sendAction(action_id) {
    if (action_id >= 0 && action_id < Action.#ACTION_STRING.length) {
      KRequest.post(
        '/action',
        {
          'what': Action.#ACTION_STRING[action_id],
        },
        Action.#ACTION_FUNC[action_id]
      );
      Log.o('Send Action ' + Action.#ACTION_STRING[action_id] + ' succeed');
    }
  }
}

Action.sendAction(Action.ACTION_GET_BOSS_INFO_JSON);
UIManager.bindRunButtonClick();
UIManager.bindSaveButtonClick();
SwitchPreference.bindClick();
ChipRadioGroup.bindClick();
ChipRadioGroup.bindCustomClick();
KRequest.updatePage('/', null);

mdui.mutation();

self.setInterval(Action.sendAction, 2000, Action.ACTION_REFRESH_STATE);
