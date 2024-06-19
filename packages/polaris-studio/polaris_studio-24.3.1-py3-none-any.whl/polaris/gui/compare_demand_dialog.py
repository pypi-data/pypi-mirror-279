from pathlib import Path
from typing import Dict

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QGroupBox, QWidget
from PyQt5.QtWidgets import QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem

import matplotlib.pyplot as plt
import pandas as pd
import tables
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from polaris.runs.run_utils import get_output_dirs
from polaris.utils.database.db_utils import read_and_close, get_schema
from .chart_availability import available_charts
from .plots.bar_chart import bar_chart
from .plots.distribution_rolling_average import start_distribution_chart
from .plots.tfld import tfld
from .utils.field_filter_config import FieldFilterConfig
from .utils.range_slider import RangeSlider


class CompareDemandDialog(QWidget):
    def __init__(self, qgis_project=None, polaris_project=None):
        QWidget.__init__(self)
        if qgis_project:
            self.iface = qgis_project.iface
        self.qgis_project = qgis_project
        self.polaris_project = polaris_project or qgis_project.polaris_project

        self.figure = plt.figure()
        self.__iterations_exist = []
        self.data = {table: {} for table in available_charts.keys()}
        self.__field_config = {}
        self.filters = {}
        topFrameLayout = QHBoxLayout()

        # Adds the list of iterations to the top left of the tool screen
        self.__build_iterations_table()
        topFrameLayout.addWidget(self.iterations)

        # Middle controls
        topFrameMiddle = self.__builds_mid_top_controls()
        topFrameLayout.addWidget(topFrameMiddle)
        self.demand_tables.currentIndexChanged.connect(self.__populate_available_table_fields)

        self.filter_frame = QGroupBox("Filters")
        filter_layout = QHBoxLayout()
        self.table_fields = self.__build_table_widget(header="Fields to filter", values=[])
        self.table_fields.setColumnWidth(0, 160)
        self.table_fields.setFixedWidth(180)

        filter_layout.addWidget(self.table_fields)

        self.filter_frame.setLayout(filter_layout)

        topFrameLayout.addWidget(self.filter_frame)
        self.table_fields.itemSelectionChanged.connect(self.__builds_filter_controls)

        topFrame = QFrame()
        topFrame.setLayout(topFrameLayout)

        layout = QVBoxLayout()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton("Plot")
        self.button.clicked.connect(self.plot)

        layout.addWidget(topFrame)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.__populate_available_table_fields()

        self.setWindowTitle("Plot demand data")

    def plot(self):
        self.button.setEnabled(False)
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        table = self.demand_tables.currentText()
        chart_name = self.chart_types.currentText()
        data = self.get_data(table, self.__selected_iterations())
        data = self.__filter_data(data)

        if chart_name == "Start time distribution":
            start_distribution_chart(data, ax, table)
        elif chart_name == "Bar":
            bar_chart(data, ax, self.barchart_field.currentText(), table)
        elif chart_name == "Trip-Length Distribution":
            tfld(data, ax, table)
        else:
            raise AttributeError("Chart type is unknown")

        # refresh canvas
        self.canvas.draw()
        self.button.setEnabled(True)

    def get_data(self, tbl_name, iterations):
        return_data = {}
        for iter_name in iterations:
            path = self.proj_root / self.demfile if iter_name == "root" else self.proj_root / iter_name / self.demfile
            if iter_name not in self.data[tbl_name]:
                h5pth = self.proj_root / "gui.cache.h5"  # type:Path
                hdf5_node = f"/{iter_name}/{tbl_name}"
                data = pd.DataFrame([])
                if h5pth.exists():
                    with tables.open_file(h5pth, "r") as h5file:
                        if h5file.root.__contains__(hdf5_node):
                            data = pd.read_hdf(h5pth, hdf5_node)
                            self.data[tbl_name][iter_name] = data
                if not data.shape[0]:
                    with read_and_close(path) as conn:
                        data = pd.read_sql(f"Select * from {tbl_name}", conn)
                    data.to_hdf(path_or_buf=h5pth, key=hdf5_node, complevel=3)
                    self.data[tbl_name][iter_name] = data

            dt = self.data[tbl_name][iter_name]
            return_data[iter_name] = dt
        return return_data

    def __iteration_exists(self, iteration_name):
        path = (
            self.proj_root / self.demfile
            if iteration_name == "root"
            else self.proj_root / iteration_name / self.demfile
        )
        return path.exists()

    def __filter_data(self, data: Dict[str, pd.DataFrame]):
        table = self.demand_tables.currentText()
        for k, df in data.items():
            for variable, widget in self.filters.items():
                if isinstance(widget, QTableWidget):
                    lst = self.__selected_in_table(widget)
                    if len(lst) > 0:
                        field_schema = self.__field_config[table][variable].field_type
                        if field_schema.type in ["INTEGER"]:
                            lst = [int(x) for x in lst]
                        df = df[df[variable].isin(lst)]
                elif isinstance(widget, RangeSlider):
                    if widget.low() > widget._minval:
                        df = df[df[variable] >= widget.low()]
                    if widget.high() > widget._maxval:
                        df = df[df[variable] <= widget.high()]
                else:
                    raise ValueError("I do not know this filter type")

            data[k] = df
        return data

    def __selected_iterations(self):
        return self.__selected_in_table(self.iterations)

    def __selected_in_table(self, table: QTableWidget):
        sel = table.selectedItems()
        if not sel:
            return []
        rows = [s.row() for s in sel if s.column() == 0]
        return [table.item(i, 0).text() for i in rows]  # type: ignore

    def __build_iterations_table(self):
        config = self.polaris_project.run_config
        config.data_dir = self.polaris_project.model_path
        self.__iterations_exist = ["root"] + sorted([str(x.name) for x in get_output_dirs(config)])
        self.__iterations_exist = [x for x in self.__iterations_exist if self.__iteration_exists(x)]

        self.iterations = self.__build_table_widget(header="Iterations", values=self.__iterations_exist)
        if len(self.__iterations_exist) > 0:
            self.iterations.selectRow(0)
        self.iterations.setColumnWidth(0, 220)
        self.iterations.setFixedWidth(240)
        return self.iterations

    def __builds_mid_top_controls(self):
        middle_top_layout = QGridLayout()
        # List of tables we can plot
        self.demand_tables = QComboBox()
        self.demand_tables.addItems(sorted(self.data.keys()))
        middle_top_layout.addWidget(QLabel(text="Table"))
        middle_top_layout.addWidget(self.demand_tables)
        # Types of charts we can make
        self.chart_types = QComboBox()
        self.chart_types.addItems(available_charts["Trip"])
        self.chart_types.currentIndexChanged.connect(self.__change_chart_type)
        middle_top_layout.addWidget(QLabel(text="Chart type"))
        middle_top_layout.addWidget(self.chart_types)

        # Field to create the bar chart by
        self.barchart_field = QComboBox()
        self.barchart_field.clear()
        self.__lbl_barchart = QLabel(text="Bar Chart field")
        self.barchart_field.setVisible(False)
        self.__lbl_barchart.setVisible(False)
        middle_top_layout.addWidget(self.__lbl_barchart)
        middle_top_layout.addWidget(self.barchart_field)

        topFrameMiddle = QFrame()
        topFrameMiddle.setLayout(middle_top_layout)
        return topFrameMiddle

    def __change_chart_type(self):
        self.barchart_field.setVisible(self.chart_types.currentText() == "Bar")
        self.__lbl_barchart.setVisible(self.chart_types.currentText() == "Bar")
        if self.chart_types.currentText() == "Bar":
            self.__populate_available_table_fields()

    def __builds_filter_controls(self):
        self.filters.clear()

        # Clears frame
        filter_layout = self.filter_frame.layout()
        for i in range(filter_layout.count() - 1, 0, -1):
            filter_layout.itemAt(i).widget().setParent(None)

        sel = self.table_fields.selectedItems()

        if not sel:
            self.adjustSize()
            return

        rows = [s.row() for s in sel if s.column() == 0]
        filter_fields = [self.table_fields.item(i, 0).text() for i in rows]

        self.__get_field_stats()

        table = self.demand_tables.currentText()
        if table not in self.__field_config:
            return

        df = list(self.get_data(table, [self.__reference_iteration]).values())[0]

        for fld in filter_fields:
            widget = None
            ffconfig = self.__field_config[table][fld]  # type: FieldFilterConfig
            ffconfig.populate(df)

            if len(ffconfig.values) > 0:
                widget = self.__build_table_widget(header=f"{fld} values", values=ffconfig.values)
                widget.setColumnWidth(0, 140)
                widget.setFixedWidth(160)
                self.filters[fld] = widget
            else:
                minval, maxval = ffconfig.min_val, ffconfig.max_val
                if None not in [minval, maxval]:
                    widget = self.__build_range_slider(fld, minval, maxval)

            if widget is not None:
                filter_layout.addWidget(widget)

        self.table_fields.setColumnWidth(0, 160)
        self.filter_frame.setLayout(filter_layout)
        self.adjustSize()

    def __populate_available_table_fields(self):
        self.__get_field_stats()

        table = self.demand_tables.currentText()
        if table not in self.__field_config:
            return

        fields = []
        df = list(self.get_data(table, [self.__reference_iteration]).values())[0]
        for fld, ffconfig in self.__field_config[table].items():  # type: str, FieldFilterConfig
            if self.chart_types.currentText() == "Bar":
                ffconfig.populate(df)
            if len(ffconfig.values) > 0:
                fields.append(fld)

        # List of tables we can plot
        self.barchart_field.clear()
        if self.chart_types.currentText() == "Bar":
            self.barchart_field.addItems(sorted(fields))

        self.table_fields.setRowCount(len(self.__field_config[table]))

        for i, fld in enumerate(self.__field_config[table].keys()):
            self.table_fields.setItem(i, 0, QTableWidgetItem(str(fld)))
        self.table_fields.clearSelection()

    def __get_field_stats(self):
        table = self.demand_tables.currentText()
        if table in self.__field_config:
            return

        if not self.__reference_file.exists():
            return

        table = self.demand_tables.currentText()
        with read_and_close(self.__reference_file) as conn:
            db_schema = get_schema(conn, table)

            for fld, field in db_schema.items():
                self.__field_config[table] = self.__field_config.get(table, {})
                self.__field_config[table][fld] = FieldFilterConfig(field_type=field, values=[], table=table)

    @property
    def __reference_file(self) -> Path:
        reference_file = self.proj_root / self.demfile
        if not reference_file.exists():
            iter_name = self.__selected_iterations()
            if len(iter_name) != 0:
                reference_file = (
                    reference_file if iter_name[0] == "root" else self.proj_root / iter_name[0] / self.demfile
                )
        return reference_file

    @property
    def __reference_iteration(self) -> str:
        iter_name = self.__selected_iterations()
        if len(iter_name) != 0:
            return iter_name[0]
        else:
            return self.__iterations_exist[0]

    def __build_table_widget(self, header, values) -> QTableWidget:
        widget = QTableWidget()
        widget.setColumnCount(1)
        widget.setHorizontalHeaderLabels([header])
        widget.setRowCount(0)
        if len(values):
            widget.setRowCount(len(values))

        for i, val in enumerate(values):
            widget.setItem(i, 0, QTableWidgetItem(str(val)))

        f = QFont()
        f.setPointSize(12)
        widget.setFont(f)
        return widget

    def __build_range_slider(self, variable_name: str, minval: float, maxval: float):
        lbl = QLabel(variable_name)

        label = QLabel(f"{minval} - {maxval}")
        slider = RangeSlider(minval=minval, maxval=maxval, label=label)
        slider.update_label()
        slider.sliderMoved.connect(slider.update_label)
        self.filters[variable_name] = slider

        frame = QFrame()
        layout = QVBoxLayout()
        layout.addWidget(lbl)
        layout.addWidget(slider)
        layout.addWidget(label)
        frame.setLayout(layout)
        return frame

    @property
    def demfile(self) -> str:
        return str(self.polaris_project.demand_file.name)

    @property
    def proj_root(self):
        return self.polaris_project.model_path

    def exit_procedure(self):
        self.close()
