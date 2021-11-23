
all:
	@echo "make {linux|windows}"

linux:
	pyinstaller --onefile -n bayrell_os_desktop_client ./run
	

windows:
	pyinstaller --onefile -n bayrell_os_desktop_client ./run
	
	
clean:
	rm -rf dist/*
	
