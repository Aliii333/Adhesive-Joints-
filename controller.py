from HartSmith import HartSmith
from Volkersen import volkersen
from Goland import Goland
from failureMode import failureMode
from interface import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from graphOutput import graphOutput
from adhesive import adhesive
from adherend import adherend
from numpy import arange
import threading
import concurrent.futures
import sys

"""
import PyQt5
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
"""


class controller:
    def __init__(self):
        self.dljActive = False
        self.sljActive = False
        self.tubeActive = False
        self.stringEmpty = False
        self.Hartsmith = HartSmith
        self.Volkersen = volkersen
        self.failure = failureMode
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.startUi()

    def startUi(self):
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.setWindowTitle("Adhesive Joint Strength Prediction")
        self.MainWindow.show()

        # Remove these values upon completion - they are for testing only
        self.ui.Image.setPixmap(QtGui.QPixmap("SingleLappedJointHart-SmithSmallest.png"))
        self.sljActive = True
        self.ui.LoadLineEdit.setText("1000")
        self.ui.AdModLineEdit.setText("70")
        self.ui.TopAdThickLineEdit.setText("1.62")
        self.ui.BaseAdThickLineEdit.setText("1.62")
        self.ui.PRatioLineEdit.setText("0.4")
        self.ui.OverlapLengthLineEdit.setText("12.7")
        self.ui.AdhesiveThickLineEdit.setText("0.25")
        self.ui.AdShearModLineEdit.setText("4.82")
        self.ui.JointWidthLineEdit.setText("25.4")
        self.ui.AdhesiveYieldStressLineEdit.setText("49")
        self.ui.SubstrateShearYieldStressLineEdit.setText("0")
        self.ui.SubstrateYieldStressLineEdit.setText("0")
        self.ui.Substrate2ndYieldStressLineEdit.setText("0")

        # Connects the buttons to functions within controller
        self.ui.HartSmithPushButton.setEnabled(False)
        self.ui.VolkersenPushButton.setEnabled(False)
        self.ui.SolveButton.clicked.connect(self.on_solveClick)
        self.ui.ClearButton.clicked.connect(self.on_clearClick)
        self.ui.HartSmithPushButton.clicked.connect(self.on_graphClickHartSmith)
        self.ui.VolkersenPushButton.clicked.connect(self.on_graphClickVolkersen)

        self.ui.actionAV119_3.triggered.connect(self.on_AV119Click)
        self.ui.actionRedux326.triggered.connect(self.on_Redux326Click)
        self.ui.actionHysol19321.triggered.connect(self.on_Hysol19321Click)
        self.ui.actionCustom_Adhesive_2.triggered.connect(self.on_CustomAdhesive)

        self.ui.actionMildSteel.triggered.connect(self.on_MildSteelClick)
        self.ui.actionHighStrengthSteel.triggered.connect(self.on_HighStrengthSteelClick)
        self.ui.actionAluminium.triggered.connect(self.on_AluminiumClick)
        self.ui.actionCarbonFiber.triggered.connect(self.on_CarbonFiberClick)
        self.ui.actionCustom_Adherend_2.triggered.connect(self.on_CustomAdherend)

        self.ui.actionSingle_Lapped_Joint_3.triggered.connect(self.on_SLJClick)
        self.ui.actionDouble_Lapped_Joint_2.triggered.connect(self.on_DLJClick)
        self.ui.VonMises.triggered.connect(self.on_VonMises)
        self.ui.DruckerPrager.triggered.connect(self.on_DrukcerPrager)
        self.ui.TsaiWu.triggered.connect(self.on_TsaiWu)


        # kills program on exit
        sys.exit(self.app.exec_())

    def validationEmpty(self, valueCheck):
        if valueCheck == "":
            self.stringEmpty = True
        else:
            return float(valueCheck)

    def on_solveClick(self):
        # validates each input
        load = self.validationEmpty(self.ui.LoadLineEdit.text())
        adMod = self.validationEmpty(self.ui.AdModLineEdit.text())
        TopAdThick = self.validationEmpty(self.ui.TopAdThickLineEdit.text())
        BaseAdThick = self.validationEmpty(self.ui.BaseAdThickLineEdit.text())
        pRatio = self.validationEmpty(self.ui.PRatioLineEdit.text())
        overlapLength = self.validationEmpty(self.ui.OverlapLengthLineEdit.text())
        AdhesiveThickness = self.validationEmpty(self.ui.AdhesiveThickLineEdit.text())
        AdShearMod = self.validationEmpty(self.ui.AdShearModLineEdit.text())
        jointWidth = self.validationEmpty(self.ui.JointWidthLineEdit.text())
        GAdherend = self.validationEmpty(self.ui.AdherendShearModulusLineEdit.text())
        GAdhesive = self.validationEmpty(self.ui.AdhesiveShearModulusLineEdit.text())
        AdhesiveYieldStrength = self.validationEmpty(self.ui.AdhesiveYieldStrengthLineEdit.text())
        ThroughThinckness =  self.validationEmpty(self.ui.ThroughThincknessLineEdit.text())
        InterlaminarShearStrength =  self.validationEmpty(self.ui.InterlaminarShearStrengthLineEdit.text())

        # Yield stresses
        adhesiveYieldStress = self.validationEmpty(self.ui.AdhesiveYieldStressLineEdit.text())
        substrateShearYieldStress = self.validationEmpty(self.ui.SubstrateShearYieldStressLineEdit.text())
        substrateYieldStress = self.validationEmpty(self.ui.SubstrateYieldStressLineEdit.text())
        substrate2ndYieldStress = self.validationEmpty(self.ui.Substrate2ndYieldStressLineEdit.text())



        if not self.stringEmpty:
            # Determines if the active joint is single or double lapped
            if self.sljActive:
                # Initialises the Hart-Smith and Volkersen classes
                self.Hartsmith = HartSmith(load, adMod, TopAdThick, pRatio, overlapLength, AdhesiveThickness,
                                           AdShearMod,
                                           jointWidth, adhesiveYieldStress)
                self.Volkersen = volkersen(load, jointWidth, pRatio, AdShearMod, TopAdThick, BaseAdThick, adMod,
                                           AdhesiveThickness,
                                           overlapLength, adhesiveYieldStress)
                self.Goland = Goland(load, adMod, TopAdThick, pRatio, overlapLength, AdhesiveThickness,
                                           AdShearMod,
                                           jointWidth, adhesiveYieldStress, 1,AdhesiveYieldStrength, substrateShearYieldStress)
                self.ui.HartSmithPushButton.setEnabled(True)

                # Calculates the stress; shear and normal
                self.Hartsmith.shearstress()
                self.Hartsmith.tensilestress()
                #Sets the max stress and fos
                self.ui.MaxStressHartSmithLineEdit.setText("{0:.3f}".format(self.Hartsmith.maximumValue()))
                self.ui.FactorofSafetyHartSmithLabel.setText("{0:.3f}".format(self.Hartsmith.maximumValueTensile()))

                self.ui.MaxStressGolandLineEdit.setText("{0:.3f}".format(self.Goland.Pa()))
                self.ui.FactorofSafetyGoland.setText("{0:.3f}".format(self.Goland.Ps()))
                #Replace the function below with the failure class
                self.failure = failureMode(self.Hartsmith.maximumValue(), self.Hartsmith.maximumValueTensile(), adMod,
                                           AdShearMod, GAdhesive, GAdherend, substrateShearYieldStress, AdhesiveYieldStrength,
                                           ThroughThinckness, InterlaminarShearStrength)
                self.ui.FailureMode1LineEdit.setText("{0:.3f}".format(self.failure.vonMises()))
                self.ui.FailureMode2LineEdit.setText("{0:.3f}".format(self.failure.DruckerPrager()))
                self.ui.FailureMode3LineEdit.setText("{0:.3f}".format(self.failure.TsaiWu()))
                self.ui.InformationBox.setText(self.failure.failureCheck("choose"))

            elif self.dljActive:
                # Since DLJ then the overlap length and joint width are doubled
                overlapLength *= 2
                jointWidth *= 2

                # Initialises the volkersen class
                self.Volkersen = volkersen(load, jointWidth, pRatio, AdShearMod, TopAdThick, BaseAdThick, adMod,
                                           AdhesiveThickness,
                                           overlapLength, adhesiveYieldStress)

                # Disables the Hart-Smith push button therefore disabling the graph output
                self.ui.HartSmithPushButton.setEnabled(False)

                # Sets the max stress and fos text fields
                self.ui.MaxStressHartSmithLineEdit.setText("Not Available")
                self.ui.FactorofSafetyHartSmithLabel.setText("Not Available")

            if self.ui.homogenousRadioButton.isChecked() or (adhesiveYieldStress <= substrateYieldStress):
                # Calculates the volkersen shear stress
                self.Volkersen.shearstress()
                self.ui.VolkersenPushButton.setEnabled(True)

                # Sets the values of the max stress and FoS Volkersen
                self.ui.MaxStressVolkersenLineEdit.setText("{0:.3f}".format(self.Volkersen.maximumValue()))

                # Need to replace the inputs below
                #volkersenFail = self.failure.failCheck()[1]
                #self.ui.FactorofSafetyLineEdit.setText(
                #    "{0:.3f}".format(volkersenFail))
                #self.ui.InformationBox.setText(self.failure.failCheck()[-1])
            else:
                self.ui.MaxStressVolkersenLineEdit.setText("Not Available")
                self.ui.FactorofSafetyLineEdit.setText("Not Available")
                self.ui.VolkersenPushButton.setEnabled(False)

        else:
            error = QtWidgets.QMessageBox()
            error.setIcon(QtWidgets.QMessageBox.Warning)
            error.setText("Fields must not be left blank")
            error.setWindowTitle("Input Error")
            error.exec_()
            self.stringEmpty = False

    def on_clearClick(self):
        # TODO: Add all the line edits to this
        self.ui.LoadLineEdit.clear()
        self.ui.AdModLineEdit.clear()
        self.ui.TopAdThickLineEdit.clear()
        self.ui.BaseAdThickLineEdit.clear()
        self.ui.PRatioLineEdit.clear()
        self.ui.OverlapLengthLineEdit.clear()
        self.ui.AdhesiveThickLineEdit.clear()
        self.ui.AdShearModLineEdit.clear()
        self.ui.JointWidthLineEdit.clear()
        self.ui.AdhesiveYieldStressLineEdit.clear()
        self.ui.SubstrateShearYieldStressLineEdit.clear()
        self.ui.SubstrateYieldStressLineEdit.clear()
        self.ui.Substrate2ndYieldStressLineEdit.clear()
        self.ui.AdhesiveShearModulusLineEdit.clear()
        self.ui.AdherendShearModulusLineEdit.clear()
        self.ui.AdhesiveYieldStrengthLineEdit.clear()
        self.ui.ThroughThincknessLineEdit.clear()
        self.ui.InterlaminarShearStrengthLineEdit.clear()

        # Disables the Hart-Smith and Volkersen buttons
        self.ui.HartSmithPushButton.setEnabled(False)
        self.ui.VolkersenPushButton.setEnabled(False)

        # Empties the shear stress of both classes
        self.Hartsmith.shear = []
        self.Hartsmith.tensile = []
        self.Volkersen.shear = []

    def on_graphClickHartSmith(self):
        graph = graphOutput(self.Hartsmith)
        graph.outputGraph()

    def on_graphClickVolkersen(self):
        graph = graphOutput(self.Volkersen)
        graph.outputGraph()

    def on_AV119Click(self):
        getAdhesiveName = self.ui.actionAV119_3.text()
        ad = adhesive(getAdhesiveName)
        adhesiveValues = ad.readFile()  # AdhesiveValues is a list containing 4 data values [adName, adMod, pRatio,
        # maxShearStress]
        self.ui.AdShearModLineEdit.setText(adhesiveValues[1])
        self.ui.PRatioLineEdit.setText(adhesiveValues[2])
        self.ui.AdhesiveYieldStressLineEdit.setText(adhesiveValues[3])
        self.ui.AdhesiveShearModulusLineEdit.setText(adhesiveValues[4])
        self.ui.AdhesiveYieldStrengthLineEdit.setText(adhesiveValues[5])
        self.ui.AdShearModLineEdit.setEnabled(False)
        self.ui.PRatioLineEdit.setEnabled(False)
        self.ui.AdhesiveYieldStressLineEdit.setEnabled(False)
        self.ui.AdhesiveShearModulusLineEdit.setEnabled(False)
        self.ui.AdhesiveYieldStrengthLineEdit.setEnabled(False)

    def on_Redux326Click(self):
        getAdhesiveName = self.ui.actionRedux326.text()
        ad = adhesive(getAdhesiveName)
        adhesiveValues = ad.readFile()  # AdhesiveValues is a list containing 4 data values [adName, adMod, pRatio,
        # maxShearStress]
        self.ui.AdShearModLineEdit.setText(adhesiveValues[1])
        self.ui.PRatioLineEdit.setText(adhesiveValues[2])
        self.ui.AdhesiveYieldStressLineEdit.setText(adhesiveValues[3])
        self.ui.AdShearModLineEdit.setEnabled(False)
        self.ui.PRatioLineEdit.setEnabled(False)
        self.ui.AdhesiveYieldStressLineEdit.setEnabled(False)
        self.ui.AdhesiveYieldStressLineEdit.setText(adhesiveValues[3])
        self.ui.AdhesiveShearModulusLineEdit.setText(adhesiveValues[4])
        self.ui.AdhesiveYieldStrengthLineEdit.setText(adhesiveValues[5])
        self.ui.AdhesiveYieldStressLineEdit.setEnabled(False)
        self.ui.AdhesiveShearModulusLineEdit.setEnabled(False)
        self.ui.AdhesiveYieldStrengthLineEdit.setEnabled(False)


    def on_Hysol19321Click(self):
        getAdhesiveName = self.ui.actionHysol19321.text()
        ad = adhesive(getAdhesiveName)
        adhesiveValues = ad.readFile()  # AdhesiveValues is a list containing 4 data values [adName, adMod, pRatio,
        # maxShearStress]
        self.ui.AdShearModLineEdit.setText(adhesiveValues[1])
        self.ui.PRatioLineEdit.setText(adhesiveValues[2])
        self.ui.AdhesiveYieldStressLineEdit.setText(adhesiveValues[3])
        self.ui.AdShearModLineEdit.setEnabled(False)
        self.ui.PRatioLineEdit.setEnabled(False)
        self.ui.AdhesiveYieldStressLineEdit.setEnabled(False)
        self.ui.AdhesiveYieldStressLineEdit.setText(adhesiveValues[3])
        self.ui.AdhesiveShearModulusLineEdit.setText(adhesiveValues[4])
        self.ui.AdhesiveYieldStrengthLineEdit.setText(adhesiveValues[5])
        self.ui.AdhesiveYieldStressLineEdit.setEnabled(False)
        self.ui.AdhesiveShearModulusLineEdit.setEnabled(False)
        self.ui.AdhesiveYieldStrengthLineEdit.setEnabled(False)


    def on_MildSteelClick(self):
        getAdherendName = self.ui.actionMildSteel.text()
        ad = adherend(getAdherendName)
        adherendValues = ad.readFile()
        self.ui.AdModLineEdit.setText(adherendValues[1])
        self.ui.SubstrateShearYieldStressLineEdit.setText(adherendValues[2])
        self.ui.AdModLineEdit.setEnabled(False)
        self.ui.SubstrateShearYieldStressLineEdit.setEnabled(False)
        self.ui.AdherendShearModulusLineEdit.setText(adherendValues[3])
        self.ui.AdherendShearModulusLineEdit.setEnabled(False)
        self.ui.ThroughThincknessLineEdit.setText(adherendValues[4])
        self.ui.ThroughThincknessLineEdit.setEnabled(False)
        self.ui.InterlaminarShearStrengthLineEdit.setText(adherendValues[5])
        self.ui.InterlaminarShearStrengthLineEdit.setEnabled(False)


    def on_HighStrengthSteelClick(self):
        getAdherendName = self.ui.actionHighStrengthSteel.text()
        ad = adherend(getAdherendName)
        adherendValues = ad.readFile()
        self.ui.AdModLineEdit.setText(adherendValues[1])
        self.ui.SubstrateShearYieldStressLineEdit.setText(adherendValues[2])
        self.ui.AdModLineEdit.setEnabled(False)
        self.ui.SubstrateShearYieldStressLineEdit.setEnabled(False)
        self.ui.AdherendShearModulusLineEdit.setText(adherendValues[3])
        self.ui.AdherendShearModulusLineEdit.setEnabled(False)
        self.ui.ThroughThincknessLineEdit.setText(adherendValues[4])
        self.ui.ThroughThincknessLineEdit.setEnabled(False)
        self.ui.InterlaminarShearStrengthLineEdit.setText(adherendValues[5])
        self.ui.InterlaminarShearStrengthLineEdit.setEnabled(False)


    def on_AluminiumClick(self):
        getAdherendName = self.ui.actionAluminium.text()
        ad = adherend(getAdherendName)
        adherendValues = ad.readFile()
        self.ui.AdModLineEdit.setText(adherendValues[1])
        self.ui.SubstrateShearYieldStressLineEdit.setText(adherendValues[2])
        self.ui.AdModLineEdit.setEnabled(False)
        self.ui.SubstrateShearYieldStressLineEdit.setEnabled(False)
        self.ui.AdherendShearModulusLineEdit.setText(adherendValues[3])
        self.ui.AdherendShearModulusLineEdit.setEnabled(False)
        self.ui.ThroughThincknessLineEdit.setText(adherendValues[4])
        self.ui.ThroughThincknessLineEdit.setEnabled(False)
        self.ui.InterlaminarShearStrengthLineEdit.setText(adherendValues[5])
        self.ui.InterlaminarShearStrengthLineEdit.setEnabled(False)


    # SHEHAB
    def on_CarbonFiberClick(self):
        getAdherendName = self.ui.actionCarbonFiber.text()
        ad = adherend(getAdherendName)
        adherendValues = ad.readFile()
        self.ui.AdModLineEdit.setText(adherendValues[1])
        self.ui.SubstrateShearYieldStressLineEdit.setText(adherendValues[2])
        self.ui.AdModLineEdit.setEnabled(False)
        self.ui.SubstrateShearYieldStressLineEdit.setEnabled(False)
        self.ui.AdherendShearModulusLineEdit.setText(adherendValues[3])
        self.ui.AdherendShearModulusLineEdit.setEnabled(False)
        self.ui.ThroughThincknessLineEdit.setText(adherendValues[4])
        self.ui.ThroughThincknessLineEdit.setEnabled(False)
        self.ui.InterlaminarShearStrengthLineEdit.setText(adherendValues[5])
        self.ui.InterlaminarShearStrengthLineEdit.setEnabled(False)

    def on_CustomAdhesive(self):
        self.ui.AdShearModLineEdit.setEnabled(True)
        self.ui.PRatioLineEdit.setEnabled(True)
        self.ui.AdhesiveYieldStressLineEdit.setEnabled(True)
        self.ui.AdhesiveShearModulusLineEdit.setEnabled(True)
        self.ui.AdhesiveYieldStrengthLineEdit.setEnabled(True)


    def on_CustomAdherend(self):
        self.ui.AdModLineEdit.setEnabled(True)
        self.ui.SubstrateShearYieldStressLineEdit.setEnabled(True)
        self.ui.AdherendShearModulusLineEdit.setEnabled(True)
        self.ui.ThroughThincknessLineEdit.setEnabled(True)
        self.ui.InterlaminarShearStrengthLineEdit.setEnabled(True)

    def on_SLJClick(self):
        self.dljActive = False
        self.sljActive = True
        self.ui.HartSmithPushButton.setEnabled(True)
        self.ui.Image.setPixmap(QtGui.QPixmap("SingleLappedJointHart-SmithSmallest.png"))

    def on_DLJClick(self):
        self.dljActive = True
        self.sljActive = False
        self.ui.HartSmithPushButton.setEnabled(False)
        self.ui.Image.setPixmap(QtGui.QPixmap("DoubleLappedJointHart-SmithSmallest.png"))

    def on_VonMises(self):
        self.ui.InformationBox.setText(self.failure.failureCheck("VonMises"))
    def on_DrukcerPrager(self):
        self.ui.InformationBox.setText(self.failure.failureCheck("DruckerPrager"))
    def on_TsaiWu(self):
        self.ui.InformationBox.setText(self.failure.failureCheck("TsaiWu"))


if __name__ == '__main__':
    controller = controller()
    controller.startUi()
