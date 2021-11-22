# -*- coding: utf-8 -*-

import sys, os, json
from os.path import abspath, dirname, join
from .MainWindow import Ui_MainWindow
from .ConnectionDialog import Ui_ConnectionDialog

import PyQt5
from PyQt5.QtWidgets import \
	QApplication, QMainWindow, QSystemTrayIcon, QMenu, \
	QAction, QWidget, QStyle, QDialog, QMessageBox, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


main_window = None


class Connection():
	
	def __init__(self):
		self.connection_name = "";
		self.host = "";
		self.port = "";
		self.username = "";
		self.password = "";


class ConnectionDialog(QDialog, Ui_ConnectionDialog):
	
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		self.setWindowTitle("Connection")
		self.type = "add"



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
		
		pass
	
	
	def show_connection_dialog(self, item:QListWidgetItem = None):
		dlg = ConnectionDialog()
		
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
	
	
def run():
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	sys.exit(app.exec())

