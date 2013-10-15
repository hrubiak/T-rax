from UIFiles.T_Rax_OutputGraphWidget import Ui_output_graph_widget

from PyQt4 import QtGui, QtCore
import sys

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class TRaxOutputGraphView(QtGui.QWidget, Ui_output_graph_widget):
    def __init__(self, parent=None):
        super(TRaxOutputGraphView, self).__init__(None)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle('Output Graph')
        self.create_graph()
        self.resizeEvent = self.resize_graph

    def create_graph(self):
        self.figure = Figure(None, dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.graph_frame)

        graph_layout = QtGui.QVBoxLayout(self.graph_frame)
        graph_layout.setContentsMargins(0,0,0,0)
        graph_layout.setSpacing(0)
        graph_layout.setMargin(0)
        graph_layout.addWidget(self.canvas)
        self.canvas.setSizePolicy( QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        self.axes = self.figure.add_subplot(111)
        
    def plot_series(self, y_data, y_data_errors, color, label):
        x=xrange(len(y_data))
        self.axes.errorbar(x, y_data, yerr=y_data_errors, label=label,
                     color=color, lw=2, capsize=5, capthick=2,
                     marker='s', mec=color, ms=8)

    def set_axis_labels(self,x_axis_label, y_axis_label):
        self.axes.set_xlabel(x_axis_label)
        self.axes.set_ylabel(y_axis_label)

    def adjust_axes_limits(self):
        self.adjust_xlim()
        self.adjust_ylim()

    def adjust_xlim(self):
        old_xlim=self.axes.get_xlim()
        xlim_range=old_xlim[1]-old_xlim[0]
        self.axes.set_xlim(old_xlim[0]-0.05*xlim_range,
                           old_xlim[1]+0.05*xlim_range)

    def adjust_ylim(self):
        old_ylim=self.axes.get_ylim()
        ylim_range=old_ylim[1]-old_ylim[0]
        self.axes.set_ylim(old_ylim[0]-0.05*ylim_range,
                           old_ylim[1]+0.05*ylim_range)

    def redraw_figure(self):
        self.axes.legend(loc='best')
        self.figure.tight_layout()
        self.canvas.draw()

    def resize_graph(self, event):
        new_size=self.graph_frame.size()
        self.figure.set_size_inches([new_size.width() / 100.0, new_size.height() / 100.0])
        self.redraw_figure()

if __name__=='__main__':
    app=QtGui.QApplication(sys.argv)
    view=TRaxOutputGraphView()
    app.exec_()