import traceback

from fandango import get_device
from taurus.external.qt.Qt import Qt
from taurus.external.qt.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QLabel,
    QApplication,
    QMainWindow,
    QDockWidget,
    QComboBox,
    QWidget,
    QMenu,
    QAbstractItemView,
    QLineEdit,
    QCheckBox,
    QTableView,
    QPushButton,
    QAction,
    QVBoxLayout,
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
    QTabWidget,
)
from fandango.qt import Draggable
from taurus.qt.qtgui.display import TaurusLabel
from taurus.core.tango.util import tangoFormatter
from taurus_pyqtgraph import TaurusTrend
import pyqtgraph as pg
from .history import show_history
from .TreeUtility.ModelChooser import TaurusModelChooser


class ArchivingBrowserView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_menu = QTabWidget()
        self.tab_menu.setTabPosition(self.tab_menu.North)

        # Create the necessary widgets
        self.label0 = QLabel(
            "Enter Device and Attribute filters using wildcards"
            "(e.g. li/ct/plc[0-9]+ / ^stat*$ & !status) and press enter"
            "or click the 'Update' button"
        )
        self.device_or_alias_label = QLabel("Device or Alias:")
        self.lineEdit_device = QLineEdit()
        self.attribute_label = QLabel("Attribute:")
        self.lineEdit_attribute = QLineEdit()
        self.lineEdit_start_date = QLineEdit("YYYY/MM/DD HH:MM:SS")
        # self.lineEdit_start_date.text = "YYYY/MM/DD HH:MM:SS"
        self.lineEdit_start_date.setMinimumSize(200, 25)
        self.lineEdit_start_date.setMaximumSize(200, 25)
        self.button_update = QPushButton("Update")
        self.button_plot = QPushButton("Plot")
        self.new_trend_button = QPushButton("New Trend")
        self.new_trend_button.setMaximumSize(100, 25)
        self.new_trend_button.setMinimumSize(100, 25)
        self.new_form_button = QPushButton("New Form")
        self.new_form_button.setMaximumSize(100, 25)
        self.new_form_button.setMinimumSize(100, 25)
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setMaximumSize(100, 25)
        self.refresh_button.setMinimumSize(100, 25)
        self.clear_button = QPushButton("Clear plot")
        self.clear_button.setMaximumSize(100, 25)
        self.clear_button.setMinimumSize(100, 25)
        self.checkbox_cache = QCheckBox("Archived attributes search")
        self.drag_and_drop_label = QLabel(
            "If drag&drop fails, please use 'right-click' and select the "
            "desired option from the contextual menu. Multiple selection "
            "available with checkboxes from the right."
        )
        self.start_date_label = QLabel("Start date:")
        self.start_date_label.setMaximumSize(100, 25)
        self.start_date_label.setMinimumSize(100, 25)
        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")
        self.trend = TaurusTrend()
        self.trend.showGrid(x=True, y=True, alpha=0.3)
        self.comboBox_range = QComboBox()
        self.comboBox_range.setMinimumSize(70, 25)
        self.comboBox_range.setMaximumSize(70, 25)
        self.comboBox_range.addItem("1m")
        self.comboBox_range.addItem("5m")
        self.comboBox_range.addItem("30m")
        self.comboBox_range.addItem("1h")
        self.comboBox_range.addItem("12h")
        self.comboBox_range.addItem("1d")
        self.comboBox_range.addItem("1w")
        self.comboBox_range.addItem("1y")
        self.comboBox_range.setEditable(True)

        # Create the table with the necessary columns
        self.table = QTableView()
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(25)
        self.table_model = QStandardItemModel()
        self.table.setModel(self.table_model)
        self.selected_widget = None

        # Create a header view and set it on the table
        self.header = QHeaderView(Qt.Horizontal)
        self.table.setHorizontalHeader(self.header)

        # Set the table to allow selection of multiple rows
        self.table.setSelectionMode(QAbstractItemView.NoSelection)

        # Add columns to the table model
        self.table_model.setColumnCount(6)
        self.table_model.setHorizontalHeaderLabels(
            ["", "Device", "Alias", "Attribute", "label/value", "Archiving", "Plot"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Create the vertical layout and add the widgets and table
        layout = QVBoxLayout()
        layout.addWidget(self.label0)
        layout_fields = QHBoxLayout()
        layout_fields.addWidget(self.device_or_alias_label)
        layout_fields.addWidget(self.lineEdit_device)
        layout_fields.addWidget(self.attribute_label)
        layout_fields.addWidget(self.lineEdit_attribute)
        layout_fields.addWidget(self.checkbox_cache)
        layout_fields.addWidget(self.button_update)
        layout.addLayout(layout_fields)
        layout.addWidget(self.table)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.drag_and_drop_label)
        layout.addLayout(horizontal_layout)

        dockable_bottom = QDockWidget()
        bottom_content = QWidget()
        bottom_content_layout = QVBoxLayout()
        bottom_content_layout.addWidget(self.trend)

        horizontal_bottom_layout = QHBoxLayout()

        horizontal_bottom_layout.setAlignment(Qt.AlignLeft)
        horizontal_bottom_layout.addWidget(self.start_date_label)
        horizontal_bottom_layout.addWidget(self.lineEdit_start_date)
        horizontal_bottom_layout.addWidget(self.comboBox_range)
        horizontal_bottom_layout.addWidget(self.refresh_button)
        horizontal_bottom_layout.addWidget(self.clear_button)
        right_buttons_layout = QHBoxLayout()
        right_buttons_layout.setAlignment(Qt.AlignRight)
        right_buttons_layout.addWidget(self.new_trend_button)
        right_buttons_layout.addWidget(self.new_form_button)
        horizontal_bottom_layout.addLayout(right_buttons_layout)

        bottom_content_layout.addLayout(horizontal_bottom_layout)
        bottom_content.setLayout(bottom_content_layout)

        dockable_bottom.setWidget(bottom_content)

        # Add the layout to the main window
        main_widget = QWidget()
        main_widget.setMinimumSize(1200, 300)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, dockable_bottom)

        self.contextual_menu = QMenu(self)
        self._populate_contextual_menu()

        self.tree_chooser = TaurusModelChooser(parent=self.tab_menu)
        self.tab_menu.addTab(main_widget, "Search")
        self.tab_menu.addTab(self.tree_chooser, "Tree")
        self.setCentralWidget(self.tab_menu)

        self.tree_chooser.updateModels.connect(self.trend.addModels)

        # Set window properties
        self.setWindowTitle("Tango Browser")

        self.show()

    def _populate_contextual_menu(self):
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

        self.test_action = QAction("Test Device", self)
        self.show_dev_info_action = QAction("Show Device Info", self)
        self.trend_attribute_action = QAction("Trend attribute", self)
        self.trend_selected_attributes_action = QAction(
            "Trend selected attributes", self
        )
        self.form_attribute_action = QAction("Create form with attribute", self)
        self.form_selected_attributes_action = QAction(
            "Create form with selected attributes", self
        )
        self.select_all_attributes_action = QAction("Select all attributes", self)
        self.deselect_all_attributes_action = QAction("Deselect all attributes", self)

        self.contextual_menu.addAction(self.test_action)
        self.contextual_menu.addAction(self.show_dev_info_action)
        self.contextual_menu.addAction(self.trend_attribute_action)
        self.contextual_menu.addAction(self.trend_selected_attributes_action)
        self.contextual_menu.addAction(self.form_attribute_action)
        self.contextual_menu.addAction(self.form_selected_attributes_action)
        self.contextual_menu.addAction(self.select_all_attributes_action)
        self.contextual_menu.addAction(self.deselect_all_attributes_action)

    def populate_table(self, attribute_list):
        """
        Populates a custom TableView using a list of attributes
        :param attribute_list: list of attributes
        :return:
        """
        self.table_model.setRowCount(0)  # Clear previous data

        for row, attribute in enumerate(attribute_list):
            device = get_device(attribute)
            self._add_table_item(row, device, attribute)

        # Resize columns to fit the content
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _on_drag_event(self, attribute):
        models = self.tree_chooser.get_listed_models()

        if attribute not in models:
            models.append(attribute)

        self.tree_chooser.set_listed_models(models)
        return attribute

    def _add_table_item(self, row, device, attribute):
        try:
            alias = device.alias()
        except:
            alias = ""

        self.table_model.appendRow(
            [
                QStandardItem(),
                QStandardItem(),
                QStandardItem(),
                QStandardItem(),
                QStandardItem(),
                QStandardItem(),
                QStandardItem(),
            ]
        )

        attribute_name = attribute.split("/")[-1]

        check = QCheckBox()
        check.custom_model = attribute
        index = self.table_model.index(row, 0)
        self.table.setIndexWidget(index, check)

        qlabel_device_name = Draggable(QLabel)()
        qlabel_device_name.setText(device.dev_name())
        qlabel_device_name.custom_model = attribute
        qlabel_device_name.setDragEventCallback(lambda: self._on_drag_event(attribute))

        index = self.table_model.index(row, 1)
        self.table.setIndexWidget(index, qlabel_device_name)

        alias_draggable = Draggable(QLabel)()
        alias_draggable.setText(alias)
        alias_draggable.custom_model = attribute
        alias_draggable.setDragEventCallback(lambda: self._on_drag_event(attribute))

        index = self.table_model.index(row, 2)
        self.table.setIndexWidget(index, alias_draggable)

        attribute_draggable = Draggable(QLabel)()
        attribute_draggable.setText(attribute_name)
        attribute_draggable.custom_model = attribute
        attribute_draggable.setDragEventCallback(lambda: self._on_drag_event(attribute))

        index = self.table_model.index(row, 3)
        self.table.setIndexWidget(index, attribute_draggable)

        taurus_widget = TaurusLabel()
        taurus_widget.setModel(attribute)
        taurus_widget.setFormat(tangoFormatter())
        taurus_widget.custom_model = attribute

        index = self.table_model.index(row, 4)
        self.table.setIndexWidget(index, taurus_widget)

        archiving_button = QPushButton("Archiving")
        archiving_button.clicked.connect(
            lambda: self.on_show_archiving_modes(attribute)
        )
        archiving_button.custom_model = attribute

        index = self.table_model.index(row, 5)
        self.table.setIndexWidget(index, archiving_button)

        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(lambda: self._on_plot_button_clicked(attribute))
        plot_button.custom_model = attribute

        index = self.table_model.index(row, 6)
        self.table.setIndexWidget(index, plot_button)

    def _on_plot_button_clicked(self, attribute):
        models = self.tree_chooser.get_listed_models()

        if attribute not in models:
            models.append(attribute)
            self.tree_chooser.set_listed_models(models)

        self.trend.addModels(attribute)

    def show_context_menu(self, pos):
        index = self.table.indexAt(pos)

        if index.isValid():
            self.selected_widget = self.table.indexWidget(index)
            self.contextual_menu.exec_(self.table.mapToGlobal(pos))

    def on_show_archiving_modes(self, model=None):
        try:
            model = model or self.selected_widget.custom_model
            show_history(model)
        except:
            QMessageBox.warning(self, "ups!", traceback.format_exc())


if __name__ == "__main__":
    app = QApplication([])
    view = ArchivingBrowserView()
    app.exec_()
