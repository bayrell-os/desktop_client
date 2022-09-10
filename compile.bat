
rmdir /s /q dist\cloud_os_desktop_0.4.2

pyinstaller --noconsole --noconfirm -n cloud_os_desktop_0.4.2 ./run

pause

@rem pyinstaller --noconfirm -n cloud_os_desktop_0.4.2 ./run