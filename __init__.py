from PyQt5 import QtCore, QtGui, QtWidgets
# ui code generated using Qt Designer :):):)


class Colors:
	BLANK = 0, 0, 0
	WORM_SELECTED = 255, 0, 0
	PLAYER_SELECTED = 255, 0, 200  # 0, 139, 139


class Directions:
	FORWARD = 1
	BACKWARD = -1


class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.setFixedSize(365, 295)
		self.treeWidget = QtWidgets.QTreeWidget(Form)
		self.treeWidget.setGeometry(QtCore.QRect(10, 10, 191, 281))
		self.treeWidget.setObjectName("treeWidget")
		self.line_playername = QtWidgets.QLineEdit(Form)
		self.line_playername.setGeometry(QtCore.QRect(210, 10, 141, 20))
		self.line_playername.setText("")
		self.line_playername.setObjectName("line_playername")
		self.btn_add_player = QtWidgets.QPushButton(Form)
		self.btn_add_player.setGeometry(QtCore.QRect(210, 30, 71, 23))
		self.btn_add_player.setObjectName("btn_add_player")
		self.btn_add_worm = QtWidgets.QPushButton(Form)
		self.btn_add_worm.setGeometry(QtCore.QRect(280, 30, 71, 23))
		self.btn_add_worm.setObjectName("btn_add_worm")
		self.btn_skip_left = QtWidgets.QPushButton(Form)
		self.btn_skip_left.setGeometry(QtCore.QRect(210, 90, 71, 41))
		self.btn_skip_left.setObjectName("btn_skip_left")
		self.btn_skip_right = QtWidgets.QPushButton(Form)
		self.btn_skip_right.setGeometry(QtCore.QRect(280, 90, 71, 41))
		self.btn_skip_right.setObjectName("btn_skip_right")
		self.btn_remove = QtWidgets.QPushButton(Form)
		self.btn_remove.setGeometry(QtCore.QRect(210, 170, 141, 41))
		self.btn_remove.setObjectName("btn_remove")
		self.btn_nextup = QtWidgets.QPushButton(Form)
		self.btn_nextup.setGeometry(QtCore.QRect(210, 210, 141, 41))
		self.btn_nextup.setObjectName("btn_nextup")
		self._label_selected = QtWidgets.QLabel(Form)
		self._label_selected.setGeometry(QtCore.QRect(220, 150, 131, 16))
		self._label_selected.setObjectName("_label_selected")
		self._label_turn_skip = QtWidgets.QLabel(Form)
		self._label_turn_skip.setGeometry(QtCore.QRect(220, 70, 131, 16))
		self._label_turn_skip.setObjectName("_label_turn_skip")

		self.btn_add_player.clicked.connect(self.add_player)
		self.btn_add_worm.clicked.connect(self.add_worm)
		self.btn_remove.clicked.connect(self.remove_item)
		self.btn_nextup.clicked.connect(self.set_next_up)
		self.btn_skip_right.clicked.connect(self.rotate_forwards)
		self.btn_skip_left.clicked.connect(self.rotate_backwards)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Worms Turn Tracker"))
		self.treeWidget.headerItem().setText(0, _translate("Form", "Players > Next up"))
		self.treeWidget.setSortingEnabled(False)
		self.line_playername.setPlaceholderText(_translate("Form", "TheLegend27"))
		self.btn_add_player.setText(_translate("Form", "+ Player"))
		self.btn_add_worm.setText(_translate("Form", "+ Worm"))
		self.btn_skip_left.setText(_translate("Form", "<"))
		self.btn_skip_right.setText(_translate("Form", ">"))
		self.btn_remove.setText(_translate("Form", "Remove"))
		self.btn_nextup.setText(_translate("Form", "Set as next up"))
		self._label_selected.setText(_translate("Form", "Selected Actions"))
		self._label_turn_skip.setText(_translate("Form", "Turn Browser"))


	def _valid_name(self, parent):
		if text := self.line_playername.text().strip():
			for i in range(parent.childCount()):
				if text == parent.child(i).text(0):
					return None

		return text

	def get_selected(self):
		sel_items = self.treeWidget.selectedItems()
		if sel_items:
			return sel_items[0]

	def add_player(self):
		if text := self._valid_name(self.treeWidget.invisibleRootItem()):
			item = QtWidgets.QTreeWidgetItem([text])
			item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
			self.treeWidget.addTopLevelItem(item)

			# set as only selected
			self.treeWidget.clearSelection()
			item.setSelected(True)


			# if it's the first player, declare it as selected
			if self.treeWidget.invisibleRootItem().childCount() == 1:
				self._color_item(item, Colors.PLAYER_SELECTED)
			# !! dont do this after all, this sort of logic should occur only when worms are added
			# else:
			# 	# rotate to set the newly entered player as selected
			# 	self.rotate_forwards()

			# clear input box
			self.line_playername.clear()

	def add_worm(self):
		if selected := self.get_selected():
			# make the new worm
			item = QtWidgets.QTreeWidgetItem()
			item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)

			if selected.parent():
				# selected is a worm
				if text := self._valid_name(selected.parent()):
					selected.parent().addChild(item)

			else:
				# selected is a player
				if text := self._valid_name(selected):
					selected.addChild(item)

			if text:
				# the worm was successfully added
				item.setText(0, text)
				item.parent().setExpanded(True)
				# select the player (trigger standalone player rotation, ignoring worm rotation)
				self.turn()
				# if it's the first worm under this player, select it
				if item.parent().childCount() == 1:
					self._color_item(item, Colors.WORM_SELECTED)
				else:
					# select the newly appended worm
					self._worm_rotation(item.parent(), 1)
				# clear input box
				self.line_playername.clear()
				# click the next player in rotation to gracefully add worms
				root = self.treeWidget.invisibleRootItem()
				items = [root.child(i) for i in range(root.childCount())]
				index = items.index(selected)
				self.treeWidget.clearSelection()
				items[(index + 1) % len(items)].setSelected(True)

	def remove_item(self):
		if selected := self.get_selected():
			if selected.parent():
				selected.parent().removeChild(selected)
			else:
				self.treeWidget.invisibleRootItem().removeChild(selected)

			self.treeWidget.clearSelection()

	def _color_item(self, item, color=Colors.WORM_SELECTED):
		item.setForeground(0, QtGui.QBrush(QtGui.QColor(*color)))

	def _item_color(self, item):
		*rgb, alpha = item.foreground(0).color().getRgb()
		return tuple(rgb)

	def set_next_up(self):
		if selected := self.get_selected():
			if selected.parent():
				# it's a worm, iterate all of it's comrades
				for worm_index in range(selected.parent().childCount()):
					# deactivate
					self._color_item(selected.parent().child(worm_index), Colors.BLANK)
				self._color_item(selected, Colors.WORM_SELECTED)

			else:
				# it's a player, iterate players
				root = self.treeWidget.invisibleRootItem()
				for player_index in range(root.childCount()):
					# deactivate
					self._color_item(root.child(player_index), Colors.BLANK)
				self._color_item(selected, Colors.PLAYER_SELECTED)

			self.treeWidget.clearSelection()

	def rotate_forwards(self):
		self.treeWidget.clearSelection()
		self.turn()

	def rotate_backwards(self):
		self.treeWidget.clearSelection()
		self.turn(Directions.BACKWARD)

	def _worm_rotation(self, player, offset):
		# this is a standalone function as it should also trigger when a worm is added
		for worm_index in range(player.childCount()):
			if self._item_color(player.child(worm_index)) == Colors.WORM_SELECTED:
				# clear worm color
				self._color_item(player.child(worm_index), Colors.BLANK)
				# set next active worm
				new_worm = player.child((worm_index + offset) % player.childCount())
				self._color_item(new_worm, Colors.WORM_SELECTED)
				break

	def turn(self, direction=Directions.FORWARD, rotate_worms=True):
		"""
		correctly progress the turn color of selected player and it's worms
		"""
		# replace current player
		root = self.treeWidget.invisibleRootItem()
		for i in range(root.childCount()):
			if self._item_color(root.child(i)) == Colors.PLAYER_SELECTED:
				# clear player color
				self._color_item(root.child(i), Colors.BLANK)
				# set next active player
				self._color_item(root.child((i + direction) % root.childCount()), Colors.PLAYER_SELECTED)
				# progress (worm-rotate) the previous one that was just skipped from
				if rotate_worms:
					if direction == Directions.FORWARD:
						player = root.child(i)
					else:
						player = root.child((i + direction) % root.childCount())
					
					self._worm_rotation(player, direction)
				
				break


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Form = QtWidgets.QWidget()
	ui = Ui_Form()
	ui.setupUi(Form)
	Form.show()
	sys.exit(app.exec_())
