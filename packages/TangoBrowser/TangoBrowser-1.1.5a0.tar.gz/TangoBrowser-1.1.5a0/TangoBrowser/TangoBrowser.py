import os
import sys
from subprocess import Popen
from threading import Thread

import tango.db
from taurus.external.qt import QtGui
from taurus.external.qt.QtGui import QApplication, QMessageBox
from fandango import get_device_info
from fandango.tango import get_alias_dict, get_matching_device_attribute_labels
from pyhdbpp import get_default_reader
from fandango import isDate, str2time, time2str
from .view import ArchivingBrowserView, TaurusTrend


class ArchivingBrowserController(ArchivingBrowserView):
    def __init__(self):
        super().__init__()
        self._is_manual_date_set = False
        self._subprocesses = []
        self._sub_trends = []

        self._environment = os.environ.copy()
        self._environment["CLASSPATH"] = (
            "/usr/share/java/JTango.jar:"
            "/usr/share/java/Jive.jar:"
            "/usr/share/java/ATKCore.jar:"
            "/usr/share/java/ATKWidget.jar"
        )
        self._environment["TANGO_HOST"] = "{}:{}".format(
            tango.db.Database().get_db_host(), tango.db.Database().get_db_port()
        )

        self.reader = get_default_reader()
        if self.reader is None:
            print("Pyhdbpp default reader could not be set")

        self._connect_actions()

    def _on_new_trend_clicked(self):
        trend = TaurusTrend()
        trend.showGrid(x=True, y=True, alpha=0.3)
        trend.show()

        self._sub_trends.append(trend)

    def _connect_actions(self):
        self.button_update.clicked.connect(self._perform_search)
        self.new_trend_button.clicked.connect(
            # lambda: self._launch_subprocess("taurus", ["trend"])
            self._on_new_trend_clicked
        )
        self.new_form_button.clicked.connect(
            lambda: self._launch_subprocess("taurus", ["form"])
        )
        self.refresh_button.clicked.connect(self._on_refresh_clicked)
        self.clear_button.clicked.connect(self.trend.getPlotItem().clear)

        self.lineEdit_attribute.returnPressed.connect(self._perform_search)
        self.lineEdit_device.returnPressed.connect(self._perform_search)
        self.lineEdit_start_date.editingFinished.connect(self._on_edited_text)
        self.lineEdit_start_date.returnPressed.connect(self._on_refresh_clicked)

        # Context menu
        self.test_action.triggered.connect(self._on_test_clicked)

        self.show_dev_info_action.triggered.connect(self._on_show_dev_info_clicked)

        self.trend_attribute_action.triggered.connect(self._on_trend_attribute_clicked)

        self.trend_selected_attributes_action.triggered.connect(
            self._on_trend_selected_attributes_clicked
        )

        self.form_attribute_action.triggered.connect(
            lambda: self._launch_subprocess(
                "taurus", ["form", self.selected_widget.custom_model]
            )
        )

        self.form_selected_attributes_action.triggered.connect(
            self._on_form_selected_attributes_clicked
        )

        self.select_all_attributes_action.triggered.connect(
            lambda: self._set_all_checkbox_states(state=True)
        )

        self.deselect_all_attributes_action.triggered.connect(
            lambda: self._set_all_checkbox_states(state=False)
        )

    def _launch_subprocess(self, command, args):
        cmd = Popen([command] + args, env=self._environment)
        self._subprocesses.append(cmd)

    def _on_test_clicked(self):
        model = self.selected_widget.custom_model
        if model.count("/") > 2:
            model = model.rsplit("/", 1)[0]

        self._launch_subprocess(
            "/usr/bin/java",
            [
                "-DTANGO_HOST={}".format(self._environment["TANGO_HOST"]),
                "jive.ExecDev",
                model,
            ],
        )

    def _on_show_dev_info_clicked(self):
        info = get_device_info(self.selected_widget.custom_model).items()
        QMessageBox.warning(
            self,
            "{} Info".format(self.selected_widget.custom_model),
            "\n".join("%s : %s" % i for i in info),
        )

    def _on_trend_attribute_clicked(self):
        self.trend.addModels(self.selected_widget.custom_model)
        models = self.tree_chooser.get_listed_models()

        if self.selected_widget.custom_model not in models:
            models.append(self.selected_widget.custom_model)
            self.tree_chooser.set_listed_models(models)

    def _on_trend_selected_attributes_clicked(self):
        model_list = self._get_selected_attributes()
        self.trend.addModels(model_list)

        models = self.tree_chooser.get_listed_models()

        for model in model_list:
            if model not in models:
                models.append(model)

        self.tree_chooser.set_listed_models(models)

    def _on_form_selected_attributes_clicked(self):
        arguments = ["form"] + list(self._get_selected_attributes())
        self._launch_subprocess("taurus", arguments)

    def _get_selected_attributes(self):
        model_list = set()
        for row in range(self.table_model.rowCount()):
            index = self.table_model.index(row, 0)
            if self.table.indexWidget(index).isChecked():
                model = self.table.indexWidget(index).custom_model
                model_list.add(model)

        return list(model_list)

    def _on_edited_text(self):
        self._is_manual_date_set = True

    def _on_refresh_clicked(self):
        display_range = abs(str2time(self.comboBox_range.currentText()))

        if self._is_manual_date_set and isDate(self.lineEdit_start_date.text()):
            start_date = str2time(self.lineEdit_start_date.text())
        else:
            start_date = str2time() - display_range
            self.lineEdit_start_date.setText(time2str(start_date))

        end_date = start_date + display_range

        self.trend.setXRange(min=start_date, max=end_date)

        self.trend._loadArchivingDataOnce()

    def _set_all_checkbox_states(self, state=False):
        for row in range(self.table_model.rowCount()):
            index = self.table_model.index(row, 5)
            self.table.indexWidget(index).setChecked(state)

    def _perform_search(self):
        device_query = self.lineEdit_device.text()
        device_query = "*" + device_query.replace(" ", "*") + "*"

        attribute_query = self.lineEdit_attribute.text()
        attribute_query = "*" + attribute_query.replace(" ", "*") + "*"

        attribute_list = set()
        threads = []

        if self.checkbox_cache.isChecked() and self.reader is not None:
            update_target = self.fill_with_archived_attrs

            # Append matches assuming that device_query is not an alias
            attribute_list.update(
                self.reader.get_attributes(
                    pattern="{}/{}".format(device_query, attribute_query)
                )
            )
        else:
            update_target = self.fill_with_device_attrs

            # Append matches assuming that device_query is not an alias
            try:
                attribute_list.update(
                    get_matching_device_attribute_labels(device_query, attribute_query)
                )
            except Exception as e:
                print("Get matching device attributes by label error ", e)

        if self.check_length_over_100(attribute_list):
            return

        # Append matches assuming that device_query is an alias.
        # This has to be done in threads since there may be a lot
        # of devices, and a wildcard search of devices to search for
        # attributes may be too time-consuming in a non-concurrent way.
        alias_dict = get_alias_dict(device_query).items()
        if len(alias_dict) > 0 and update_target:
            for _, device in get_alias_dict(device_query).items():
                thread = Thread(
                    target=update_target, args=(device, attribute_list, attribute_query)
                )
                thread.start()
                threads.append(thread)

            # Wait for all threads to finish
            [thread.join() for thread in threads]

        if not self.check_length_over_100(attribute_list):
            self.populate_table(sorted(attribute_list))

    def check_length_over_100(self, attribute_list):
        if len(attribute_list) > 100:
            QMessageBox.warning(
                self,
                "Too much attributes",
                "Your query retrieves more than "
                "100 attributes, please try to be more "
                "specific",
            )
            return True

        return False

    @staticmethod
    def fill_with_device_attrs(device, attribute_list, attribute_query):
        try:
            attribute_list.update(
                get_matching_device_attribute_labels(device, attribute_query)
            )
        except:
            # Ignore not exported devices and devices with errors
            pass

    def fill_with_archived_attrs(self, device, attribute_list, attribute_query):
        try:
            attribute_list.update(
                self.reader.get_attributes(
                    pattern="{}/{}".format(device, attribute_query)
                )
            )
        except:
            # Ignore not exported devices and devices with errors
            pass

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        for process in self._subprocesses:
            process.terminate()
        super().closeEvent(a0)


def main():
    argv = sys.argv
    if "--help" in argv or "-h" in argv:
        print(
            """
        To open the GUI just type tango_browser.
        
        Usage for export data to csv (Using hdb2csv from pyhdbpp):
            tango_browser --export [--options] attribute1 attribute2 date1 date2 /.../filename.cvs"
            Available options for extraction are:"
                --schema="database" : choose database to extract the data'
                --arrsep=""/--no-sep : default separator between arrays values'
                --sep : separator between columns'
                --linesep : character between lines'
                --resolution=X(s) : force periodicity of values to a fix period'
                --list : list available schemas for attributes'
                --nofill : do not fill gaps using last values'
                --noheader : do not include headers'
                --nodate : do not include datetime'
                --noepoch : do not include epochs'
            
            Example for exporting: tango_browser --export sr/di/dcct/averagecurrent 
            "2023-12-10 00:00" "2023-12-10 22:00" filename.csv'
        """
        )

    if "--export" in argv or "-e" in argv:
        from subprocess import call

        print(["hdb2csv"] + argv[2:])
        try:
            call(["hdb2csv"] + argv[2:])
        except:
            print(
                "hdb2csv module not found, please update"
                " pyhdbpp to a newer version (>=1.5.0)"
            )
    else:
        app = QApplication(sys.argv)
        view = ArchivingBrowserController()
        app.exec_()


if __name__ == "__main__":
    main()
