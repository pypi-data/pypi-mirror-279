import taurus.core
from taurus.core.util.containers import CaselessList
from taurus.external.qt import Qt
from taurus.qt.qtgui.container import TaurusWidget
from taurus.qt.qtgui.panel.taurusmodellist import TaurusModelList
from taurus.qt.qtcore.mimetypes import mimetypes

from TangoBrowser.TreeUtility.TaurusDbTreeWidget import TaurusModelSelectorTree


class TaurusModelChooser(TaurusWidget):
    """A widget that allows the user to select a list of models from a tree representing
    devices and attributes from a Tango server.

    The user selects models and adds them to a list. Then the user should click on the
    update button to notify that the selection is ready.

    signals::
      - "updateModels"  emitted when the user clicks on the update button. It
        passes a list<str> of models that have been selected.
    """

    updateModels = Qt.pyqtSignal("QStringList", name="updateModels")
    UpdateAttrs = Qt.pyqtSignal(["QStringList"], ["QMimeData"], name="UpdateAttrs")

    def __init__(
        self,
        parent=None,
        selectables=None,
        host=None,
        designMode=None,
        singleModel=False,
    ):
        """Creator of TaurusModelChooser

        :param parent: (QObject) parent for the dialog
        :param selectables: (list<TaurusElementType>) if passed, only elements of the tree whose
                            type is in the list will be selectable.
        :param host: (QObject) Tango host to be explored by the chooser
        :param designMode: (bool) needed for taurusdesigner but ignored here
        :param singleModel: (bool) If True, the selection will be of just one
                            model. Otherwise (default) a list of models can be selected
        """
        TaurusWidget.__init__(self, parent)
        if host is None:
            host = taurus.Authority().getNormalName()

        self._allowDuplicates = False

        self.setLayout(Qt.QVBoxLayout())

        self.tree = TaurusModelSelectorTree(
            selectables=selectables, buttonsPos=Qt.Qt.BottomToolBarArea
        )
        self.tree.setModel(host)
        self.list = TaurusModelList()
        self.list.setSelectionMode(Qt.QAbstractItemView.ExtendedSelection)
        applyBT = Qt.QToolButton()
        applyBT.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
        applyBT.setText("Apply")
        applyBT.setIcon(Qt.QIcon("status:available.svg"))

        self._singleModelMode = singleModel

        # toolbar
        self._toolbar = self.tree.toolbar
        self._toolbar.addAction(self.list.removeSelectedAction)
        self._toolbar.addAction(self.list.removeAllAction)
        self._toolbar.addAction(self.list.moveUpAction)
        self._toolbar.addAction(self.list.moveDownAction)
        self._toolbar.addSeparator()
        self._toolbar.addWidget(applyBT)
        self.layout().addWidget(self.tree)
        self.layout().addWidget(self.list)

        self.modelChanged.connect(self.tree.setModel)

        # connections:
        self.tree.addModels.connect(self.add_models)
        applyBT.clicked.connect(self._on_update_models)

    def get_listed_models(self, asMimeData=False):
        """returns the list of models that have been added

        :param asMimeData: (bool) If False (default), the return value will be a
                           list of models. If True, the return value is a
                           `QMimeData` containing at least `TAURUS_MODEL_LIST_MIME_TYPE`
                           and `text/plain` MIME types. If only one model was selected,
                           the mime data also contains a TAURUS_MODEL_MIME_TYPE.

        :return: (list<str> or QMimeData) the type of return depends on the value of `asMimeData`
        """
        models = self.list.getModelList()
        if self.is_single_model_mode():
            models = models[:1]
        if asMimeData:
            md = Qt.QMimeData()
            md.setData(mimetypes.TAURUS_MODEL_LIST_MIME_TYPE, str("\r\n".join(models)))
            md.setText(", ".join(models))
            if len(models) == 1:
                md.setData(mimetypes.TAURUS_MODEL_MIME_TYPE, str(models[0]))
            return md
        return models

    def set_listed_models(self, models):
        """adds the given list of models to the widget list"""
        self.list.model().clearAll()
        self.list.addModels(models)

    def reset_listed_models(self):
        """equivalent to setListedModels([])"""
        self.list.model().clearAll()

    def update_list(self, attrList):
        """for backwards compatibility with AttributeChooser only. Use :meth:`setListedModels` instead"""
        self.info(
            "ModelChooser.updateList() is provided for backwards compatibility only. Use setListedModels() instead"
        )
        self.set_listed_models(attrList)

    def add_models(self, models):
        """Add given models to the selected models list"""
        if len(models) == 0:
            models = [""]
        if self.is_single_model_mode():
            self.reset_listed_models()
        if self._allowDuplicates:
            self.list.addModels(models)
        else:
            listedmodels = CaselessList(self.get_listed_models())
            for m in models:
                if m not in listedmodels:
                    listedmodels.append(m)
                    self.list.addModels([m])

    def on_remove_selected(self):
        """
        Remove the list-selected models from the list
        """
        self.list.removeSelected()

    def _on_update_models(self):
        models = self.get_listed_models()
        self.updateModels.emit(models)
        if (
            taurus.core.taurusbasetypes.TaurusElementType.Attribute
            in self.tree._selectables
        ):
            # for backwards compatibility with the old AttributeChooser
            self.UpdateAttrs.emit(models)

    def set_single_model_mode(self, single):
        """
        sets whether the selection should be limited to just one model
        (single=True) or not (single=False)
        """

        if single:
            self.tree.tree_view().setSelectionMode(Qt.QAbstractItemView.SingleSelection)
        else:
            self.tree.tree_view().setSelectionMode(
                Qt.QAbstractItemView.ExtendedSelection
            )
        self._singleModelMode = single

    def is_single_model_mode(self):
        """returns True if the selection is limited to just one model. Returns False otherwise.

        :return: (bool)"""
        return self._singleModelMode

    def reset_single_model_mode(self):
        """equivalent to setSingleModelMode(False)"""
        self.set_single_model_mode(False)

    @staticmethod
    def model_chooser_dlg(
        parent=None,
        selectables=None,
        host=None,
        asMimeData=False,
        singleModel=False,
        windowTitle="Model Chooser",
    ):
        """Static method that launches a modal dialog containing a TaurusModelChooser

        :param parent: (QObject) parent for the dialog
        :param selectables: (list<TaurusElementType>) if passed, only elements of the tree whose
                            type is in the list will be selectable.
        :param host: (QObject) Tango host to be explored by the chooser
        :param asMimeData: (bool) If False (default),  a list of models will be.
                           returned. If True, a `QMimeData` object will be
                           returned instead. See :meth:`getListedModels` for a
                           detailed description of this QMimeData object.
        :param singleModel: (bool) If True, the selection will be of just one
                            model. Otherwise (default) a list of models can be selected
        :param windowTitle: (str) Title of the dialog (default="Model Chooser")

        :return: (list,bool or QMimeData,bool) Returns a models,ok tuple. models can be
                 either a list of models or a QMimeData object, depending on
                 `asMimeData`. ok is True if the dialog was accepted (by
                 clicking on the "update" button) and False otherwise
        """
        dlg = Qt.QDialog(parent)
        dlg.setWindowTitle(windowTitle)
        dlg.setWindowIcon(Qt.QIcon("logos:taurus.png"))
        layout = Qt.QVBoxLayout()
        w = TaurusModelChooser(
            parent=parent, selectables=selectables, host=host, singleModel=singleModel
        )
        layout.addWidget(w)
        dlg.setLayout(layout)
        w.updateModels.connect(dlg.accept)
        dlg.exec_()
        return w.get_listed_models(asMimeData=asMimeData), (
            dlg.result() == dlg.Accepted
        )

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusWidget.getQtDesignerPluginInfo()
        ret["module"] = "taurus.qt.qtgui.panel"
        ret["icon"] = "designer:listview.png"
        ret["container"] = False
        ret["group"] = "Taurus Views"
        return ret

    singleModelMode = Qt.pyqtProperty(
        "bool", is_single_model_mode, set_single_model_mode, reset_single_model_mode
    )
