# -*- coding: utf-8 -*-

import sys
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
		self.setWindowTitle("BAYRELL OS Thin Desktop Client")
		
		# Set to center
		self.set_window_center()
		
		#self.show_connection_dialog()
		
		# Add action
		self.addButton.clicked.connect(self.onAddClick)
		self.editButton.clicked.connect(self.onEditClick)
		
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
		
	
	
	def onAddClick(self):
		self.show_connection_dialog()
		pass
	
	
	def onEditClick(self):
		
		items = self.listWidget.selectedIndexes()
		if len(items) > 0:
			self.show_connection_dialog( self.listWidget.item(items[0].row()) )
			
		pass
	
	
	
def run():
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	sys.exit(app.exec())

