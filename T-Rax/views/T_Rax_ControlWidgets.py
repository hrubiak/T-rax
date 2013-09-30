from PyQt4 import QtGui
from UIFiles.T_Rax_TemperatureControl import Ui_temperature_control_widget
from UIFiles.T_Rax_RubyControl import Ui_ruby_control_widget
from UIFiles.T_Rax_DiamondControl import Ui_diamond_control_widget
import numpy as np


class TemperatureControlWidget(QtGui.QWidget, Ui_temperature_control_widget):
    def __init__(self, parent = None):
        super(TemperatureControlWidget, self).__init__(parent)
        self.setupUi(self)

    def set_fit_limits(self, limits):
        self.fit_from_txt.setText(str(int(np.round(limits[0]))))
        self.fit_to_txt.setText(str(int(np.round(limits[1]))))
        
    def get_fit_limits(self):
        return [int(self.fit_from_txt.text()),
                int(self.fit_to_txt.text())]

class RubyControlWidget(QtGui.QWidget, Ui_ruby_control_widget):
    def __init__(self, parent = None):
        super(RubyControlWidget, self).__init__(parent)
        self.setupUi(self)

class DiamondControlWidget(QtGui.QWidget, Ui_diamond_control_widget):
    def __init__(self, parent = None):
        super(DiamondControlWidget, self).__init__(parent)
        self.setupUi(self)