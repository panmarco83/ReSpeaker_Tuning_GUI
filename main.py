#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtUiTools import QUiLoader
import os
import sys

sys.path.insert(0, 'usb_4_mic_array/')

import tuning as res_tuning

class resp_gui( QtWidgets.QMainWindow ):
	def __init__( self, parent=None ):
		super( resp_gui, self ).__init__( parent )

		ui_file_name = "".join([ os.path.dirname( os.path.abspath(__file__) ), "/ui/main.ui"])
		ui_file = QtCore.QFile(ui_file_name)
		loader = QUiLoader()
		self.ui = loader.load(ui_file, self)
		ui_file.close()
		self.ui.show()

		self.current_values = {}
		self.device = res_tuning.find()
		self.update_current_values()
		self.populate_list()

	def populate_list( self ):
		self.ui.listWidget.clear()
		self.ui.listWidget.setAlternatingRowColors(True)

		for param in self.current_values:

			tmp_param_info = list( self.current_values[param]['defaults'] )
			for i in range(0,7):
				tmp_param_info.pop(0)
			cur_val = self.current_values[param]['cur_val']

			if self.current_values[param]['defaults'][5] == 'rw':
				if self.current_values[param]['defaults'][2] == 'int' and self.current_values[param]['defaults'][3] == 1:
					item = QtWidgets.QListWidgetItem()
					widget = QtWidgets.QWidget()
					layout = QtWidgets.QHBoxLayout()
					item.setData( QtCore.Qt.UserRole, param )

					info_label = QtWidgets.QLabel( self.current_values[param]['defaults'][6] )
					layout.addWidget(info_label)

					chkBox = QtWidgets.QCheckBox()
					if cur_val == 1:
						chkBox.setChecked( True )
					chkBox.setFixedWidth( 24 )
					chkBox.stateChanged.connect( lambda state=True, x=[param,chkBox]: self.update_bool_parameter(x) )
					tmp_opts = ""
					for i in tmp_param_info:
						tmp_opts += f"{i}\n"
					chkBox.setToolTip(tmp_opts)
					layout.addWidget(chkBox)

					widget.setLayout(layout)

					self.ui.listWidget.addItem( item )
					item.setSizeHint( widget.sizeHint() )
					self.ui.listWidget.setItemWidget( item, widget )

				if self.current_values[param]['defaults'][2] == 'int' and self.current_values[param]['defaults'][3] >= 2:
					item = QtWidgets.QListWidgetItem()
					widget = QtWidgets.QWidget()
					layout = QtWidgets.QHBoxLayout()
					item.setData( QtCore.Qt.UserRole, param )

					info_label = QtWidgets.QLabel( self.current_values[param]['defaults'][6] )
					layout.addWidget(info_label)

					combobox = QtWidgets.QComboBox()
					for i in tmp_param_info:
						combobox.addItem(i)
					combobox.setCurrentIndex( cur_val )
					combobox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
					combobox.currentIndexChanged.connect( lambda state=True, x=[param,combobox]: self.update_val_parameter(x) )
					layout.addWidget( combobox )

					widget.setLayout(layout)

					self.ui.listWidget.addItem( item )
					item.setSizeHint( widget.sizeHint() )
					self.ui.listWidget.setItemWidget( item, widget )

				elif self.current_values[param]['defaults'][2] == 'float' and self.current_values[param]['defaults'][3] == 1:
					item = QtWidgets.QListWidgetItem()
					widget = QtWidgets.QWidget()
					layout = QtWidgets.QHBoxLayout()
					item.setData( QtCore.Qt.UserRole, param )

					info_label = QtWidgets.QLabel( self.current_values[param]['defaults'][6] )
					info_label.setWordWrap(True)
					layout.addWidget(info_label)

					float_val = QtWidgets.QDoubleSpinBox()
					
					float_val.setFixedWidth( 192 )
					float_val.setSingleStep(0.00001)
					float_val.setDecimals(len(str(cur_val).split(".")[1]))
					float_val.setMaximum( self.current_values[param]['defaults'][3] )
					temp_tt = f"Maximum: {self.current_values[param]['defaults'][3]}\nMinimum: {self.current_values[param]['defaults'][4]}"
					float_val.setToolTip(temp_tt)
					float_val.setValue( cur_val )
					float_val.valueChanged.connect( lambda state=True, x=[param,float_val]: self.update_float_parameter(x) )
					tmp_opts = ""
					for i in tmp_param_info:
						tmp_opts += f"{i}\n"
					float_val.setToolTip(tmp_opts)
					layout.addWidget(float_val)


					widget.setLayout(layout)

					self.ui.listWidget.addItem( item )
					item.setSizeHint( widget.sizeHint() )
					self.ui.listWidget.setItemWidget( item, widget )

			elif self.current_values[param]['defaults'][5] == 'ro':
				item = QtWidgets.QListWidgetItem()
				widget = QtWidgets.QWidget()
				layout = QtWidgets.QHBoxLayout()
				item.setData( QtCore.Qt.UserRole, param )

				info_label = QtWidgets.QLabel( self.current_values[param]['defaults'][6] )
				info_label.setWordWrap(True)
				layout.addWidget(info_label)

				read_only_value = QtWidgets.QLabel()
				ro_val = ""
				if cur_val == 1:
					ro_val = "Enabled"
				else:
					ro_val = "Disabled"
				read_only_value.setText(ro_val)
				tmp_opts = ""
				for i in tmp_param_info:
					tmp_opts += f"{i}\n"
				read_only_value.setToolTip(tmp_opts)
				read_only_value.setAlignment(QtGui.Qt.AlignRight)
				layout.addWidget( read_only_value )
				widget.setLayout(layout)

				self.ui.listWidget.addItem( item )
				item.setSizeHint( widget.sizeHint() )
				self.ui.listWidget.setItemWidget( item, widget )

	def update_current_values( self ):
		for name in sorted( res_tuning.PARAMETERS.keys() ):
			temp_current_val = self.device.read(name)
			self.current_values[ name ] = {"defaults": res_tuning.PARAMETERS[name], "cur_val": temp_current_val }

	def update_bool_parameter( self, par_name ):
		self.device.write( par_name[0], int( par_name[1].isChecked() ) )

	def update_val_parameter( self, par_name ):
		self.device.write( par_name[0], par_name[1].currentIndex() )

	def update_float_parameter( self, par_name ):
		self.device.write( par_name[0], par_name[1].value() )

if __name__ == '__main__':

	#import sys
	QtCore.QCoreApplication.setAttribute( QtCore.Qt.AA_ShareOpenGLContexts )
	app = QtWidgets.QApplication( sys.argv )

	window = resp_gui()
	sys.exit(app.exec_())
