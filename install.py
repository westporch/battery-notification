#!/usr/bin/python3

import subprocess
import os

# 미완성 (현재 작성 중)

'''
작업할 내용
- dunst를 설정하는 함수를 추가하기
- install.py만 다운받아서, git clone으로 패키지를 설치하도록 하기?
'''

CRONTAB_FILE = "/etc/cron.d/battery-notification"
USER_HOME_DIR = subprocess.check_output('echo $HOME', shell=True).decode('utf-8').rstrip()
DUNST_DIR = USER_HOME_DIR + '/.config/dunst'


def install_requirement_packages():
	requirement_packages = ['python3-distutils', 'libnotify-bin', 'libnotify-dev', 'vorbis-tools', 'dunst'] # 추가로 설치할 패키지(선택 사항):  $ pip install pgi, vext, vext.gi

	for rp in requirement_packages:
		return_value = subprocess.call('dpkg -l | grep %s >/dev/null'%rp, shell=True) # 해당 패키지가 시스템에 이미 설치된 경우 0을 반환함.

		if(return_value != 0):
			subprocess.check_output('sudo apt install -y %s'%rp, shell=True)
		else:
			print('%s 패키지를 설치할 수 없습니다.'%rp)


def add_crontab():
    return_value = os.path.isfile('%s'%CRONTAB_FILE)

    if(return_value):
        pass
    else:
        subprocess.check_output('sudo cp battery-notification /etc/cron.d/battery-notification', shell=True)


def set_dunst():
    dir_return_value = os.path.exists('%s'%DUNST_DIR)    # dunst의 디렉터리가 존재하면, True를 반환함.
    file_return_value = os.path.isfile('%s'%DUNST_DIR + '/dunstrc')

    if(dir_return_value == False):
        print('%s'%DUNST_DIR + ' 디렉터리를 생성하였습니다.')
        subprocess.check_output('mkdir %s'%DUNST_DIR, shell=True)
    else:
        pass


    if(file_return_value == False):
        subprocess.check_output('wget https://raw.githubusercontent.com/westporch/dotfiles/master/dunst/dunstrc -P %s'%DUNST_DIR, shell=True)
    else:
        pass


def main():
    install_requirement_packages()
    add_crontab()
    set_dunst()


main()

