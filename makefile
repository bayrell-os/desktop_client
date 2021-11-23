
all:
	@echo "make {linux|windows}"

linux:
	pyinstaller --onefile -n bayrell_os_desktop_client_1_0 ./run
	

clean:
	rm -rf dist/*
	
