#!/usr/bin/python3

import subprocess

# 미완성 (현재 작성 중)

def install_requirement_packages():
	requirement_packages = ['python3-distutils', 'libnotify-bin', 'libnotify-dev', 'vorbis-tools'] # 추가로 설치할 패키지(선택 사항):  $ pip install pgi, vext, vext.gi

	for rp in requirement_packages:
		return_value = subprocess.call('dpkg -l | grep %s >/dev/null'%rp, shell=True) # 해당 패키지가 시스템에 이미 설치된 경우 0을 반환함.

		if(return_value != 0):
			subprocess.check_output('sudo apt install -y %s'%rp, shell=True)
		else:
			print('%s 패키지를 설치할 수 없습니다.'%rp)


def main():
	install_requirement_packages()


main()

