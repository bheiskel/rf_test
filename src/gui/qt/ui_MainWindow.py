# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(540, 540)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QSize(540, 540))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMinimumSize(QSize(540, 540))
        self.centralwidget.setMaximumSize(QSize(540, 540))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.programmerWidget = QWidget(self.centralwidget)
        self.programmerWidget.setObjectName(u"programmerWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.programmerWidget.sizePolicy().hasHeightForWidth())
        self.programmerWidget.setSizePolicy(sizePolicy2)
        self.verticalLayout = QVBoxLayout(self.programmerWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.RFTestVersionWidget = QWidget(self.programmerWidget)
        self.RFTestVersionWidget.setObjectName(u"RFTestVersionWidget")
        sizePolicy2.setHeightForWidth(self.RFTestVersionWidget.sizePolicy().hasHeightForWidth())
        self.RFTestVersionWidget.setSizePolicy(sizePolicy2)
        self.horizontalLayout_5 = QHBoxLayout(self.RFTestVersionWidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.rfTestVersionLabel = QLabel(self.RFTestVersionWidget)
        self.rfTestVersionLabel.setObjectName(u"rfTestVersionLabel")

        self.horizontalLayout_5.addWidget(self.rfTestVersionLabel)

        self.rfTestVersion = QLabel(self.RFTestVersionWidget)
        self.rfTestVersion.setObjectName(u"rfTestVersion")

        self.horizontalLayout_5.addWidget(self.rfTestVersion)


        self.verticalLayout.addWidget(self.RFTestVersionWidget, 0, Qt.AlignmentFlag.AlignLeft)

        self.donleFWVersionWidget = QWidget(self.programmerWidget)
        self.donleFWVersionWidget.setObjectName(u"donleFWVersionWidget")
        sizePolicy2.setHeightForWidth(self.donleFWVersionWidget.sizePolicy().hasHeightForWidth())
        self.donleFWVersionWidget.setSizePolicy(sizePolicy2)
        self.horizontalLayout_7 = QHBoxLayout(self.donleFWVersionWidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.dongleFWVersionLabel = QLabel(self.donleFWVersionWidget)
        self.dongleFWVersionLabel.setObjectName(u"dongleFWVersionLabel")

        self.horizontalLayout_7.addWidget(self.dongleFWVersionLabel)

        self.dongleFWVersion = QLabel(self.donleFWVersionWidget)
        self.dongleFWVersion.setObjectName(u"dongleFWVersion")

        self.horizontalLayout_7.addWidget(self.dongleFWVersion)


        self.verticalLayout.addWidget(self.donleFWVersionWidget, 0, Qt.AlignmentFlag.AlignLeft)

        self.programForm = QFormLayout()
        self.programForm.setObjectName(u"programForm")
        self.debuggerLabel = QLabel(self.programmerWidget)
        self.debuggerLabel.setObjectName(u"debuggerLabel")

        self.programForm.setWidget(0, QFormLayout.LabelRole, self.debuggerLabel)

        self.debuggerSNR = QComboBox(self.programmerWidget)
        self.debuggerSNR.setObjectName(u"debuggerSNR")

        self.programForm.setWidget(0, QFormLayout.FieldRole, self.debuggerSNR)

        self.deviceVersionLabel = QLabel(self.programmerWidget)
        self.deviceVersionLabel.setObjectName(u"deviceVersionLabel")

        self.programForm.setWidget(1, QFormLayout.LabelRole, self.deviceVersionLabel)

        self.deviceVersion = QComboBox(self.programmerWidget)
        self.deviceVersion.setObjectName(u"deviceVersion")

        self.programForm.setWidget(1, QFormLayout.FieldRole, self.deviceVersion)

        self.loadCapacitorLabel = QLabel(self.programmerWidget)
        self.loadCapacitorLabel.setObjectName(u"loadCapacitorLabel")

        self.programForm.setWidget(2, QFormLayout.LabelRole, self.loadCapacitorLabel)

        self.loadCapacitor = QLineEdit(self.programmerWidget)
        self.loadCapacitor.setObjectName(u"loadCapacitor")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.loadCapacitor.sizePolicy().hasHeightForWidth())
        self.loadCapacitor.setSizePolicy(sizePolicy3)
        self.loadCapacitor.setMinimumSize(QSize(0, 0))

        self.programForm.setWidget(2, QFormLayout.FieldRole, self.loadCapacitor)


        self.verticalLayout.addLayout(self.programForm)

        self.radioButtons = QWidget(self.programmerWidget)
        self.radioButtons.setObjectName(u"radioButtons")
        sizePolicy2.setHeightForWidth(self.radioButtons.sizePolicy().hasHeightForWidth())
        self.radioButtons.setSizePolicy(sizePolicy2)
        self.horizontalLayout_3 = QHBoxLayout(self.radioButtons)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.FEM = QRadioButton(self.radioButtons)
        self.FEM.setObjectName(u"FEM")

        self.horizontalLayout_3.addWidget(self.FEM)


        self.verticalLayout.addWidget(self.radioButtons)

        self.femPinWidget = QWidget(self.programmerWidget)
        self.femPinWidget.setObjectName(u"femPinWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.femPinWidget.sizePolicy().hasHeightForWidth())
        self.femPinWidget.setSizePolicy(sizePolicy4)
        self.verticalLayout_3 = QVBoxLayout(self.femPinWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.femPinsLabel = QLabel(self.femPinWidget)
        self.femPinsLabel.setObjectName(u"femPinsLabel")

        self.verticalLayout_3.addWidget(self.femPinsLabel, 0, Qt.AlignmentFlag.AlignHCenter)

        self.femPins = QFormLayout()
        self.femPins.setObjectName(u"femPins")
        self.txEnLabel = QLabel(self.femPinWidget)
        self.txEnLabel.setObjectName(u"txEnLabel")

        self.femPins.setWidget(0, QFormLayout.LabelRole, self.txEnLabel)

        self.txEnPin = QLineEdit(self.femPinWidget)
        self.txEnPin.setObjectName(u"txEnPin")

        self.femPins.setWidget(0, QFormLayout.FieldRole, self.txEnPin)

        self.rxEnLabel = QLabel(self.femPinWidget)
        self.rxEnLabel.setObjectName(u"rxEnLabel")

        self.femPins.setWidget(1, QFormLayout.LabelRole, self.rxEnLabel)

        self.rxEnPin = QLineEdit(self.femPinWidget)
        self.rxEnPin.setObjectName(u"rxEnPin")

        self.femPins.setWidget(1, QFormLayout.FieldRole, self.rxEnPin)

        self.pdnLabel = QLabel(self.femPinWidget)
        self.pdnLabel.setObjectName(u"pdnLabel")

        self.femPins.setWidget(2, QFormLayout.LabelRole, self.pdnLabel)

        self.pdnPin = QLineEdit(self.femPinWidget)
        self.pdnPin.setObjectName(u"pdnPin")

        self.femPins.setWidget(2, QFormLayout.FieldRole, self.pdnPin)

        self.modeLabel = QLabel(self.femPinWidget)
        self.modeLabel.setObjectName(u"modeLabel")

        self.femPins.setWidget(3, QFormLayout.LabelRole, self.modeLabel)

        self.modePin = QLineEdit(self.femPinWidget)
        self.modePin.setObjectName(u"modePin")

        self.femPins.setWidget(3, QFormLayout.FieldRole, self.modePin)

        self.antSelLabel = QLabel(self.femPinWidget)
        self.antSelLabel.setObjectName(u"antSelLabel")

        self.femPins.setWidget(4, QFormLayout.LabelRole, self.antSelLabel)

        self.antSelPin = QLineEdit(self.femPinWidget)
        self.antSelPin.setObjectName(u"antSelPin")

        self.femPins.setWidget(4, QFormLayout.FieldRole, self.antSelPin)


        self.verticalLayout_3.addLayout(self.femPins)


        self.verticalLayout.addWidget(self.femPinWidget)

        self.buttonWidget = QWidget(self.programmerWidget)
        self.buttonWidget.setObjectName(u"buttonWidget")
        sizePolicy1.setHeightForWidth(self.buttonWidget.sizePolicy().hasHeightForWidth())
        self.buttonWidget.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.buttonWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.buttonRows = QVBoxLayout()
        self.buttonRows.setObjectName(u"buttonRows")
        self.buttonRow1 = QHBoxLayout()
        self.buttonRow1.setObjectName(u"buttonRow1")
        self.flashButton = QPushButton(self.buttonWidget)
        self.flashButton.setObjectName(u"flashButton")

        self.buttonRow1.addWidget(self.flashButton)

        self.recoverButton = QPushButton(self.buttonWidget)
        self.recoverButton.setObjectName(u"recoverButton")

        self.buttonRow1.addWidget(self.recoverButton)

        self.resetButton = QPushButton(self.buttonWidget)
        self.resetButton.setObjectName(u"resetButton")

        self.buttonRow1.addWidget(self.resetButton)


        self.buttonRows.addLayout(self.buttonRow1)

        self.buttonRow2 = QHBoxLayout()
        self.buttonRow2.setObjectName(u"buttonRow2")
        self.detectDeviceButton = QPushButton(self.buttonWidget)
        self.detectDeviceButton.setObjectName(u"detectDeviceButton")

        self.buttonRow2.addWidget(self.detectDeviceButton)

        self.updateDebuggersButton = QPushButton(self.buttonWidget)
        self.updateDebuggersButton.setObjectName(u"updateDebuggersButton")

        self.buttonRow2.addWidget(self.updateDebuggersButton)


        self.buttonRows.addLayout(self.buttonRow2)


        self.horizontalLayout_2.addLayout(self.buttonRows)


        self.verticalLayout.addWidget(self.buttonWidget)


        self.horizontalLayout.addWidget(self.programmerWidget, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.rfTestWiget = QWidget(self.centralwidget)
        self.rfTestWiget.setObjectName(u"rfTestWiget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.rfTestWiget.sizePolicy().hasHeightForWidth())
        self.rfTestWiget.setSizePolicy(sizePolicy5)
        self.verticalLayout_2 = QVBoxLayout(self.rfTestWiget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.rfTestWiget)
        self.label.setObjectName(u"label")
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.testLabel = QLabel(self.rfTestWiget)
        self.testLabel.setObjectName(u"testLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.testLabel)

        self.testType = QComboBox(self.rfTestWiget)
        self.testType.setObjectName(u"testType")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.testType)

        self.dataRateLabel = QLabel(self.rfTestWiget)
        self.dataRateLabel.setObjectName(u"dataRateLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.dataRateLabel)

        self.dataRate = QComboBox(self.rfTestWiget)
        self.dataRate.setObjectName(u"dataRate")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.dataRate)

        self.outputPowerLabel = QLabel(self.rfTestWiget)
        self.outputPowerLabel.setObjectName(u"outputPowerLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.outputPowerLabel)

        self.outputPower = QLineEdit(self.rfTestWiget)
        self.outputPower.setObjectName(u"outputPower")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.outputPower)

        self.firstChannelLabel = QLabel(self.rfTestWiget)
        self.firstChannelLabel.setObjectName(u"firstChannelLabel")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.firstChannelLabel)

        self.firstChannel = QLineEdit(self.rfTestWiget)
        self.firstChannel.setObjectName(u"firstChannel")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.firstChannel)

        self.lastChannelLabel = QLabel(self.rfTestWiget)
        self.lastChannelLabel.setObjectName(u"lastChannelLabel")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.lastChannelLabel)

        self.lastChannel = QLineEdit(self.rfTestWiget)
        self.lastChannel.setObjectName(u"lastChannel")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.lastChannel)


        self.verticalLayout_2.addLayout(self.formLayout_2)

        self.femSettingsWidget = QWidget(self.rfTestWiget)
        self.femSettingsWidget.setObjectName(u"femSettingsWidget")
        sizePolicy4.setHeightForWidth(self.femSettingsWidget.sizePolicy().hasHeightForWidth())
        self.femSettingsWidget.setSizePolicy(sizePolicy4)
        self.verticalLayout_4 = QVBoxLayout(self.femSettingsWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pinSettingsLabel = QLabel(self.femSettingsWidget)
        self.pinSettingsLabel.setObjectName(u"pinSettingsLabel")

        self.verticalLayout_4.addWidget(self.pinSettingsLabel, 0, Qt.AlignmentFlag.AlignHCenter)

        self.femSettings = QFormLayout()
        self.femSettings.setObjectName(u"femSettings")
        self.modeSettingLabel = QLabel(self.femSettingsWidget)
        self.modeSettingLabel.setObjectName(u"modeSettingLabel")

        self.femSettings.setWidget(0, QFormLayout.LabelRole, self.modeSettingLabel)

        self.modeSetting = QSpinBox(self.femSettingsWidget)
        self.modeSetting.setObjectName(u"modeSetting")
        self.modeSetting.setWrapping(True)
        self.modeSetting.setMaximum(1)

        self.femSettings.setWidget(0, QFormLayout.FieldRole, self.modeSetting)

        self.antSelSetting = QSpinBox(self.femSettingsWidget)
        self.antSelSetting.setObjectName(u"antSelSetting")
        self.antSelSetting.setWrapping(True)
        self.antSelSetting.setMinimum(0)
        self.antSelSetting.setMaximum(1)
        self.antSelSetting.setValue(0)

        self.femSettings.setWidget(1, QFormLayout.FieldRole, self.antSelSetting)

        self.antSelSettingLabel = QLabel(self.femSettingsWidget)
        self.antSelSettingLabel.setObjectName(u"antSelSettingLabel")

        self.femSettings.setWidget(1, QFormLayout.LabelRole, self.antSelSettingLabel)


        self.verticalLayout_4.addLayout(self.femSettings)


        self.verticalLayout_2.addWidget(self.femSettingsWidget)

        self.startButton = QPushButton(self.rfTestWiget)
        self.startButton.setObjectName(u"startButton")
        sizePolicy4.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy4)
        self.startButton.setToolTipDuration(-1)

        self.verticalLayout_2.addWidget(self.startButton)


        self.horizontalLayout.addWidget(self.rfTestWiget, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RF test", None))
        self.rfTestVersionLabel.setText(QCoreApplication.translate("MainWindow", u"RF Test version:", None))
        self.rfTestVersion.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.dongleFWVersionLabel.setText(QCoreApplication.translate("MainWindow", u"Dongle FW version:", None))
        self.dongleFWVersion.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.debuggerLabel.setText(QCoreApplication.translate("MainWindow", u"Debugger", None))
        self.deviceVersionLabel.setText(QCoreApplication.translate("MainWindow", u"Device version:", None))
        self.loadCapacitorLabel.setText(QCoreApplication.translate("MainWindow", u"HFXO Load capacitor:", None))
#if QT_CONFIG(tooltip)
        self.loadCapacitor.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Internal load capacitors in pF. To disable the internal load capacitors set this to 0. Leave blank to use default configuration.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.FEM.setText(QCoreApplication.translate("MainWindow", u"FEM", None))
        self.femPinsLabel.setText(QCoreApplication.translate("MainWindow", u"FEM pin config", None))
        self.txEnLabel.setText(QCoreApplication.translate("MainWindow", u"TX_EN", None))
#if QT_CONFIG(tooltip)
        self.txEnPin.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>TX enable pin. High when DUT transmitting, low otherwise.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.rxEnLabel.setText(QCoreApplication.translate("MainWindow", u"RX_EN", None))
#if QT_CONFIG(tooltip)
        self.rxEnPin.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>RX enable pin. High when DUT receiving, low otherwise.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pdnLabel.setText(QCoreApplication.translate("MainWindow", u"PDN", None))
#if QT_CONFIG(tooltip)
        self.pdnPin.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Power down pin, always high.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.modeLabel.setText(QCoreApplication.translate("MainWindow", u"MODE", None))
#if QT_CONFIG(tooltip)
        self.modePin.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Mode pin, state controlled by FEM config and can be changed without reflashing test firmware.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.antSelLabel.setText(QCoreApplication.translate("MainWindow", u"ANT_SEL", None))
#if QT_CONFIG(tooltip)
        self.antSelPin.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Antenna select pin, state controlled by FEM config and can be changed without reflashing test firmware.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.flashButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Flash test firmware to DUT, and writes load capacitor config and FEM pin config to DUT.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.flashButton.setText(QCoreApplication.translate("MainWindow", u"Flash", None))
#if QT_CONFIG(tooltip)
        self.recoverButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Recover the DUT by erasing flash and disabling readback protection.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.recoverButton.setText(QCoreApplication.translate("MainWindow", u"Recover", None))
#if QT_CONFIG(tooltip)
        self.resetButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Pin reset, requires DUT reset pin to be connected to the debugger.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.detectDeviceButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Gets device version of the connected DUT.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.detectDeviceButton.setText(QCoreApplication.translate("MainWindow", u"Detect device", None))
#if QT_CONFIG(tooltip)
        self.updateDebuggersButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Gets all debuggers available.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.updateDebuggersButton.setText(QCoreApplication.translate("MainWindow", u"Get debuggers", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Test config", None))
        self.testLabel.setText(QCoreApplication.translate("MainWindow", u"Test", None))
#if QT_CONFIG(tooltip)
        self.testType.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.dataRateLabel.setText(QCoreApplication.translate("MainWindow", u"Data Rate", None))
        self.outputPowerLabel.setText(QCoreApplication.translate("MainWindow", u"Output Power", None))
#if QT_CONFIG(tooltip)
        self.outputPower.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Output power in dBm. If the configured output power isn't possible by the radio, the closest possible radio output power not exeeding the configured output power will be used.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.firstChannelLabel.setText(QCoreApplication.translate("MainWindow", u"Frequency", None))
#if QT_CONFIG(tooltip)
        self.firstChannel.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Radio frequency in MHz offset from 2400MHz.</p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lastChannelLabel.setText(QCoreApplication.translate("MainWindow", u"Last Frequency", None))
#if QT_CONFIG(tooltip)
        self.lastChannel.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Ending sweep frequency in MHz offset from 2400MHz.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pinSettingsLabel.setText(QCoreApplication.translate("MainWindow", u"FEM config", None))
        self.modeSettingLabel.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.antSelSettingLabel.setText(QCoreApplication.translate("MainWindow", u"ANT_SEL", None))
#if QT_CONFIG(tooltip)
        self.startButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Start RF test.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
#if QT_CONFIG(shortcut)
        self.startButton.setShortcut(QCoreApplication.translate("MainWindow", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

