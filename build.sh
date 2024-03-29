#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPT_PATH=`dirname $SCRIPT`
BASE_PATH=`dirname $SCRIPT_PATH`
version="0.4.2.post3"

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
		pyinstaller --onefile -n cloud_os_desktop_$version ./run
	;;
	
	build)
		. env/bin/activate
		python3.8 setup.py sdist bdist_wheel
	;;
	
	install)
		. env/bin/activate
		python3.8 setup.py sdist bdist_wheel
		echo "Install. Need root password"
		sudo pip3.8 install dist/cloud_os_desktop-$version.tar.gz
	;;
	
	uninstall)
		echo "Uninstall. Need root password"
		sudo pip3.8 uninstall cloud_os_desktop
	;;
	
	install-dev)
		python3.8 setup.py develop
	;;
	
	uninstall-dev)
		python3.8 setup.py develop -u
	;;
	
	upload)
		twine check dist/cloud_os_desktop-$version.tar.gz
		twine check dist/cloud_os_desktop-$version-py3-none-any.whl
		twine upload -r pypi dist/cloud_os_desktop-$version.tar.gz
		twine upload -r pypi dist/cloud_os_desktop-$version-py3-none-any.whl
	;;
	
	clean)
		rm -rf dist/*
	;;
	
	ui)
		pushd cloud_os_desktop
		pyuic5 AboutDialog.ui -o AboutDialog.py
		pyuic5 MainWindow.ui -o MainWindow.py
		pyuic5 ConnectDialog.ui -o ConnectDialog.py
		pyuic5 EditConnectionDialog.ui -o EditConnectionDialog.py
		pyuic5 WebBrowser.ui -o WebBrowser.py
		popd
	;;
	
	*)
		echo "Usage: $0 {build|compile|ui|clean|install|install-dev|uninstall|uninstall-dev|upload|create-env|pip-freeze|pip-install-online|pip-install-offline|pip-save}"
		RETVAL=1

esac

exit $RETVAL