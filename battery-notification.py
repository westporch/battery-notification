#!/usr/bin/python3

# 작성: Westporch(westporch@debianusers.or.kr)

'''
의존성 패키지
$ sudo apt install python3-distutils libnotify-bin libnotify-dev vorbis-tools
($ pip install pgi, vext, vext.gi)
'''

import subprocess
import gi
import time
import os

gi.require_version('Notify', '0.7') # https://notify2.readthedocs.io/en/latest/
from gi.repository import Notify


BAT_NAME = subprocess.check_output("ls /sys/class/power_supply | grep BAT", shell=True).decode("utf-8").rstrip()    # 예) BAT1
BAT_INFO_FILE = "/sys/class/power_supply/%s"%BAT_NAME + '/uevent'

BAT_STATUS = subprocess.check_output("cat %s"%BAT_INFO_FILE + ' | grep POWER_SUPPLY_STATUS | cut -d \'=\' -f 2', shell=True).decode("utf-8").rstrip()    # 'Charging' 또는 'Discharging'
CHARGE_FULL_DESIGN = int(subprocess.check_output("cat %s"%BAT_INFO_FILE + ' | grep POWER_SUPPLY_CHARGE_FULL_DESIGN | cut -d \'=\' -f 2', shell=True).decode("utf-8").rstrip())
CHARGE_FULL = int(subprocess.check_output("cat %s"%BAT_INFO_FILE + ' | grep POWER_SUPPLY_CHARGE_FULL | tail -n 1 | cut -d \'=\' -f 2', shell=True).decode("utf-8").rstrip())
CHARGE_NOW = int(subprocess.check_output("cat %s"%BAT_INFO_FILE + ' | grep POWER_SUPPLY_CHARGE_NOW | cut -d \'=\' -f 2', shell=True).decode("utf-8").rstrip())
REMAINING_BAT_PERCENT = round((CHARGE_NOW / CHARGE_FULL) * 100)

WARNING_BAT_PERCENT = 20 
ALERTING_BAT_PERCENT = 10   


def get_battery_max_charge_percent():
    bat_max_charge_percent = round((CHARGE_FULL / CHARGE_FULL_DESIGN) * 100)

    if bat_max_charge_percent >= 80 and bat_max_charge_percent < 90:
        bat_max_charge_percent = 80     # 배터리 수명 연장 모드(배터리 충전을 80%로 제한한 경우)
        return bat_max_charge_percent
    elif bat_max_charge_percent >= 70 and bat_max_charge_percent < 80:
        bat_max_charge_percent = 60     # 배터리 수명 연장 모드(배터리 충전을 60%로 제한한 경우)
        return bat_max_charge_percent
    else:
        bat_max_charge_percent = 100    # '배터리 수명 연장 모드'를 사용하지 않는 경우
        return bat_max_charge_percent


# 사운드 파일: StartLabsTheme(https://www.gnome-look.org/p/1291372/)
def play_sound():
    if REMAINING_BAT_PERCENT == get_battery_max_charge_percent():
        os.system('/usr/bin/ogg123 --device pulse --quiet /opt/battery-notification/complete.ogg')
    else:
        os.system('/usr/bin/ogg123 --device pulse --quiet /opt/battery-notification/battery-low.ogg')

'''
def draw_battery(occupied_space):
	battery_charge_full_size = int(occupied_space / 10) 
	charged_space = battery_charge_full_size * '■ '
	uncharged_space = (10 - battery_charge_full_size) * '□ '
	draw_battery = charged_space + uncharged_space
	
	return draw_battery		#  예) ■ ■ ■ ■ ■ ■ ■ ■ □ □
'''


def draw_battery(occupied_space):
	occupied_space = int(occupied_space / 10) 
	charged_space = occupied_space * '■ '
	uncharged_space = (10 - occupied_space) * '□ '
	draw_battery = charged_space + uncharged_space
	
	return draw_battery		#  예) ■ ■ ■ ■ ■ ■ ■ ■ □ □


def warn_battery_low():
    Notify.init("배터리의 전원이 부족합니다.")
    notification = Notify.Notification.new("배터리의 전원이 부족합니다.", "배터리를 충전해 주십시오.\n %s(%s%%)"%(draw_battery(REMAINING_BAT_PERCENT), REMAINING_BAT_PERCENT))
    notification.set_urgency(2) # URGENCY_CRITICAL
    notification.set_timeout(15000)
    notification.show()
    play_sound()


def alert_battery_low():
    Notify.init("배터리의 전원이 매우 부족합니다.")
    notification = Notify.Notification.new("배터리의 전원이 매우 부족합니다.", "전원이 매우 부족하여 잠시 후 절전모드로 전환합니다.\n %s(%s%%)"%(draw_battery(REMAINING_BAT_PERCENT), REMAINING_BAT_PERCENT))
    play_sound()
    time.sleep(10)
    os.system('systemctl suspend')   


def battery_full():
    Notify.init("배터리 충전 완료")
    notification = Notify.Notification.new("배터리 충전 완료", "배터리 충전을 완료했습니다.\n  %s(%s%%)"%(draw_battery(get_battery_max_charge_percent()), get_battery_max_charge_percent()))
    notification.set_urgency(1) # URGENCY_NORMAL
    notification.show()
    play_sound()


def main():
    if REMAINING_BAT_PERCENT <= 20 and BAT_STATUS == "Discharging":
        warn_battery_low()
    elif REMAINING_BAT_PERCENT <= 10 and BAT_STATUS == "Discharging":
        alert_battery_low()
    elif REMAINING_BAT_PERCENT == get_battery_max_charge_percent():
        battery_full()


main()
