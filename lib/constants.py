from lib.base import Rect, Point, Color, Rgb
from lib.logger import Logger


class _ConfigValue:
    def __init__(self, config: str):
        self.__config__ = config

    def get(self):
        return self.__config__


class ConfigSections:
    SECTION_MAIN = _ConfigValue('Main')
    SECTION_CUSTOM = _ConfigValue('Custom')
    SECTION_SETTINGS = _ConfigValue('Settings')


class ConfigOptions:
    GAMING_MODE_MAIN = _ConfigValue('GamingModeMain')
    TRACK_BELL_SWITCH = _ConfigValue('TrackBellSwitch')
    TRACK_FOLLOW_SWITCH = _ConfigValue('TrackFollowSwitch')
    ROOM_CREATOR_SWITCH = _ConfigValue('RoomCreatorSwitch')
    BELL_SELECTOR_MODE = _ConfigValue('BellSelectorMode')
    BELL_BOSS_SELECTOR_ADVANCED = _ConfigValue('BellBossSelectorAdvanced')
    FOLLOW_FRIEND_SELECT = _ConfigValue('FollowFriendSelect')
    FOLLOW_FRIEND_SELECT_NAME = _ConfigValue('FollowFriendSelectName')
    # full non-full
    ROOM_CREATOR_START_FIGHT_MODE = _ConfigValue('RoomCreatorStartFightMode')
    ROOM_CREATOR_GHOST_MODE = _ConfigValue('RoomCreatorGhostMode')
    ROOM_CREATOR_GHOST_ESCAPE_TIME = _ConfigValue('RoomCreatorGhostEscapeTime')
    RECRUITMENT_MODE = _ConfigValue('RecruitmentMode')
    ROOM_CREATOR_BOSS_SELECTOR = _ConfigValue('RoomCreatorBossSelector')
    COMMON_BOSS_SELECTOR = _ConfigValue('CommonBossSelector')
    GAME_SERVER = _ConfigValue('GameServer')
    DEVICE_ADB_SERIAL = _ConfigValue('DeviceADBSerial')
    ENABLE_TAB_LOG_SWITCH = _ConfigValue('EnableTabLogSwitch')


class ConfigValues:
    GAMING_MODE_MAIN_GUEST = _ConfigValue('room_guest')
    GAMING_MODE_MAIN_OWNER = _ConfigValue('room_owner')
    BELL_SELECTOR_MODE_COMMON = _ConfigValue('common_boss_selector')
    BELL_SELECTOR_MODE_ADVANCED = _ConfigValue('bell_boss_selector_advanced')

    COMMON_ENABLE = _ConfigValue('enable')
    COMMON_DISABLE = _ConfigValue('disable')


class Actions:
    SCREENSHOT_NOW = 'screenshot_now'


class CheckColor:
    # 底栏
    BOTTOM_BAR_ACTIVE_COLOR = Color(Rgb(255, 156, 22), Rgb(255, 162, 33))
    BOTTOM_BAR_INACTIVE_COLOR = Color(Rgb(253, 249, 249), Rgb(255, 255, 255))
    # 准备界面
    PREPARE_ACTIVE_COLOR = Color(Rgb(255, 156, 22), Rgb(255, 162, 33))


class CheckPoint:
    # 底栏
    BOTTOM_BAR_CITY_POINT = Point(101, 1260)
    BOTTOM_BAR_HOME_POINT = Point(230, 1260)
    BOTTOM_BAR_CHARACTER_POINT = Point(349, 1260)
    BOTTOM_BAR_STORE_POINT = Point(468, 1260)
    BOTTOM_BAR_PICKUP_POINT = Point(585, 1260)
    BOTTOM_BAR_MENU_POINT = Point(698, 1260)
    # 准备界面
    PREPARE_PLAYER1_STATUS = Point(45, 290)
    PREPARE_PLAYER2_STATUS = Point(270, 290)
    PREPARE_PLAYER3_STATUS = Point(508, 290)
    PREPARE_START_FIGHT = Point(250, 925)


class Template:
    def __init__(self, template_name: str, rect_dict: dict):
        self.__template_name = template_name
        self.__rect_dict = rect_dict

    def getRect(self, server_name: str):
        if server_name not in self.__rect_dict.keys():
            print('Error: There is no template \"{template_name}\" for \"{server_name}\"'
                  .format(template_name=self.__template_name, server_name=server_name))
            Logger.quit(-1)
        return self.__rect_dict[server_name]

    def getName(self):
        return self.__template_name


class CheckRect:
    # 底栏
    BOTTOM_BAR_CITY_RECT = Rect(Point(7, 1192), Point(100, 1280))
    BOTTOM_BAR_HOME_RECT = Rect(Point(131, 1192), Point(235, 1280))
    BOTTOM_BAR_CHARACTER_RECT = Rect(Point(250, 1192), Point(354, 1280))
    BOTTOM_BAR_STORE_RECT = Rect(Point(370, 1192), Point(474, 1280))
    BOTTOM_BAR_PICKUP_RECT = Rect(Point(490, 1192), Point(594, 1280))
    BOTTOM_BAR_MENU_RECT = Rect(Point(610, 1192), Point(714, 1280))
    # 主界面
    DIALOG_ANNOUNCEMENT_CLOSE_BUTTON_RECT = Rect(Point(216, 1147), Point(503, 1210))
    # 准备界面
    PREPARE_CHECKBOX_BUTTON_RECT = Rect(Point(213, 891), Point(507, 974))


class CheckTemplate:
    # 通用
    COMMON_CARD_INFO_ICON = Template(
        'Common_card_info_icon',
        {
            'cn': Rect(Point(652, 1063), Point(697, 1105)),
            'tw': Rect(Point(652, 1063), Point(697, 1105))
        }
    )
    COMMON_CHECKBOX_ACTIVE = Template(
        'Common_checkbox_active',
        {
            'cn': Rect(Point(236, 886), Point(276, 979)),
            'tw': Rect(Point(236, 886), Point(276, 979)),
        }
    )
    COMMON_CHECKBOX_INACTIVE = Template(
        'Common_checkbox_inactive',
        {
            'cn': Rect(Point(236, 886), Point(276, 979)),
            'tw': Rect(Point(236, 886), Point(276, 979)),
        }
    )
    COMMON_MULTI_PLAY_BUTTON = Template(
        'Common_multi_play_button',
        {
            # Fact: Rect(Point(343, 840), Point(603, 905))
            'cn': Rect(Point(45, 772), Point(673, 1075)),
            'tw': Rect(Point(45, 772), Point(673, 1075))
        }
    )
    COMMON_START_FIGHT_BUTTON = Template(
        'Common_start_fight_button',
        {
            'cn': Rect(Point(213, 890), Point(505, 973)),
            'tw': Rect(Point(213, 890), Point(505, 973))
        }
    )
    # 对话框
    DIALOG_SINGLE_OK = Template(
        'Dialog_single_ok',
        {
            'cn': Rect(Point(219, 795), Point(502, 856)),
            'tw': Rect(Point(219, 795), Point(502, 856))
        }
    )
    DIALOG_DOUBLE_OK = Template(
        'Dialog_double_ok',
        {
            'cn': Rect(Point(381, 795), Point(663, 856)),
            'tw': Rect(Point(381, 795), Point(663, 856))
        }
    )
    DIALOG_DOUBLE_CANCEL = Template(
        'Dialog_double_cancel',
        {
            'cn': Rect(Point(54, 795), Point(340, 856)),
            'tw': Rect(Point(54, 795), Point(340, 856))
        }
    )
    # 登录后继续任务弹窗 // 特判
    DIALOG_CONTINUE_TASK = Template(
        'Dialog_continue_task',
        {
            'cn': Rect(Point(234, 520), Point(487, 593)),
            'tw': Rect(Point(130, 476), Point(583, 676))
        }
    )
    # 日期改变弹窗
    DIALOG_DATE_CHANGED = Template(
        'Dialog_date_changed',
        {
            'cn': Rect(Point(298, 535), Point(421, 614)),
            'tw': Rect(Point(238, 535), Point(475, 614))
        }
    )
    # 房间解散弹窗
    DIALOG_ROOM_DISBAND = Template(
        'Dialog_room_disband',
        {
            'cn': Rect(Point(288, 560), Point(433, 590))
        }
    )
    # 超时房间解散弹窗
    DIALOG_ROOM_DISBAND_TIMEOUT = Template(
        'Dialog_room_disband_timeout',
        {
            'cn': Rect(Point(168, 550), Point(550, 600)),
            'tw': Rect(Point(168, 550), Point(550, 600))
        }
    )
    # 领主加成点数
    DIALOG_INCOME_BUFF = Template(
        'Dialog_income_buff',
        {
            'cn': Rect(Point(236, 502), Point(488, 580)),
            'tw': Rect(Point(220, 495), Point(498, 575))
        }
    )
    # 招募对话框标题
    DIALOG_RECRUITMENT_TITLE = Template(
        'Dialog_recruitment_title',
        {
            'cn': Rect(Point(297, 330), Point(424, 365)),
            'tw': Rect(Point(297, 330), Point(424, 365))
        }
    )
    # 招募对话框确认按钮
    DIALOG_RECRUITMENT_OK = Template(
        'Dialog_recruitment_ok',
        {
            'cn': Rect(Point(381, 891), Point(663, 954)),
            'tw': Rect(Point(381, 891), Point(663, 954))
        }
    )
    # 招募对话框取消按钮
    DIALOG_RECRUITMENT_CANCEL = Template(
        'Dialog_recruitment_cancel',
        {
            'cn': Rect(Point(54, 891), Point(340, 954)),
            'tw': Rect(Point(54, 891), Point(340, 954))
        }
    )
    # 登录界面
    LOGIN_INTERFACE_SIGN = Template(
        'Login_interface_sign',
        {
            'cn': Rect(Point(342, 835), Point(424, 908)),
            'tw': Rect(Point(342, 835), Point(424, 908))
        }
    )
    # 主界面几大按钮
    HOME_BELL_ACTIVE = Template(
        'Bell_active',
        {
            'cn': Rect(Point(21, 8), Point(74, 60)),
            'tw': Rect(Point(21, 8), Point(74, 60))
        })
    HOME_BOSS_LIST_BUTTON = Template(
        'Home_boss_list_button',
        {
            'cn': Rect(Point(529, 1072), Point(720, 1155)),
            'tw': Rect(Point(536, 1072), Point(630, 1155))
        }
    )
    BOSS_LIST_LOADING_TEXT = Template(
        'Boss_list_loading_text',
        {
            'cn': Rect(Point(305, 618), Point(458, 658)),
            'tw': Rect(Point(305, 618), Point(458, 658))
        }
    )
    BOSS_LIST_REFRESH_BUTTON = Template(
        'Boss_list_refresh_button',
        {
            'cn': Rect(Point(632, 285), Point(682, 332)),
            'tw': Rect(Point(632, 285), Point(682, 332))
        }
    )
    BOSS_LIST_REFRESH_UNAVAILABLE_BUTTON = Template(
        'Boss_list_refresh_unavailable_button',
        {
            'cn': Rect(Point(632, 285), Point(682, 332)),
            'tw': Rect(Point(632, 285), Point(682, 332))
        }
    )
    BOSS_INFO_EXCHANGE_BUTTON = Template(
        'Boss_info_exchange_button',
        {
            'cn': Rect(Point(632, 285), Point(682, 332)),
            'tw': Rect(Point(632, 285), Point(682, 332))
        }
    )
    # 铃铛相关
    BELL_DIALOG_TITLE_RECT = Template(
        'Bell_dialog_title',
        {
            'cn': Rect(Point(288, 48), Point(431, 92)),
            'tw': Rect(Point(288, 48), Point(431, 92))
        }
    )
    BELL_DIALOG_BOSS_INFO_IMG = Template(
        'Bell_dialog_boss_info_img',
        {
            'cn': Rect(Point(48, 312), Point(208, 399)),
            'tw': Rect(Point(48, 332), Point(208, 419))
        }
    )
    BELL_DIALOG_JOIN_RECT = Template(
        'Bell_dialog_join',
        {
            'cn': Rect(Point(380, 1043), Point(660, 1104)),
            'tw': Rect(Point(380, 1077), Point(660, 1140))
        }
    )
    BELL_DIALOG_DISJOIN_RECT = Template(
        'Bell_dialog_disjoin',
        {
            'cn': Rect(Point(62, 1043), Point(338, 1104)),
            'tw': Rect(Point(62, 1077), Point(338, 1140))
        }
    )
    # 招募
    RECRUITMENT_BUTTON = Template(
        'Recruitment_button',
        {
            'cn': Rect(Point(250, 800), Point(467, 861)),
            'tw': Rect(Point(250, 800), Point(467, 861))
        }
    )
    RECRUITMENT_DOUBLE_FOLLOW_CHECKBOX = Template(
        'Recruitment_double_follow_checkbox',
        {
            'cn': Rect(Point(56, 451), Point(665, 555)),
            'tw': Rect(Point(56, 451), Point(665, 555))
        }
    )
    RECRUITMENT_SINGLE_FOLLOW_CHECKBOX = Template(
        'Recruitment_single_follow_checkbox',
        {
            'cn': Rect(Point(56, 585), Point(665, 682)),
            'tw': Rect(Point(56, 585), Point(665, 682))
        }
    )
    RECRUITMENT_RANDOM_CHECKBOX = Template(
        'Recruitment_random_checkbox',
        {
            'cn': Rect(Point(56, 705), Point(665, 808)),
            'tw': Rect(Point(56, 705), Point(665, 808))
        }
    )
    # 战斗界面
    FIGHT_WAITING_FOR_OTHERS_TEXT_RECT = Template(
        'Fight_waiting_for_others',
        {
            'cn': Rect(Point(305, 618), Point(458, 658)),
            'tw': Rect(Point(305, 618), Point(458, 658))
        }
    )
    FIGHT_PAUSE_BUTTON_RECT = Template(
        'Fight_pause_button',
        {
            'cn': Rect(Point(0, 25), Point(80, 116)),
            'tw': Rect(Point(0, 25), Point(80, 116))
        }
    )
    FIGHT_PAUSE_UI_ESCAPE_BUTTON = Template(
        'Fight_pause_ui_escape_button',
        {
            'cn': Rect(Point(0, 1196), Point(155, 1264)),
            'tw': Rect(Point(0, 1196), Point(155, 1264))
        }
    )
    FIGHT_PAUSE_UI_ESCAPE_DIALOG = Template(
        'Fight_pause_ui_escape_dialog',
        {
            'cn': Rect(Point(180, 515), Point(535, 638)),
            'tw': Rect(Point(180, 495), Point(535, 658))
        }
    )
    FIGHT_REBORN_BUTTON_TEXT = Template(
        'Fight_reborn_button_text',
        {
            'cn': Rect(Point(313, 1049), Point(377, 1086)),
            'tw': Rect(Point(287, 1049), Point(395, 1086))
        }
    )
    # 结算界面
    RESULT_BOTTOM_BLANK_SPACE = Template(
        'Result_bottom_blank_space',
        {
            'cn': Rect(Point(400, 400), Point(704, 704)),
            'tw': Rect(Point(400, 400), Point(704, 704))
        }
    )
    RESULT_BOTTOM_CONTINUE_BUTTON = Template(
        'Result_bottom_continue_button',
        {
            'cn': Rect(Point(248, 1174), Point(471, 1232)),
            'tw': Rect(Point(248, 1174), Point(471, 1232))
        }
    )
    RESULT_BOTTOM_EXIT_ROOM_BUTTON = Template(
        'Result_bottom_exit_room_button',
        {
            'cn': Rect(Point(102, 1174), Point(326, 1232)),
            'tw': Rect(Point(102, 1174), Point(326, 1232))
        }
    )
    RESULT_BOTTOM_DISBAND_ROOM_BUTTON = Template(
        'Result_bottom_disband_room_button',
        {
            'cn': Rect(Point(102, 1174), Point(326, 1232)),
            'tw': Rect(Point(102, 1174), Point(326, 1232))
        }
    )
    RESULT_BOTTOM_BACK_ROOM_BUTTON = Template(
        'Result_bottom_back_room_button',
        {
            'cn': Rect(Point(393, 1174), Point(618, 1232)),
            'tw': Rect(Point(393, 1174), Point(618, 1232))
        }
    )
    RESULT_OFFLINE_EXIT_ROOM_BUTTON = Template(
        'Result_bottom_offline_exit_room_button',
        {
            'cn': None,
            'tw': Rect(Point(248, 1174), Point(471, 1232))
        }
    )


class Locate:
    BOSS_LIST_CARD_TITLE_ROOM_SUFFIX = {
        'cn': '的房间',
        'tw': '的房間'
    }


class Const:
    # Boss列表头图底部坐标Y
    BOSS_LIST_HEADER_BOTTOM_Y = 372
    # Boss列表第一张卡片底部坐标Y
    BOSS_LIST_FIRST_CARD_BOTTOM_Y = 512
    # Boss列表卡片 左边坐标 X
    BOSS_LIST_CARD_LEFT_X = 24
    # Boss列表卡片 右边坐标 X
    BOSS_LIST_CARD_RIGHT_X = 695
    # "i"图标左侧(防止点到"i"图标)
    BOSS_LIST_CARD_RIGHT_X_NO_INFO = 648
    # "i"图标到卡片顶部距离
    BOSS_LIST_CARD_INFO_MARGIN_TOP = 45
    # "i"图标到卡片底部距离
    BOSS_LIST_CARD_INFO_MARGIN_BOTTOM = 44
    # "i"图标右边的房间状态颜色图案间距
    BOSS_LIST_CARD_INFO_MARGIN_LEFT_ROOM_STATUS = 48
    # 卡片文字内容 右边坐标 X
    BOSS_LIST_CARD_TEXT_RIGHT = 540
    # 卡片文字内容 左边坐标 X
    BOSS_LIST_CARD_TEXT_LEFT = 200


class ResultCode:
    START_SUCCEED = 1
    START_FAILED = 2
    STOP_SUCCEED = 3
    STOP_FAILED = 4
    WAITING_TASK = 5


class StatusCode:
    # 正常状态
    NO_ERROR = 0
    # 刚刚Error过
    HAD_ERROR = 1
    # Error: adb连接失败
    ADB_CONNECT_FAILED = -1
    # Error: adb连接中断
    ADB_CONNECT_INTERRUPT = -2
    # Error: 设备分辨率不支持
    UNSUPPORTED_RESOLUTION = -3


class Status:
    def __init__(self, code: int, name: str):
        self.code = code
        self.name = name


class Task:
    NO_TASK = Status(0, "无任务")
    GO_BACK_TO_HOME = Status(1, "返回首页")
    GO_ROOM_AS_GUEST = Status(101, "进入房间-乘客")
    GO_ROOM_AS_OWNER = Status(102, "进入房间-房主")
    GO_ROOM_PREPARE_AS_GUEST = Status(103, "准备战斗-乘客")
    GO_ROOM_PREPARE_AS_OWNER = Status(104, "准备战斗-房主")
    GO_ROOM_WAITING_FIGHT_GUEST = Status(105, "等待战斗开始-乘客")
    GO_ROOM_WAITING_FIGHT_OWNER = Status(106, "等待战斗开始-房主")
    GO_FIGHT_AS_GUEST = Status(201, "前往战斗-乘客")
    GO_FIGHT_AS_OWNER = Status(202, "前往战斗-房主")
    GO_FIGHT = Status(203, "战斗中")
    GO_FIGHT_ESCAPE = Status(204, "退出房间(跳车/灵车)")
    GO_FIGHT_RESULT = Status(205, "战斗结束-结算")
    GO_FIGHT_END_FAST_JUMP = Status(206, "战后快速跳转")
    GO_BELL_CLICKED = Status(301, "检测到铃铛")
    GO_BELL_JOIN = Status(302, "加入铃铛")
    GO_CREATOR_GET_TARGET_BOSS_INFO = Status(401, "获取目标Boss信息")
    GO_CREATOR_CHECK_BOSS_LIST = Status(402, "寻找目标Boss")
    GO_CREATOR_CHECK_BOSS_LEVEL = Status(403, "选择目标难度")
    GO_CREATOR_CREATE_ROOM = Status(404, "创建目标Boss房间")
    GO_FOLLOW_CHECK_BOSS_LIST = Status(501, "寻找房间")
    GO_LOGIN = Status(901, "前往登录")
    GO_CONTINUE_AFTER_LOGIN = Status(902, "已登录，准备开始检测当前界面")
    GO_CHECK_INTERFACE = Status(903, "检测当前界面")
