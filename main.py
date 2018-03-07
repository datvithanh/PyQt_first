import os
import sys
import time
import signal
import psutil
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

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(950, 621)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 925, 411))
        self.tableWidget.setRowCount(350)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.horizontalHeader().setDefaultSectionSize(137)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(57)
        self.tableWidget.verticalHeader().setDefaultSectionSize(40)
        #btn
        self.btn_pid = QtGui.QPushButton(self.centralwidget)
        self.btn_pid.setGeometry(QtCore.QRect(10, 550, 111, 41))
        self.btn_pid.setAutoRepeatDelay(300)
        self.btn_pid.setObjectName(_fromUtf8("btn_pid"))

        self.btn_cpu = QtGui.QPushButton(self.centralwidget)
        self.btn_cpu.setGeometry(QtCore.QRect(140, 550, 111, 41))
        self.btn_cpu.setObjectName(_fromUtf8("btn_cpu"))

        self.btn_mem = QtGui.QPushButton(self.centralwidget)
        self.btn_mem.setGeometry(QtCore.QRect(270, 550, 111, 41))
        self.btn_mem.setObjectName(_fromUtf8("btn_mem"))

        self.btn_kill = QtGui.QPushButton(self.centralwidget)
        self.btn_kill.setGeometry(QtCore.QRect(790, 550, 111, 41))
        self.btn_kill.setObjectName(_fromUtf8("btn_kill"))
        self.btn_kill.setStyleSheet("background-color: #fc7979; border-radius: 5px; color: white")

        self.label_sort = QtGui.QLabel(self.centralwidget)
        self.label_sort.setGeometry(QtCore.QRect(10, 520, 191, 17))
        self.label_sort.setObjectName(_fromUtf8("label_sort"))

        self.label_count = QtGui.QLabel(self.centralwidget)
        self.label_count.setGeometry(QtCore.QRect(10, 430, 371, 17))
        self.label_count.setObjectName(_fromUtf8("label_count"))

        self.label_ram = QtGui.QLabel(self.centralwidget)
        self.label_ram.setGeometry(QtCore.QRect(10, 450, 520, 17))
        self.label_ram.setObjectName(_fromUtf8("label_ram"))

        self.label_cpu = QtGui.QLabel(self.centralwidget)
        self.label_cpu.setGeometry(QtCore.QRect(10, 470, 371, 17))
        self.label_cpu.setObjectName(_fromUtf8("label_cpu"))

        self.text_search = QtGui.QPlainTextEdit(self.centralwidget)
        self.text_search.setGeometry(QtCore.QRect(430, 550, 141, 41))
        self.text_search.setObjectName(_fromUtf8("text_search"))

        self.label_search = QtGui.QLabel(self.centralwidget)
        self.label_search.setGeometry(QtCore.QRect(430, 520, 151, 17))
        self.label_search.setObjectName(_fromUtf8("label_search"))

        self.btn_search = QtGui.QPushButton(self.centralwidget)
        self.btn_search.setGeometry(QtCore.QRect(580, 550, 111, 41))
        self.btn_search.setObjectName(_fromUtf8("pushButton"))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        header_labels = "Pid Name Parent User Status %CPU %MEM".split()

        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setHorizontalHeaderLabels(header_labels)
        self.btn_pid.clicked.connect(self.loadDataPid)
        self.btn_cpu.clicked.connect(self.loadDataCpu)
        self.btn_mem.clicked.connect(self.loadDataMem)
        self.btn_kill.clicked.connect(self.killProcess)
        self.btn_search.clicked.connect(self.search)
        self.tableWidget.setColumnWidth(0, 50)

        self.loadDataPid()
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("Process manager", "Process manager", None))
        self.btn_pid.setText(_translate("MainWindow", "PID", None))
        self.btn_cpu.setText(_translate("MainWindow", "%CPU", None))
        self.btn_mem.setText(_translate("MainWindow", "%MEM", None))
        self.btn_kill.setText(_translate("MainWindow", "KILL", None))
        self.label_sort.setText(_translate("MainWindow", "Sắp xếp chương trình theo:", None))
        self.label_search.setText(_translate("MainWindow", "Search tiến trình:", None))
        self.btn_search.setText(_translate("MainWindow", "SEARCH", None))
    
    def killProcess(self):
        choice = QtGui.QMessageBox.question(self.tableWidget, 'Dung chuong trinh!', 'Ban co chac muon dung chuong trinh nay?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            pid = int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
            sig=signal.SIGTERM
            if pid == os.getpid():
                raise RuntimeError("I refuse to kill myself")
            parent = psutil.Process(pid)
            parent.terminate()
            self.loadDataPid()
        else:
            pass

    def search(self):
        text = str(self.text_search.toPlainText())
        data = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status'])
            except psutil.NoSuchProcess:
                pass
            else:
                if text in pinfo['name']:
                    data.append(pinfo)
        if len(data) == 0:
            choice = QtGui.QMessageBox.information(self.tableWidget, 'Thong bao!', 'Khong tim thay chuong trinh ban muon tim?', QtGui.QMessageBox.Ok)

        for dataid, data_item in enumerate(data):
            parent = psutil.Process(data_item['pid']).parent()
            self.tableWidget.setItem(dataid, 0, QtGui.QTableWidgetItem(str(data_item['pid'])))

            self.tableWidget.setItem(dataid, 1, QtGui.QTableWidgetItem(str(data_item['name'])))

            if parent is None:
                self.tableWidget.setItem(dataid, 2, QtGui.QTableWidgetItem('None'))
            else:
                self.tableWidget.setItem(dataid, 2, QtGui.QTableWidgetItem('pid='+str(parent.pid) +'; name='+parent.name()))

            self.tableWidget.setItem(dataid, 3, QtGui.QTableWidgetItem(str(data_item['username'])))

            self.tableWidget.setItem(dataid, 4, QtGui.QTableWidgetItem(str(data_item['status'])))

            self.tableWidget.setItem(dataid, 5, QtGui.QTableWidgetItem("{0:.3f}".format(data_item['cpu_percent'])))

            self.tableWidget.setItem(dataid, 6, QtGui.QTableWidgetItem("{0:.3f}".format(data_item['memory_percent'])))

    def loadDataPid(self):
        self.label_count.setText(_translate("MainWindow", "Tổng số tiến trình: " + str(len(psutil.pids())), None))
        mem = psutil.virtual_memory();
        self.label_ram.setText(_translate("MainWindow", "RAM (MB): " + str(mem.total/(1024*1024)) + " total, " + str(mem.free/(1024*1024)) + " free, " + str(mem.available/(1024*1024)) + " available, " + str(mem.used/(1024*1024)) + " used, " + str((mem.buffers + mem.cached)/(1024*1024)) + " buff/cache.", None))
        self.label_cpu.setText(_translate("MainWindow", "CPU: " + str(psutil.cpu_percent()) + "%", None))

        data = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status'])
            except psutil.NoSuchProcess:
                pass
            else:
                data.append(pinfo)
        for dataid, data_item in enumerate(data):
            parent = psutil.Process(data_item['pid']).parent()
            self.tableWidget.setItem(dataid, 0, QtGui.QTableWidgetItem(str(data_item['pid'])))

            self.tableWidget.setItem(dataid, 1, QtGui.QTableWidgetItem(str(data_item['name'])))

            if parent is None:
                self.tableWidget.setItem(dataid, 2, QtGui.QTableWidgetItem('None'))
            else:
                self.tableWidget.setItem(dataid, 2, QtGui.QTableWidgetItem('pid='+str(parent.pid) +'; name='+parent.name()))

            self.tableWidget.setItem(dataid, 3, QtGui.QTableWidgetItem(str(data_item['username'])))

            self.tableWidget.setItem(dataid, 4, QtGui.QTableWidgetItem(str(data_item['status'])))

            self.tableWidget.setItem(dataid, 5, QtGui.QTableWidgetItem("{0:.3f}".format(data_item['cpu_percent'])))

            self.tableWidget.setItem(dataid, 6, QtGui.QTableWidgetItem("{0:.3f}".format(data_item['memory_percent'])))

    def loadDataCpu(self):
        self.label_count.setText(_translate("MainWindow", "Tổng số tiến trình: " + str(len(psutil.pids())), None))
        mem = psutil.virtual_memory();
        self.label_ram.setText(_translate("MainWindow", "RAM (MB): " + str(mem.total/(1024*1024)) + " total, " + str(mem.free/(1024*1024)) + " free, " + str(mem.available/(1024*1024)) + " available, " + str(mem.used/(1024*1024)) + " used, " + str((mem.buffers + mem.cached)/(1024*1024)) + " buff/cache.", None))
        self.label_cpu.setText(_translate("MainWindow", "CPU: " + str(psutil.cpu_percent()) + "%", None))

        data = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status'])
            except psutil.NoSuchProcess:
                pass
            else:
                data.append(pinfo)

        data.sort(key=lambda data_item: data_item['cpu_percent'], reverse=True)
        for dataid, data_item in enumerate(data):
            parent = psutil.Process(data_item['pid']).parent()
            self.tableWidget.setItem(dataid, 0, QtGui.QTableWidgetItem(str(data_item['pid'])))

            self.tableWidget.setItem(dataid, 1, QtGui.QTableWidgetItem(str(data_item['name'])))

            if parent is None:
                self.tableWidget.setItem(dataid, 2, QtGui.QTableWidgetItem('None'))
            else:
                self.tableWidget.setItem(dataid, 2, QtGui.QTableWidgetItem('pid='+str(parent.pid) +'; name='+parent.name()))

            self.tableWidget.setItem(dataid, 3, QtGui.QTableWidgetItem(str(data_item['username'])))

            self.tableWidget.setItem(dataid, 4, QtGui.QTableWidgetItem(str(data_item['status'])))

            self.tableWidget.setItem(dataid, 5, QtGui.QTableWidgetItem("{0:.3f}".format(data_item['cpu_percent'])))

            self.tableWidget.setItem(dataid, 6, QtGui.QTableWidgetItem("{0:.3f}".format(data_item['memory_percent'])))

    def loadDataMem(self):
        self.label_count.setText(_translate("MainWindow", "Tổng số tiến trình: " + str(len(psutil.pids())), None))
        mem = psutil.virtual_memory();
        self.label_ram.setText(_translate("MainWindow", "RAM (MB): " + str(mem.total/(1024*1024)) + " total, " + str(mem.free/(1024*1024)) + " free, " + str(mem.available/(1024*1024)) + " available, " + str(mem.used/(1024*1024)) + " used, " + str((mem.buffers + mem.cached)/(1024*1024)) + " buff/cache.", None))
        self.label_cpu.setText(_translate("MainWindow", "CPU: " + str(psutil.cpu_percent()) + "%", None))

        data = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status'])
            except psutil.NoSuchProcess:
                pass
            else:
                data.append(pinfo)

        data.sort(key=lambda data_item: data_item['memory_percent'], reverse=True)
        for dataid, data_item in enumerate(data):
            parent = psutil.Process(data_item['pid']).parent()
            self.tableWidget.setItem(dataid, 0, QtGui.QTableWidgetItem(str(data_item['pid'])))

            self.tableWidget.setItem(dataid, 1, QtGui.QTableWidgetItem(str(data_item['name'])))

            if parent is None:
                self.tableWidget.setItem(dataid, 2, QtGui.QTableWidgetItem('None'))
            else:
                self.tableWidget.setItem(dataid, 2, QtGui.QTableWidgetItem('pid='+str(parent.pid) +'; name='+parent.name()))

            self.tableWidget.setItem(dataid, 3, QtGui.QTableWidgetItem(str(data_item['username'])))

            self.tableWidget.setItem(dataid, 4, QtGui.QTableWidgetItem(str(data_item['status'])))

            self.tableWidget.setItem(dataid, 5, QtGui.QTableWidgetItem("{0:.3f}".format(data_item['cpu_percent'])))

            self.tableWidget.setItem(dataid, 6, QtGui.QTableWidgetItem("{0:.3f}".format(data_item['memory_percent'])))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
