# -*- coding: utf-8 -*-

import asyncio, sys, os, json, threading, time
from os.path import abspath, dirname, join
from threading import Timer
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder

from .MainWindow import Ui_MainWindow
from .ConnectDialog import Ui_ConnectDialog
from .EditConnectionDialog import Ui_EditConnectionDialog
from .WebBrowser import Ui_WebBrowser

import PyQt5
from PyQt5.QtWidgets import \
	QApplication, QMainWindow, QSystemTrayIcon, QMenu, \
	QAction, QWidget, QStyle, QDialog, QMessageBox, \
	QListWidgetItem, QToolBar, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

main_window = None

class Connection():
	
	def __init__(self):
		self.connection_name = "";
		self.host = "";
		self.port = "";
		self.username = "";
		self.password = "";


class ConnectDialog(QDialog, Ui_ConnectDialog):
	
	def __init__(self, web_browser):
		QDialog.__init__(self)
		self.setupUi(self)
		self.setWindowTitle("Connect to server")
		
		self.status_connection = 0
		self.web_browser = web_browser
		
		
		
		self.ssh_server = None
	
	
			
	
	

class EditConnectionDialog(QDialog, Ui_EditConnectionDialog):
	
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		self.setWindowTitle("Edit connection")



class WebBrowser(QMainWindow, Ui_WebBrowser):
	
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		
		self.home_url = ""
		self.connect_data = None
		self.connect_dialog = None
		self.ssh_server = None
		self.thread_connect = None
		
		self.setupUi(self)
		self.setWindowTitle("Connect to server")
		self.setCentralWidget(self.webBrowser)
		
		# Tool Bar
		self.toolBar = QToolBar()
		self.addToolBar(self.toolBar)
		
		# Buttons
		self.prevButton = QAction('Prev', self)
		self.nextButton = QAction('Next', self)
		self.refreshButton = QAction('Refresh', self)
		self.homeButton = QAction('Home', self)
		self.urlEdit = QLineEdit()
		
		# Add to toolbar
		self.toolBar.addAction(self.prevButton)
		self.toolBar.addAction(self.nextButton)
		self.toolBar.addAction(self.refreshButton)
		#self.toolBar.addAction(self.homeButton)
		self.toolBar.addWidget(self.urlEdit)
		
		# Events
		self.prevButton.triggered.connect(self.onPrevButtonClick)
		self.nextButton.triggered.connect(self.onNextButtonClick)
		self.refreshButton.triggered.connect(self.onRefreshButtonClick)
		self.homeButton.triggered.connect(self.onHomeButtonClick)
		self.urlEdit.returnPressed.connect(self.onUrlEditChange)
		self.webBrowser.urlChanged.connect(self.onWebBrowserUrlChange)
		
		# Maximize
		self.showMaximized()
	
	
	def sshConnect(self):
		
		time.sleep(5)
		
		self.connect_dialog.accept()
		return
		
		if self.connect_data == None:
			self.connect_dialog.label.setText("Error: Connection data is None")
			return
		
		# Connect to ssh server
		data:Connection = self.connect_data
		
		try:
			self.ssh_server = SSHTunnelForwarder(
				data.host,
				ssh_port=data.port,
				ssh_username=data.username,
				ssh_password=data.password,
				remote_bind_address=('127.0.0.1', 80)
			)
			self.ssh_server.start()
			self.setHomeUrl("http://127.0.0.1:" + str(self.ssh_server.local_bind_port))
			
		except Exception as e:
			s = "Error: Failed to connect to %s:%d: %r".format(data.host, data.port, e)
			self.connect_dialog.label.setText(s)
			return
		
		if self.connect_dialog != None:
			self.connect_dialog.accept()
			
		pass
	
	
	def sshDisconnect(self):
		
		if self.thread_connect != None:
			self.thread_connect.stop()
			self.thread_connect = None
		
		if self.ssh_server != None:
			self.ssh_server.stop()
			self.ssh_server = None
	
	
	
	def connectToServer(self, data:Connection):
		
		print ("Connect to server")
		
		# Create connection dialog
		self.connect_dialog = ConnectDialog(self)
		
		# Setup connection
		self.connect_data = data
		
		# Connect to server
		self.thread_connect = threading.Thread(target=self.sshConnect)
		self.thread_connect.start()
		
		# Show connection dialog
		result = self.connect_dialog.exec()
		
		# Cancel connect
		if (result == 0):
			#self.sshDisconnect()
			self.close()
			
			print ("Cancel connect")
		
		# Success connect
		else:
			
			print ("Success connect")
			pass
		
		self.connect_dialog = None
		
		pass
	
	
	def setHomeUrl(self, url):
		self.home_url = url
		
		webBrowser:QWebEngineView = self.webBrowser
		webBrowser.setUrl( QUrl(self.home_url) )
		
	
	def onPrevButtonClick(self):
		webBrowser:QWebEngineView = self.webBrowser
		webBrowser.back()
	
	
	def onNextButtonClick(self):
		webBrowser:QWebEngineView = self.webBrowser
		webBrowser.forward()
	
	
	def onRefreshButtonClick(self):
		webBrowser:QWebEngineView = self.webBrowser
		webBrowser.reload()
	
	
	def onHomeButtonClick(self):
		webBrowser:QWebEngineView = self.webBrowser
		webBrowser.setUrl( QUrl(self.home_url) )
	
	
	def onUrlEditChange(self):
		url = self.urlEdit.text()
		webBrowser:QWebEngineView = self.webBrowser
		webBrowser.setUrl( QUrl(url) )
	
	
	def onWebBrowserUrlChange(self, url):
		self.urlEdit.setText(url.toString())
		pass
	

class MainWindow(QMainWindow, Ui_MainWindow):
	
	
	def __init__(self):
		QMainWindow.__init__(self)
		
		# Set a title
		self.setupUi(self)
		self.setWindowTitle("BAYRELL OS Desktop Client")
		
		# Set to center
		self.set_window_center()
		
		# Load items
		self.loadItems()
		
		# Add action
		self.addButton.clicked.connect(self.onAddClick)
		self.editButton.clicked.connect(self.onEditClick)
		self.deleteButton.clicked.connect(self.onDeleteClick)
		self.connectButton.clicked.connect(self.onConnectClick)
		
		pass
	
	
	def show_connection_dialog(self, item:QListWidgetItem = None):
		dlg = EditConnectionDialog()
		
		if item != None:
			data = item.data(1)
			dlg.connectionNameEdit.setText( data.connection_name )
			dlg.hostEdit.setText( data.host )
			dlg.portEdit.setText( data.port )
			dlg.usernameEdit.setText( data.username )
			dlg.passwordEdit.setText( data.password )
		
		result = dlg.exec()
		
		if result == 1:
			
			# Create data
			data = Connection()
			data.connection_name = dlg.connectionNameEdit.text()
			data.host = dlg.hostEdit.text()
			data.port = dlg.portEdit.text()
			data.username = dlg.usernameEdit.text()
			data.password = dlg.passwordEdit.text()
			
			# Add data to list widget
			if item == None:
				item = QListWidgetItem(data.connection_name)
				item.setData(1, data)
				self.listWidget.addItem(item)
			
			else:
				item.setText(data.connection_name)
				item.setData(1, data)
	
		
	def set_window_center(self):
		
		desktop = QApplication.desktop()
		screen_number = desktop.screenNumber(desktop.cursor().pos())
		center = desktop.screenGeometry(screen_number).center()
		
		window_size = self.size()
		width = window_size.width(); 
		height = window_size.height();
		
		x = center.x() - width / 2;
		y = center.y() - height / 2;
		
		self.move ( x, y );
		
		
	def getConnectionsFileName(self):
		path = os.path.expanduser('~')
		path = os.path.join(path, ".config", "bayrell_os")
		os.makedirs(path, exist_ok=True)
		file_name = os.path.join(path, "connections.json")
		return file_name
	
	
	def loadItems(self):
		
		file_name = self.getConnectionsFileName()
		file_content = ""
		
		try:
			if os.path.exists(file_name):
				with open(file_name) as file:
					file_content = file.read()
					file.close()
				
				objects = json.loads(file_content)
				for obj in objects:
					
					data = Connection()
					data.connection_name = obj["connection_name"]
					data.host = obj["host"]
					data.port = obj["port"]
					data.username = obj["username"]
					data.password = obj["password"]
					
					item = QListWidgetItem(data.connection_name)
					item.setData(1, data)
					self.listWidget.addItem(item)
				
		finally:
			pass
		
		pass
	
	def saveItems(self):
		
		objects = []
		for row in range(self.listWidget.count()):
			item = self.listWidget.item(row)
			
			data = item.data(1)
			obj = {
				"connection_name": data.connection_name,
				"host": data.host,
				"port": data.port,
				"username": data.username,
				"password": data.password,
			}
			
			objects.append(obj)
		
		text = json.dumps(objects, indent=2) 
		
		file_name = self.getConnectionsFileName()
		with open(file_name, "w") as file:
			file.write(text)
			file.close()
			
		pass
	
	
	def onAddClick(self):
		self.show_connection_dialog()
		self.saveItems()
	
	
	def onEditClick(self):
		
		items = self.listWidget.selectedIndexes()
		if len(items) > 0:
			self.show_connection_dialog( self.listWidget.item(items[0].row()) )
			
		self.saveItems()
	
	
	def onDeleteClick(self):
		items = self.listWidget.selectedIndexes()
		for item in items:
			row = item.row()
			self.listWidget.takeItem(row)
		
		self.saveItems()
	
	
	def onConnectClick(self):
		
		items = self.listWidget.selectedIndexes()
		if len(items) > 0:
			row = items[0].row()
			item = self.listWidget.item(row)
			data = item.data(1)
			
			web_browser = WebBrowser(self)
			web_browser.show()
			web_browser.connectToServer(data)
		
		pass
	
	
def run():
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	sys.exit(app.exec())

