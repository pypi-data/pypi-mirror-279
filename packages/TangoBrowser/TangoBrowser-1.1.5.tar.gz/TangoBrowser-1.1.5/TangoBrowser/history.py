from taurus.external.qt import Qt

from fandango import now, Object, time2str, str2time
from fandango.qt import QOptionDialog
import fandango
import traceback
import time
import re
import pickle
import os
from pyhdbpp import get_default_reader

try:
    from pyhdbpp.utils import export_to_text
except:
    print(
        "Deprecation warning: export_to_text will be removed from this "
        "package in the future, please upgrade to pyhdbpp >= 1.5.0"
    )
    # FIXME: Remove this compatibility when pyhdbpp >= 1.5.0
    backwards_export_to_text = True

tformat = "%Y-%m-%d %H:%M:%S"

TABS = []


def state_formatter(value):
    try:
        n = int(float(value))
        state = fandango.tango.DevState.values[n]
        return "%s (%s)" % (value, state)
    except:
        return str(value)


def get_value_formatter(attribute):
    formatter = str
    try:
        # ai = fandango.tango.get_attribute_config(attribute)
        d, a = attribute.rsplit("/", 1)
        ai = fandango.get_device(d).get_attribute_config(a)
        # print(attribute,':',ai)
        if ai.data_type is fandango.tango.CmdArgType.DevState:
            formatter = state_formatter
        # else:
        # print(repr(ai.datatype))
    except:
        traceback.print_exc()
    return formatter


def get_data_filename(var, data=None, fileformat="pck", dateformat="epoch"):
    fname = var.replace("/", ".")
    if data is not None and len(data):
        if dateformat == "epoch" or True:
            date = "%d-%d" % (int(data[0][0]), int(data[-1][0]))
        elif dateformat == "human":
            time2human = lambda t: re.sub("[^0-9]", "", time2str(t))
            date = "%s-%s" % (time2human(data[0][0]), time2human(data[-1][0]))
        fname += "--%s" % date
    fname += "." + fileformat
    return fname


def save_data_file(
    var, data, filename="", folder="", format="pck", **kwargs
):  # format in 'pck' or 'csv'
    """
    This method will be use to export archived data to 'csv' or 'pck' formats.
    Kwargs can be used to pass arguments to Reader.export_to_text
    """
    path = folder + "/" + (filename or get_data_filename(var, data, format))
    kwargs = kwargs or {"arrsep": " "}
    print("Saving %d registers to %s ..." % (len(data), path))
    if format == "csv":
        # FIXME: Remove this compatibility when pyhdbpp >= 1.5.0 is released
        if backwards_export_to_text:
            text = export_to_text_backwards({var: data}, **kwargs)
        else:
            text = export_to_text({var: data}, **kwargs)
        open(path, "w").write(text)
    else:
        pickle.dump(data, open(path, "w"))
    return path


# FIXME: Remove this method when pyhdbpp >= 1.5.0 is released
def export_to_text_backwards(table, order=None, **kwargs):
    """
    It will convert a [(timestamp,value)] array in a CSV-like text.
    Order will be used to set the order to data columns (date and timestamp will be always first and second).

    Other parameters are available:

      sep : character to split values in each row
      arrsep : character to split array values in a data column
      linesep : characters to insert between lines

    """
    sep = kwargs.get("sep", "\t").decode()
    arrsep = kwargs.get("arrsep", kwargs.get("separator", ", ")).decode()
    linesep = kwargs.get("linesep", "\n").decode()

    start = time.time()
    if not hasattr(table, "keys"):
        table = {"attribute": table}
    if not order or not all(k in order for k in table):
        keys = list(sorted(table.keys()))
    else:
        keys = sorted(list(table.keys()), key=order.index)

    csv = sep.join(["date", "time"] + keys) + linesep

    def value_to_text(s):
        v = (
            str(s) if not fandango.isSequence(s) else arrsep.join(map(str, s))
        ).replace("None", "")
        return v

    time_to_text = lambda t: (
        time2str(t, cad="%Y-%m-%d_%H:%M:%S") + ("%0.3f" % (t % 1)).lstrip("0")
    )  # taurustrend timestamp format

    ml = min(len(v) for v in list(table.values()))
    for i in range(ml):  # len(table.values()[0])):
        csv += sep.join(
            [
                time_to_text(list(table.values())[0][i][0]),
                str(list(table.values())[0][i][0]),
            ]
            + [value_to_text(table[k][i][1]) for k in keys]
        )
        csv += linesep

    print(("Text file generated in %d milliseconds" % (1000 * (time.time() - start))))
    return csv


class ShowHistoryDialog(Object):
    DefaultStart = 0
    DefaultEnd = 0

    @classmethod
    def get_default_dates(klass):
        return klass.DefaultStart or now() - 3600, klass.DefaultEnd or now()

    @classmethod
    def set_default_dates(klass, start, end):
        klass.DefaultStart = start
        klass.DefaultEnd = end

    @staticmethod
    def setup_table(attribute, start, stop, values):
        print("drawing table from %d values: %s ..." % (len(values), values[:2]))
        twi = Qt.QWidget()
        twi.setLayout(Qt.QVBoxLayout())
        tab = Qt.QTableWidget()
        tab.setWindowTitle("%s: %s to %s" % (attribute, start, stop))
        twi.setWindowTitle("%s: %s to %s" % (attribute, start, stop))
        tab.setRowCount(len(values))
        tab.setColumnCount(3)
        tab.setHorizontalHeaderLabels(["TIME", "EPOCH", "VALUE"])

        formatter = get_value_formatter(attribute)

        for i, tup in enumerate(values):
            date, value = tup[:2]
            qdate = Qt.QTableWidgetItem(time2str(date))
            qdate.setTextAlignment(Qt.Qt.AlignRight)
            tab.setItem(i, 0, qdate)
            qtime = Qt.QTableWidgetItem(str(date))
            qtime.setTextAlignment(Qt.Qt.AlignRight)
            tab.setItem(i, 1, qtime)
            qvalue = Qt.QTableWidgetItem(formatter(value))
            qvalue.setTextAlignment(Qt.Qt.AlignRight)
            tab.setItem(i, 2, qvalue)

        twi.layout().addWidget(tab)
        tab.resizeColumnsToContents()
        tab.horizontalHeader().setStretchLastSection(True)
        return twi

    @classmethod
    def show_new_dialog(klass, attribute, schema="*", parent=None, dates=[]):
        try:
            if not Qt.QApplication.instance():
                Qt.QApplication([])
        except:
            pass
        print("in Vacca.widgets.show_history(%s)")

        print("getting archiving readers ...")

        rd = get_default_reader()
        attribute = str(attribute).lower()

        try:
            dates = dates or klass.get_default_dates()
            if not all(map(fandango.isString, dates)):
                dates = list(map(time2str, dates))
        except:
            traceback.print_exc()
            dates = time2str(), time2str()

        is_attribute_archived = rd.is_attribute_archived(attribute)
        if is_attribute_archived:
            print("%s is being archived" % attribute)
            di = Qt.QDialog(parent)
            wi = di  # QtGui.QWidget(di)
            wi.setLayout(Qt.QGridLayout())
            begin = Qt.QLineEdit()
            begin.setText(dates[0])
            end = Qt.QLineEdit()
            end.setText(dates[1])
            tfilter = Qt.QLineEdit()
            vfilter = Qt.QCheckBox()
            wi.setWindowTitle("Show %s Archiving" % attribute)
            wil = wi.layout()
            wi.layout().addWidget(Qt.QLabel(attribute), 0, 0, 1, 2)
            wi.layout().addWidget(Qt.QLabel("Preferred Schema"), 1, 0, 1, 1)
            qschema = Qt.QComboBox()
            qschema.insertItems(0, ["*"])
            wil.addWidget(qschema, 1, 1, 1, 1)
            wil.addWidget(
                Qt.QLabel("Enter Begin and End dates in %s format" % tformat),
                2,
                0,
                1,
                2,
            )
            wil.addWidget(Qt.QLabel("Begin:"), 3, 0, 1, 1)
            wil.addWidget(begin, 3, 1, 1, 1)
            wil.addWidget(Qt.QLabel("End:"), 4, 0, 1, 1)
            wil.addWidget(end, 4, 1, 1, 1)
            wil.addWidget(Qt.QLabel("Time Filter:"), 5, 0, 1, 1)
            wil.addWidget(tfilter, 5, 1, 1, 1)
            wil.addWidget(Qt.QLabel("Value Filter:"), 6, 0, 1, 1)
            wil.addWidget(vfilter, 6, 1, 1, 1)
            buttons = Qt.QDialogButtonBox(wi)
            buttons.addButton(Qt.QPushButton("Export"), Qt.QDialogButtonBox.AcceptRole)

            bt = Qt.QPushButton("Apply")
            buttons.addButton(bt, Qt.QDialogButtonBox.ApplyRole)

            buttons.addButton(Qt.QPushButton("Close"), Qt.QDialogButtonBox.RejectRole)

            buttons.accepted.connect(wi.accept)
            buttons.rejected.connect(wi.reject)
            wi.layout().addWidget(buttons, 7, 0, 1, 2)

            def check_values():
                di.exec_()
                if di.result():
                    print("checking result ...")
                    try:
                        start, stop = str(begin.text()), str(end.text())
                        try:
                            tf = int(str(tfilter.text()))
                        except:
                            tf = 0
                        vf = vfilter.isChecked()
                        if not all(
                            re.match(
                                "[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+",
                                str(s).strip(),
                            )
                            for s in (start, stop)
                        ):
                            print("dates are wrong ...")
                            Qt.QMessageBox.warning(
                                None,
                                "Show archiving",
                                "Dates seem not in %s format" % (tformat),
                                Qt.QMessageBox.Ok,
                            )
                            return check_values()
                        else:
                            print("getting values ...")
                            print("using default reader")
                            values = rd.get_attribute_values(attribute, start, stop)
                            if not len(values) and rd.is_attribute_archived(
                                attribute, active=True
                            ):
                                print(
                                    "Attribute {} is archived but no data "
                                    "has been fetch, check archiving reader "
                                    "{}".format(attribute, rd)
                                )
                                return
                            if vf:
                                values = fandango.arrays.decimate_array(values)
                            if tf:
                                print("Filtering %d values (1/%dT)" % (len(values), tf))
                                values = fandango.arrays.filter_array(
                                    values, window=tf
                                )  # ,begin=start,end=stop)

                            twi = klass.setup_table(attribute, start, stop, values)
                            klass.set_default_dates(str2time(start), str2time(stop))

                            button = Qt.QPushButton("Save to file")
                            button2 = Qt.QPushButton("Send to email")

                            # button.setTextAlignment(Qt.Qt.AlignCenter)
                            button.pressed.connect(
                                lambda: save_to_file(attribute, values, twi, False)
                            )

                            twi.layout().addWidget(button)

                            button2.pressed.connect(
                                lambda: send_by_email(attribute, values, twi)
                            )

                            twi.layout().addWidget(button2)
                            twi.show()

                            print("show_history done ...")
                            return twi
                    except Exception as e:
                        print(traceback.format_exc())
                        Qt.QMessageBox.warning(
                            None,
                            "Warning",
                            "Unable to retrieve the values (%s), sorry" % e,
                        )
                else:
                    print("dialog closed")
                    return None

            print("asking for dates ...")
            return check_values()
        else:
            Qt.QMessageBox.warning(
                None,
                "Show archiving",
                "Attribute %s is not being archived" % attribute,
                Qt.QMessageBox.Ok,
            )


def save_to_file(var, data, parent, edit):
    try:
        options = {
            "sep": "\\t",
            "arrsep": "\\ ",
            "linesep": "\\n",
        }
        import codecs

        try:
            dd = QOptionDialog(model=options, title="CSV Options")
            dd.exec_()
        except:
            # FIXME: This try catch will not be necessary after fandango update
            print("Using default CSV options")

        for k, v in list(options.items()):
            options[k] = codecs.escape_decode(str(v))[0]

        print(options)

        filename = Qt.QFileDialog.getSaveFileName(
            parent,
            "File to save",
            "/data/" + get_data_filename(var, data, "csv", "human"),
            "CSV files (*.csv)",
        )

        if filename and len(filename) > 1:
            filename = filename[0]

        save_data_file(var, data, filename, format="csv", **options)
        if edit:
            try:
                os.system("gedit %s &" % filename)
            except:
                pass
        return filename
    except Exception as e:
        Qt.QMessageBox.warning(
            None,
            "Warning",
            "Unable to save %s\n:%s" % (filename, e),
        )


def send_by_email(var, data, parent):
    try:
        receivers, ok = Qt.QInputDialog.getText(None, "Send by email", "to:")
        if ok:
            filename = str(save_to_file(var, data, parent, edit=False))
            fandango.linos.sendmail(
                filename,
                var,
                receivers=str(receivers),
                attachments=[filename],
            )
    except Exception as e:
        Qt.QMessageBox.warning(
            None,
            "Warning",
            "Unable to send %s\n:%s" % (filename, e),
        )


def show_history(*args, **kwargs):
    """This method is a wrapper for HistoryDialog.show_new_dialog"""
    print("{}: ArchivingBrowser.archiving_mode.show_history(...)".format(time2str()))
    return ShowHistoryDialog.show_new_dialog(*args, **kwargs)
