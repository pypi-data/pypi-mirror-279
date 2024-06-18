import sys
import os
import Orange
import Orange.data
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output

from PyQt5.QtWidgets import (
    QTableWidgetItem, QTableWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QLineEdit, QPushButton, QWidget
)
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import uic, QtWidgets
from AnyQt.QtCore import Qt

class TableEditor(widget.OWWidget):
    name = "Table Editor -- 2"
    description = "Editing table element, returning the datatable edited"
    icon = "icons/table_editor.png"

    dossier_du_script = os.path.dirname(os.path.abspath(__file__))
    input_data = None

    class Inputs:
        input_data = Input("Data", Orange.data.Table)

    class Outputs:
        data_out = Output("Data", Orange.data.Table)

    @Inputs.input_data
    def set_data(self, input_data):
        self.input_data = input_data

        # Imprimer les informations sur les données
        if input_data:
            # Remplir la table avec les données
            self.fill_table()

    def __init__(self):
        super().__init__()
        self.init_Ui()

    def init_Ui(self):
        # QT Management
        uic.loadUi(self.dossier_du_script + '/widget_designer/table_editor.ui', self)

        self.table_widget = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.reset_button = self.findChild(QtWidgets.QPushButton, 'reset')
        self.validate_button = self.findChild(QtWidgets.QPushButton, 'validate')

        # Ajuster automatiquement la taille de la table pour afficher toutes les lignes et colonnes
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

        self.reset_button.clicked.connect(self.reset_table)
        self.validate_button.clicked.connect(self.save_and_send)

    def reset_table(self):
        # Réinitialiser la table avec les données initiales
        self.fill_table()

    def fill_table(self):
        # Vérifier si des données sont disponibles
        if self.input_data:
            # Effacer toutes les données précédentes dans la table
            self.table_widget.clear()

            # Obtenir le domaine (noms de colonnes)
            domain = self.input_data.domain
            column_names = [attr.name for attr in domain.attributes]
            meta_names = [meta.name for meta in domain.metas]

            # Obtenir les données (valeurs des instances) et les méta-données
            data = self.input_data.X
            metas = self.input_data.metas

            # Définir le nombre de lignes et de colonnes
            num_rows = len(data)
            num_cols = len(column_names) + len(meta_names)

            # Définir le nombre de colonnes dans la table
            self.table_widget.setColumnCount(num_cols)
            self.table_widget.setRowCount(num_rows)

            # Définir les noms de colonnes dans la table
            self.table_widget.setHorizontalHeaderLabels(column_names + meta_names)

            # Ajouter les données dans la table
            for row_index, row_data in enumerate(data):
                for col_index, value in enumerate(row_data):
                    if isinstance(domain.attributes[col_index], Orange.data.DiscreteVariable):
                        combobox = QComboBox()
                        values = domain.attributes[col_index].values
                        combobox.addItems(values)
                        combobox.setCurrentText(str(value))
                        self.table_widget.setCellWidget(row_index, col_index, combobox)
                    elif isinstance(domain.attributes[col_index], Orange.data.ContinuousVariable):
                        line_edit = QLineEdit(str(value))
                        validator = QDoubleValidator()
                        line_edit.setValidator(validator)
                        self.table_widget.setCellWidget(row_index, col_index, line_edit)
                    else:
                        item = QTableWidgetItem(str(value))
                        self.table_widget.setItem(row_index, col_index, item)

            # Ajouter les méta-données dans la table
            for row_index, row_data in enumerate(metas):
                for meta_index, value in enumerate(row_data):
                    col_index = len(column_names) + meta_index
                    if isinstance(domain.metas[meta_index], Orange.data.DiscreteVariable):
                        combobox = QComboBox()
                        values = sorted(set(self.input_data[:, domain.metas[meta_index]].metas[:, meta_index]))
                        combobox.addItems(map(str, values))
                        combobox.setCurrentText(str(value))
                        self.table_widget.setCellWidget(row_index, col_index, combobox)
                    else:
                        item = QTableWidgetItem(str(value))
                        self.table_widget.setItem(row_index, col_index, item)

    def on_accepted(self):
        # Gérer l'acceptation de la boîte de dialogue si nécessaire
        pass

    def get_edited_data(self):
        edited_data = []

        for i in range(self.table_widget.rowCount()):
            row = []
            for j in range(self.table_widget.columnCount()):
                cell_widget = self.table_widget.cellWidget(i, j)
                if cell_widget and isinstance(cell_widget, QComboBox):
                    row.append(cell_widget.currentText())
                elif cell_widget and isinstance(cell_widget, QLineEdit):
                    row.append(cell_widget.text())
                else:
                    item = self.table_widget.item(i, j)
                    if item is not None:
                        row.append(item.text())
                    else:
                        row.append('')
            edited_data.append(row)
        return edited_data

    def save_and_send(self):
        edited_data = self.get_edited_data()
        # Récupérer les noms de domaine de la table d'origine
        original_domain = self.input_data.domain
        attribute_names = [attr.name for attr in original_domain.attributes]
        meta_names = [meta.name for meta in original_domain.metas]
        attributes = []

        for column_idx, attribute_name in enumerate(attribute_names):
            values = set(row[column_idx] for row in edited_data)
            try:
                values = {float(values) for values in values}
                variable = Orange.data.ContinuousVariable(attribute_name)
            except ValueError:
                variable = Orange.data.DiscreteVariable(attribute_name, values=list(values))

            attributes.append(variable)

        domain = Orange.data.Domain(attributes, metas=[Orange.data.StringVariable(meta) for meta in meta_names])
        data = Orange.data.Table(domain, edited_data)
        self.Outputs.data_out.send(data)

if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication

    app = QApplication(sys.argv)
    table_editor = TableEditor()

    table_editor.show()

    app.exec_()
