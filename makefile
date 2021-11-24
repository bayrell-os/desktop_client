
all:
	@echo "make {bdist|compile|clean}"

compile:
	pyinstaller --onefile -n bayrell_os_desktop_client_1_2 ./run
	
bdist:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf dist/*
	
