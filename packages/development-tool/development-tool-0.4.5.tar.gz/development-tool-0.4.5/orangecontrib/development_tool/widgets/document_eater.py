import os
import sys
import Orange.data
import numpy as np
import pandas as pd
from Orange.data.pandas_compat import table_from_frame, table_to_frame
from PyQt5 import uic, QtWidgets
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output
from AnyQt.QtCore import Qt, QObject, pyqtSignal

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from sentence_transformers import SentenceTransformer
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QPushButton
from PyQt5 import QtCore
import copy
from Orange.data import Domain, StringVariable, ContinuousVariable, Table
from PyQt5.QtCore import QThread, pyqtSignal

from PyQt5.QtWidgets import QComboBox, QProgressBar
class DocumentEater(widget.OWWidget):
    name = "DocumentEater"
    description = "Documents ingestion to generate embeddings and store it in db and add it to input file"
    icon = "icons/data-integration.png"
    want_control_area = False

    dossier_du_script = os.path.dirname(os.path.abspath(__file__))
    input_data = None
    working_dir = os.path.dirname(os.path.abspath(__file__) + '/tests/')
    model_dir = os.path.join(working_dir, "Models")
    data_dir = os.path.join(working_dir, "Data")
    db_dir = os.path.join(data_dir, "db")

    auto_send = False  # Variable de classe pour suivre l'état de la case à cocher
    model_name = None
    dataChanged = pyqtSignal()

    embeddings_generated = False

    progressBar = None

    class Inputs:
        input_data = Input("Data", Orange.data.Table)

    class Outputs:
        data_out = Output("Data", Orange.data.Table)

    @Inputs.input_data
    def set_data(self, input_data):
        self.input_data = input_data
        print("new input data")
        if self.auto_send:  # Si auto_send est activé
            self.generate_embeddings()  # Appeler generate_embeddings automatiquement

        # Réinitialise la barre de progression à 0 si input_data est None
        if input_data is None:
                self.progressBar.setValue(0)


        # Mettre à jour la combobox avec les noms des colonnes de métadonnées
        if input_data is not None:
            meta_columns = [var.name for var in input_data.domain.metas]
            self.metaComboBox.clear()
            self.metaComboBox.addItems(meta_columns)
            # Sélectionne la colonne "content" par défaut si elle existe, sinon sélectionne la première colonne disponible
            default_column_index = meta_columns.index("content") if "content" in meta_columns else 0
            self.metaComboBox.setCurrentIndex(default_column_index)

    def __init__(self):
        super().__init__()

        self.setFixedWidth(470)
        self.setFixedHeight(300)

        self.embeddings_generated = False
        # QT Management
        uic.loadUi(self.dossier_du_script + '/widget_designer/document_eater.ui', self)

        self.selectFolderButton = self.findChild(QPushButton, 'push')
        # Connexion du clic du bouton à la méthode pour ouvrir le sélecteur de fichier
        self.selectFolderButton.clicked.connect(self.select_folder)

        self.generate = self.findChild(QPushButton, 'generate')
        self.generate.clicked.connect(self.generate_embeddings)

        self.modelPathLabel = self.findChild(QtWidgets.QLabel,
                                             'label')  # Récupérer le QLabel à partir du fichier .ui
        self.modelPathLabel.setText("Model Folder Path: Not selected")  # Définir le texte initial

        self.generateCheckBox = self.findChild(QtWidgets.QCheckBox,
                                               'checkBox')  # Récupérer le QCheckBox à partir du fichier .ui
        self.generateCheckBox.stateChanged.connect(self.toggle_auto_send)  # Connecter le signal stateChanged
        self.generate.setEnabled(not self.generateCheckBox.isChecked())  # Désactiver le bouton de génération

        # Ajoute cette ligne dans ta méthode __init__ après avoir chargé le fichier UI
        self.metaComboBox = self.findChild(QComboBox, 'comboBox')

        # Initialise la barre de progression à 0%
        self.progressBar.setValue(0)

    def toggle_auto_send(self, state):
        self.auto_send = state == QtCore.Qt.Checked
        if self.auto_send and self.input_data is not None:
            # Vérifie si les embeddings ont déjà été générés
            if not self.embeddings_generated:
                self.generate_embeddings()
        else:
            # Si auto_send est désactivé ou s'il n'y a pas de données d'entrée, réinitialise la barre de progression à 0
            self.progressBar.setValue(0)

    def select_folder(self):
        # Ouvrir la boîte de dialogue pour sélectionner un dossier
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        # Si un dossier a été sélectionné
        if folder_path:
            # Récupérer la liste des fichiers dans le dossier
            files = os.listdir(folder_path)
            # Vérifier s'il y a des fichiers dans le dossier
            if files:
                # Sélectionner le premier fichier dans la liste (peu importe lequel)
                file_name = files[0]
                # Construire le chemin complet du fichier en utilisant le chemin du dossier et le nom du fichier
                model_name = os.path.join(folder_path, file_name)
                # Mettre à jour self.model_name avec le chemin complet du fichier
                self.model_name = folder_path
                self.label.setText(f"Model Folder Path: {folder_path}")
            else:
                print("Le dossier sélectionné est vide.")
        else:
            print("Aucun dossier sélectionné.")

    def generate_embeddings(self):
        try:
            if self.input_data is None:
                out_data = None
            else:
                # Initialisation du modèle Sentence Transformers
                model_name = getattr(self, 'model_name', None)
                if model_name is None:
                    model_name = "all-MiniLM-L6-v2"
                    print("Using default model:", model_name)

                model = SentenceTransformer(model_name)

                # Copy of input data
                data = copy.deepcopy(self.input_data)
                attr_dom = list(data.domain.attributes)
                metas_dom = list(data.domain.metas)

                # Initialisation du modèle Sentence Transformers
                selected_column_index = self.metaComboBox.currentIndex()
                selected_column_name = self.input_data.domain.metas[selected_column_index].name

                print("col name:", selected_column_name)
                # Initialize progress bar
                self.progressBar.setMaximum(len(data))
                self.progressBar.setValue(0)

                embeddings = []

                for i, row in enumerate(data):
                    # Update progress bar value
                    self.progressBar.setValue(i + 1)
                    # Generate embeddings for the current row
                    embeddings.append(model.encode(str(row[selected_column_name])))
                # Create new metas domains for embeddings

                #embeddings = [model.encode(str(row["content"])) for row in data]
                n_columns = len(embeddings[0])
                new_metas_dom = [ContinuousVariable("embedding" + f"_{selected_column_name}" + f"_{i}") for i in range(n_columns)]

                # Create the new updated Domain
                domain = Domain(attr_dom, metas=metas_dom + new_metas_dom)
                rows = []

                n = len(data)
                for i in range(n):
                    features = list(data[i])

                    metas = list(data.metas[i])
                    metas += list(embeddings[i])
                    rows.append(features + metas)

                out_data = Table.from_list(domain, rows=rows)
                # Met à jour le statut embeddings_generated à True après avoir généré les embeddings avec succès
                self.embeddings_generated = True
            self.Outputs.data_out.send(out_data)
        except Exception as e:
            print("An error occurred during embeddings processing:", str(e))

    def load_input_data(self):
        print("self.data", self.input_data.domain)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            self.refresh_all()

        return super().eventFilter(source, event)

    def show_warning_box(self, title: str, text: str):
        # Afficher une boîte de dialogue indiquant que les colonnes nécessaires sont manquantes
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

    def refresh_all(self):
        self.load_input_data()
        print("is it called ?")


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication

    app = QApplication(sys.argv)
    mon_objet = DocumentEater()
    mon_objet.show()

    app.exec_()
