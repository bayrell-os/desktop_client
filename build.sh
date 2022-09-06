#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPT_PATH=`dirname $SCRIPT`
BASE_PATH=`dirname $SCRIPT_PATH`


case "$1" in
	
	create-env)	
		python3.8 -m venv ./env
		. env/bin/activate
		python3.8 get-pip.py
	;;
	
	pip-freeze)
		. env/bin/activate
		pip freeze > ./requirements.txt
	;;
	
	pip-install-online)
		. env/bin/activate
		pip install wheel
		pip install altgraph bcrypt cffi cryptography importlib-metadata packaging paramiko pycparser pyinstaller pyinstaller-hooks-contrib PyNaCl pyparsing PyQt5 PyQt5-Qt5 PyQt5-sip PyQtWebEngine PyQtWebEngine-Qt5 six sshtunnel toml typing_extensions zipp
	;;
	
	pip-install-offline)
		. env/bin/activate
		pip install -r ./requirements.txt --find-links=./packages --no-index
	;;
	
	pip-save)
		. env/bin/activate
		pip download -r ./requirements.txt -d ./packages
	;;
	
	compile)
		. env/bin/activate
		pyinstaller --onefile -n cloud_os_desktop_1_2 ./run
	;;
	
	build)
		. env/bin/activate
		python3.8 setup.py sdist bdist_wheel
	;;
	
	install)
		pip3.8 install dist/cloud_os_desktop-1.2.0.tar.gz
	;;
	
	uninstall)
		pip3.8 uninstall cloud_os_desktop
	;;
	
	install-dev)
		python3.8 setup.py develop
	;;
	
	uninstall-dev)
		python3.8 setup.py develop -u
	;;
	
	upload)
		twine upload -r pypi dist/*
	;;
	
	clean)
		rm -rf dist/*
	;;
	
	*)
		echo "Usage: $0 {compile|build|clean|install|install-dev|uninstall|uninstall-dev|upload|create-env|pip-freeze|pip-install-online|pip-install-offline|pip-save}"
		RETVAL=1

esac

exit $RETVAL