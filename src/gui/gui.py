from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from src.gui.qt.ui_MainWindow import Ui_MainWindow
import src.gui.logic as gui_logic
from typing import List
import __main__

DEFAULT_TX_POWER = 0
DEFAULT_FIRST_CHANNEL = 40
DEFAULT_LAST_CHANNEL = 80


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, qApp):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.qApp = qApp
        self.updateFields()
        self.signals = gui_logic.guiSignals
        self.createConnections()

    def createConnections(self):
        '''
        Sets up signal and slot connections
        '''
        # GUI button signals
        self.flashButton.clicked.connect(self.flashDevice)
        self.recoverButton.clicked.connect(self.recoverDevice)
        self.detectDeviceButton.clicked.connect(self.getDevice)
        self.updateDebuggersButton.clicked.connect(self.getDebuggers)
        self.FEM.toggled.connect(self.femSettingsVisibility)
        self.startButton.clicked.connect(self.startTest)
        self.resetButton.clicked.connect(self.resetDevice)

        # GUI update signals
        self.signals.flash_device_result.connect(self.updateFlashButton)
        self.signals.update_device.connect(self.updateDevice)
        self.signals.dongle_fw_version.connect(self.updateDongleFWVersion)
        self.signals.connected_debuggers.connect(self.updateDebuggers)
        self.signals.connected_debuggers.connect(self.getDevice)
        self.signals.recovery_completed.connect(self.updateRecoverButton)
        self.signals.test_started_success.connect(self.updateStartButton)
        self.signals.error.connect(self.errorDialog)
        self.signals.reset_buttons.connect(self.resetButtonState)

        # GUI fields update
        self.deviceVersion.currentTextChanged.connect(self.loadCapVisibility)
        self.testType.currentTextChanged.connect(self.testModeConfig)

    def updateFields(self):
        '''
        Updates GUI fields with static and initial information.
        '''
        self.getDebuggers()
        self.dongleFWVersionTask = gui_logic.DongleFWVersionTask()
        self.dongleFWVersionTask.start()
        self.deviceVersion.addItems(gui_logic.get_devices())
        self.rfTestVersion.setText(__main__.VERSION)
        self.femSettingsVisibility()
        self.loadCapVisibility(self.deviceVersion.currentText())
        self.testType.addItems(gui_logic.get_test_modes())
        self.dataRate.addItems(gui_logic.get_data_rates())
        self.outputPower.setText(str(DEFAULT_TX_POWER))
        self.firstChannel.setText(str(DEFAULT_FIRST_CHANNEL))
        self.lastChannel.setText(str(DEFAULT_LAST_CHANNEL))
        self.testModeConfig(self.testType.currentText())

    def getDevice(self):
        '''
        Gets the device version of the device connected to selected debugger.
        '''
        snr = self.debuggerSNR.currentText()
        if snr != '':
            gui_logic.detect_device(snr)

    def flashDevice(self):
        '''
        Programs the device with the test firmware and configures FEM pins and HFXO load capacitors if needed.
        '''
        self.flashButton.setStyleSheet("background-color: light gray")
        self.flashButton.setText("Flashing...")
        fem_config = None
        if self.FEM.isChecked():
            fem_config = {
                'pinTXEN': self.txEnPin.text(),
                'pinRXEN': self.rxEnPin.text(),
                'pinPDN': self.pdnPin.text(),
                'pinMODE': self.modePin.text(),
                'pinANTSEL': self.antSelPin.text(),
            }
        self.flasher_task = gui_logic.FlashFWTask(
            self.debuggerSNR.currentText(),
            self.loadCapacitor.text(),
            fem_config,
        )
        self.flasher_task.start()

    def recoverDevice(self):
        '''
        Recovers the device connected to the selected debugger.
        '''
        snr = self.debuggerSNR.currentText()
        if snr != '':
            self.recoverButton.setText('Recovering...')
            self.recoverTask = gui_logic.RecoverTask(snr)
            self.recoverTask.start()

    def getDebuggers(self):
        '''
        Gets the available debuggers.
        '''
        self.updateDebuggersTask = gui_logic.GetDebuggersTask()
        self.updateDebuggersTask.start()

    def updateRecoverButton(self):
        self.recoverButton.setText('Recover')

    def updateFlashButton(self, success: bool):
        self.flashButton.setText("Flash")
        if success:
            self.flashButton.setStyleSheet("background-color: green")
        else:
            self.flashButton.setStyleSheet("background-color: red")

    def updateStartButton(self, success: bool):
        if success:
            self.startButton.setStyleSheet("background-color: green")
        else:
            self.startButton.setStyleSheet("background-color: red")

    def updateDebuggers(self, debuggers: List[str]):
        self.debuggerSNR.clear()
        self.debuggerSNR.addItems(debuggers)

    def updateDevice(self, device):
        self.deviceVersion.setCurrentText(device)

    def updateDongleFWVersion(self, version):
        self.dongleFWVersion.setText(version)

    def startTest(self):
        '''
        Starts the RF test.
        '''
        radio_config = gui_logic.RadioConfig(
            first_channel=self.firstChannel.text(),
            last_channel=self.lastChannel.text(),
            radio_power=self.outputPower.text(),
            data_rate=self.dataRate.currentText(),
            rf_cmd=self.testType.currentText(),
            fem_config=self.modeSetting.value() + self.antSelSetting.value() * 2,
            usb_cmd=0x0B,
        )
        self.testTask = gui_logic.StartTestTask(radio_config)
        self.testTask.start()

    def run(self):
        self.show()
        self.qApp.exec()

    def femSettingsVisibility(self):
        '''
        Sets the visibility of the FEM settings.
        '''
        if self.FEM.isChecked():
            self.femPinWidget.setVisible(True)
            self.femSettingsWidget.setVisible(True)
        else:
            self.femPinWidget.setVisible(False)
            self.femSettingsWidget.setVisible(False)

    def loadCapVisibility(self, device: str):
        '''
        Sets the visibility of the HFXO load capacitor settings.
        '''

        if gui_logic.devices.get(device).get('load_cap'):
            self.loadCapacitorLabel.setVisible(True)
            self.loadCapacitor.setVisible(True)
        else:
            self.loadCapacitorLabel.setVisible(False)
            self.loadCapacitor.setVisible(False)

    def testModeConfig(self, mode: str):
        if 'sweep' in mode:
            self.lastChannel.setVisible(True)
            self.lastChannelLabel.setVisible(True)
            self.firstChannel.setText('2')
            self.firstChannelLabel.setText('Start Frequency')
        else:
            self.lastChannel.setVisible(False)
            self.lastChannelLabel.setVisible(False)
            self.firstChannelLabel.setText('Frequency')

        if 'Unmodulated' in mode and 'TX' in mode:
            self.dataRate.setVisible(False)
            self.dataRateLabel.setVisible(False)
        else:
            self.dataRate.setVisible(True)
            self.dataRateLabel.setVisible(True)

    def resetDevice(self):
        gui_logic.reset(self.debuggerSNR.currentText())

    def errorDialog(self, message: str):
        errorMsgBox = QMessageBox()
        errorMsgBox.setText(message)
        errorMsgBox.exec()

    def resetButtonState(self):
        self.flashButton.setStyleSheet("background-color: light gray")
        self.flashButton.setText("Flash")


class GUI:
    def __init__(self):
        self.qApp = QApplication()
        self.qApp.setStyle('Fusion')
        self.main_window = MainWindow(self.qApp)

    def run(self):
        self.main_window.run()
