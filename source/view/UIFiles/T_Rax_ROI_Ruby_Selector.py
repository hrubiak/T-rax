# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_ROI_Ruby_Selector.ui'
#
# Created: Wed Jul  9 08:08:08 2014
# by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_roi_selector_ruby_widget(object):
    def setupUi(self, roi_selector_ruby_widget):
        roi_selector_ruby_widget.setObjectName(_fromUtf8("roi_selector_ruby_widget"))
        roi_selector_ruby_widget.resize(945, 504)
        roi_selector_ruby_widget.setStyleSheet(_fromUtf8("QWidget{  \n"
                                                         "     background: rgba(30, 30, 30, 255);      \n"
                                                         "     color: #F1F1F1; \n"
                                                         "    font-size: 12px;\n"
                                                         " }  \n"
                                                         "\n"
                                                         "QGroupBox {  \n"
                                                         "     border: 1px solid #ADADAD;  \n"
                                                         "     border-radius: 4px;  \n"
                                                         "     margin-top: 7px;  \n"
                                                         "     padding: 0px  \n"
                                                         " }  \n"
                                                         "\n"
                                                         "QPushButton{  \n"
                                                         "     color: #F1F1F1;\n"
                                                         "     background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop:1 #505050);\n"
                                                         "     border: 1px solid #5B5B5B;\n"
                                                         "     border-radius: 5px; \n"
                                                         "     padding-left: 8px;\n"
                                                         "height: 18px;\n"
                                                         "    padding-right: 8px;   \n"
                                                         " }  \n"
                                                         "QPushButton:pressed{\n"
                                                         "        margin-top: 2,px;\n"
                                                         "        margin-left: 2px;   \n"
                                                         "}\n"
                                                         "QPushButton::disabled{\n"
                                                         "}\n"
                                                         "\n"
                                                         "QPushButton::hover{  \n"
                                                         "     border:1px solid #ADADAD; \n"
                                                         " }  \n"
                                                         " \n"
                                                         "\n"
                                                         "QPushButton::checked{\n"
                                                         "    background: qlineargradient(\n"
                                                         "        x1: 0, y1: 1, \n"
                                                         "        x2: 0, y2: 0,\n"
                                                         "        stop: 0 #727272, \n"
                                                         "        stop: 1 #444444\n"
                                                         "    );\n"
                                                         "     border:1px solid  rgb(255, 120,00);\n"
                                                         "}\n"
                                                         "\n"
                                                         "QPushButton::focus {\n"
                                                         "    outline: None;\n"
                                                         "}\n"
                                                         "\n"
                                                         " QGroupBox::title {  \n"
                                                         "      subcontrol-origin: margin;  \n"
                                                         "      left: 20px  \n"
                                                         "  }\n"
                                                         "\n"
                                                         "\n"
                                                         " QLineEdit  {  \n"
                                                         "     border-radius: 2px;  \n"
                                                         "     background: #F1F1F1;  \n"
                                                         "     color: black;  \n"
                                                         "    height: 18 px;\n"
                                                         " }  \n"
                                                         "\n"
                                                         "#roi_box{\n"
                                                         "    color:  rgba(197, 0, 3, 255);\n"
                                                         "    border: 1px solid rgba(197, 0, 3, 255);\n"
                                                         "}\n"
                                                         ""))
        self.horizontalLayout = QtGui.QHBoxLayout(roi_selector_ruby_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.axes_frame = QtGui.QFrame(roi_selector_ruby_widget)
        self.axes_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.axes_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.axes_frame.setObjectName(_fromUtf8("axes_frame"))
        self.horizontalLayout.addWidget(self.axes_frame)
        self.frame = QtGui.QFrame(roi_selector_ruby_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.roi_box = QtGui.QGroupBox(self.frame)
        self.roi_box.setMinimumSize(QtCore.QSize(180, 0))
        self.roi_box.setMaximumSize(QtCore.QSize(180, 16777215))
        self.roi_box.setObjectName(_fromUtf8("roi_box"))
        self.verticalLayout = QtGui.QVBoxLayout(self.roi_box)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.roi_box)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.x_min_txt = QtGui.QLineEdit(self.roi_box)
        self.x_min_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.x_min_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.x_min_txt.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.x_min_txt.setObjectName(_fromUtf8("x_min_txt"))
        self.gridLayout.addWidget(self.x_min_txt, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.roi_box)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.x_max_txt = QtGui.QLineEdit(self.roi_box)
        self.x_max_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.x_max_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.x_max_txt.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.x_max_txt.setObjectName(_fromUtf8("x_max_txt"))
        self.gridLayout.addWidget(self.x_max_txt, 0, 2, 1, 1)
        self.y_min_txt = QtGui.QLineEdit(self.roi_box)
        self.y_min_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.y_min_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.y_min_txt.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.y_min_txt.setObjectName(_fromUtf8("y_min_txt"))
        self.gridLayout.addWidget(self.y_min_txt, 1, 1, 1, 1)
        self.y_max_txt = QtGui.QLineEdit(self.roi_box)
        self.y_max_txt.setMinimumSize(QtCore.QSize(60, 22))
        self.y_max_txt.setMaximumSize(QtCore.QSize(60, 16777215))
        self.y_max_txt.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.y_max_txt.setObjectName(_fromUtf8("y_max_txt"))
        self.gridLayout.addWidget(self.y_max_txt, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_3.addWidget(self.roi_box)
        self.widget_2 = QtGui.QWidget(self.frame)
        self.widget_2.setMinimumSize(QtCore.QSize(180, 0))
        self.widget_2.setMaximumSize(QtCore.QSize(180, 16777215))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.save_btn = QtGui.QPushButton(self.widget_2)
        self.save_btn.setMaximumSize(QtCore.QSize(80, 16777215))
        self.save_btn.setObjectName(_fromUtf8("save_btn"))
        self.horizontalLayout_5.addWidget(self.save_btn)
        self.cancel_btn = QtGui.QPushButton(self.widget_2)
        self.cancel_btn.setMaximumSize(QtCore.QSize(80, 16777215))
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.horizontalLayout_5.addWidget(self.cancel_btn)
        self.verticalLayout_3.addWidget(self.widget_2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(roi_selector_ruby_widget)
        QtCore.QMetaObject.connectSlotsByName(roi_selector_ruby_widget)

    def retranslateUi(self, roi_selector_ruby_widget):
        roi_selector_ruby_widget.setWindowTitle(_translate("roi_selector_ruby_widget", "Form", None))
        self.roi_box.setTitle(_translate("roi_selector_ruby_widget", "ROI Limits", None))
        self.label_3.setText(_translate("roi_selector_ruby_widget", "X:", None))
        self.x_min_txt.setText(_translate("roi_selector_ruby_widget", "5", None))
        self.label_4.setText(_translate("roi_selector_ruby_widget", "Y:", None))
        self.x_max_txt.setText(_translate("roi_selector_ruby_widget", "100", None))
        self.y_min_txt.setText(_translate("roi_selector_ruby_widget", "20", None))
        self.y_max_txt.setText(_translate("roi_selector_ruby_widget", "30", None))
        self.save_btn.setText(_translate("roi_selector_ruby_widget", "Save", None))
        self.cancel_btn.setText(_translate("roi_selector_ruby_widget", "Cancel", None))
