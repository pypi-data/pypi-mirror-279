import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from Orange.widgets import widget

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\","/"):
    from Orange.widgets.orangecontrib.AAIT.utils.MetManagement import get_ia_store_requirements_json, GetFromRemote
    from Orange.widgets.orangecontrib.AAIT.utils import shared_functions,example_workflows
else:
    from orangecontrib.AAIT.utils.MetManagement import get_ia_store_requirements_json, GetFromRemote
    from orangecontrib.AAIT.utils import shared_functions,example_workflows


class OWLoadWorkflow(widget.OWWidget):
    name = "Load workflows"
    description = "Template workflow for different subjects"
    icon = "icons/documents.png"
    priority = 10
    # Chemin du répertoire du script
    dossier_du_script = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()
        self.requirements = get_ia_store_requirements_json()

        # Gestion de l'UI
        self.initUI()


    def initUI(self):
        # Charger l'interface utilisateur à partir du fichier .ui créé avec Qt Designer
        loadUi(os.path.join(self.dossier_du_script, 'designer/load_workflow.ui'), self)

        # Récupérer la ComboBox
        self.comboBox = self.findChild(QtWidgets.QComboBox, 'comboBox')
        # Connecter le signal currentIndexChanged de la ComboBox au slot handleComboBoxChange
        self.comboBox.currentIndexChanged.connect(self.handleComboBoxChange)
        # Récupérer le bouton "Save As"
        self.saveButton = self.findChild(QtWidgets.QPushButton, 'save')
        # Connecter le signal clicked du bouton au slot saveFile
        self.saveButton.clicked.connect(self.saveFile)
        # Récupérer le QTextEdit pour afficher la description
        self.descriptionTextEdit = self.findChild(QtWidgets.QTextEdit, 'descriptionTextEdit')
        # Remplir la ComboBox avec les noms de fichiers OWS du dossier
        self.populate_combo_box()


        self.test_test=self.findChild(QtWidgets.QPushButton, 'test_test')
        self.test_test.clicked.connect(self.test_ia_store)

    def test_ia_store(self):
        print("kjakjhdkqs")
        """
        Browse a collection of tutorial/example schemes.

        Returns QDialog.Rejected if the user canceled the dialog else loads
        the selected scheme into the canvas and returns QDialog.Accepted.
        """
        example_workflows.show_example_worklow(self,"IA Store")



    def populate_combo_box(self):
        workflows = []
        descriptions = dict()
        for element in self.requirements:
            workflows.append(element["name"])
            descriptions[element["name"]] = element["description"][0]
        self.descriptions = descriptions
        self.comboBox.addItems(workflows)

    def handleComboBoxChange(self, index):
        # Gérer le changement de sélection dans la ComboBox
        selected_file = self.comboBox.itemText(index)
        # Afficher la description dans le QTextEdit
        self.descriptionTextEdit.setPlainText(self.descriptions[selected_file])

    def read_description(self, file_name):
        # Chemin du fichier texte contenant la description
        description_file_path = os.path.join(self.dossier_du_script, 'ows_example', f'{os.path.splitext(file_name)[0]}.txt')
        # Lire le contenu du fichier s'il existe, sinon retourner une chaîne vide
        if os.path.exists(description_file_path):
            with open(description_file_path, 'r') as file:
                description = file.read()
        else:
            description = ""
        return description

    def saveFile(self):
        # Méthode pour sauvegarder le fichier sélectionné dans un nouvel emplacement
        selected_file = self.comboBox.currentText()
        GetFromRemote(selected_file)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = OWLoadWorkflow()
    window.show()
    app.exec_()
