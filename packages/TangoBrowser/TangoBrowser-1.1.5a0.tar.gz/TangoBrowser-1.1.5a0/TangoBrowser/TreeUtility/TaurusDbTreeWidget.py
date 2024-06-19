from taurus.core.taurusauthority import TaurusAuthority
from taurus.core.taurusbasetypes import TaurusElementType
from taurus.external.qt import Qt
from taurus.qt.qtcore.model import TaurusBaseProxyModel
from taurus.qt.qtcore.model.taurusdatabasemodel import (
    ElemType,
    TaurusTreeDeviceDomainItem,
    TaurusTreeDeviceFamilyItem,
    TaurusTreeDeviceItem,
    TaurusTreeSimpleDeviceItem,
    TaurusTreeDeviceMemberItem,
    TaurusDbBaseModel,
    TaurusDbPlainDeviceModel,
    TaurusDbServerProxyModel,
    TaurusDbServerModel,
    TaurusDbDeviceClassProxyModel,
    TaurusDbDeviceClassModel,
)
from taurus.qt.qtgui.base import TaurusBaseWidget
from taurus.qt.qtgui.container import TaurusWidget
from taurus.qt.qtgui.icon import getElementTypeIconName
from taurus.qt.qtgui.tree import TaurusBaseTreeWidget

from TangoBrowser.TreeUtility.TaurusArchivingDatabase import TaurusArchivingDatabase


class TaurusDbDeviceProxyModel(TaurusBaseProxyModel):
    """A Qt filter & sort model for model for the taurus models:
    - TaurusDbBaseModel
    - TaurusDbDeviceModel
    - TaurusDbSimpleDeviceModel
    - TaurusDbPlainDeviceModel"""

    def filterAcceptsRow(self, sourceRow, sourceParent):
        sourceModel = self.sourceModel()
        idx = sourceModel.index(sourceRow, 0, sourceParent)
        treeItem = idx.internalPointer()
        regexp = self.filterRegExp()

        # if domain node, check if it will potentially have any children
        if isinstance(treeItem, TaurusTreeDeviceDomainItem):
            domain = treeItem.display()
            devices = sourceModel.getDomainDevices(domain)
            for device in devices:
                if self.device_matches(device, regexp):
                    return True
            return False

        # if family node, check if it will potentially have any children
        if isinstance(treeItem, TaurusTreeDeviceFamilyItem):
            domain = treeItem.parent().display()
            family = treeItem.display()
            devices = sourceModel.getFamilyDevices(domain, family)
            for device in devices:
                if self.device_matches(device, regexp):
                    return True
            return False

        if (
            isinstance(treeItem, TaurusTreeDeviceItem)
            or isinstance(treeItem, TaurusTreeSimpleDeviceItem)
            or isinstance(treeItem, TaurusTreeDeviceMemberItem)
        ):
            device = treeItem.itemData()
            return self.device_matches(device, regexp)
        return True

    @staticmethod
    def device_matches(device, regexp):
        name = device.name()

        # if Qt.QString(name).contains(regexp):
        if regexp.indexIn(name) != -1:
            return True
        name = device.alias()
        if name is None:
            return False
        # return Qt.QString(name).contains(regexp)
        return regexp.indexIn(name) != -1


class TaurusDbDeviceModel(TaurusDbBaseModel):
    """A Qt model that structures device elements in a 3 level tree organized
    as:

        - <domain>
        - <family>
        - <member>"""

    ColumnRoles = (
        (
            ElemType.Device,
            ElemType.Domain,
            ElemType.Family,
            ElemType.Member,
            ElemType.Attribute,
        ),
        ElemType.DeviceAlias,
        ElemType.Server,
        ElemType.DeviceClass,
        ElemType.Exported,
        ElemType.Host,
    )

    def __init__(self, *args, **kwargs):
        super(TaurusDbDeviceModel, self).__init__(*args, **kwargs)
        self.setDataSource(TaurusArchivingDatabase())

    def setupModelData(self, data):
        if data is None:
            return
        try:
            # TODO: is this try needed? (not done in, e.g. TaurusDbPlainDeviceModel)
            from taurus.core.tango.tangodatabase import TangoDatabase
        except ImportError:
            return
        if isinstance(data, TangoDatabase):
            data = data.deviceTree()

        rootItem = self._rootItem
        for domain in data.keys():
            families = data[domain]
            domainItem = TaurusTreeDeviceDomainItem(self, domain.upper(), rootItem)
            for family in families.keys():
                members = families[family]
                familyItem = TaurusTreeDeviceFamilyItem(
                    self, family.upper(), domainItem
                )
                for member in members.keys():
                    dev = members[member]
                    memberItem = TaurusTreeDeviceItem(self, dev, parent=familyItem)
                    familyItem.appendChild(memberItem)
                domainItem.appendChild(familyItem)
            rootItem.appendChild(domainItem)


class TaurusDbTreeWidget(TaurusBaseTreeWidget):
    """A class:`taurus.qt.qtgui.tree.TaurusBaseTreeWidget` that connects to a
    :class:`taurus.core.taurusauthority.TaurusAuthority` model. It can show the list of database
    elements in four different perspectives:

    - device : a three level hierarchy of devices (domain/family/name)
    - server : a server based perspective
    - class : a class based perspective

    Filters can be inserted into this widget to restrict the tree nodes that are
    seen.
    """

    KnownPerspectives = {
        TaurusElementType.Device: {
            "label": "By device",
            "icon": getElementTypeIconName(TaurusElementType.Device),
            "tooltip": "View by device tree",
            "model": [
                TaurusDbDeviceProxyModel,
                TaurusDbDeviceModel,
            ],
        },
        # TODO: Implement filtering on the rest of options
        #  (Not working right now)
        # "PlainDevice": {
        #     "label": "By plain device",
        #     "icon": getElementTypeIconName(TaurusElementType.Device),
        #     "tooltip": "View by plain device tree (it may take a long time "
        #                "if there are problems with the exported devices)",
        #     "model": [
        #         TaurusDbDeviceProxyModel,
        #         TaurusDbPlainDeviceModel,
        #     ],
        # },
        # TaurusElementType.Server: {
        #     "label": "By server",
        #     "icon": getElementTypeIconName(TaurusElementType.Server),
        #     "tooltip": "View by server tree",
        #     "model": [
        #         TaurusDbServerProxyModel,
        #         TaurusDbServerModel,
        #     ],
        # },
        # TaurusElementType.DeviceClass: {
        #     "label": "By class",
        #     "icon": getElementTypeIconName(TaurusElementType.DeviceClass),
        #     "tooltip": "View by class tree",
        #     "model": [
        #         TaurusDbDeviceClassProxyModel,
        #         TaurusDbDeviceClassModel,
        #     ],
        # },
    }

    DftPerspective = TaurusElementType.Device

    def getModelClass(self):
        return TaurusAuthority

    def sizeHint(self):
        return Qt.QSize(1024, 512)

    @Qt.pyqtSlot("QString")
    def setModel(self, model, obj=None):
        """Sets/unsets the model name for this component

        :param model: (str) the new model name"""
        super(TaurusDbTreeWidget, self).setModel(model)
        self.modelObj = obj

    def _attach(self, **kwargs):
        """Attaches the component to the taurus model.
        In general it should not be necessary to overwrite this method in a
        subclass.

        :return: (bool) True if success in attachment or False otherwise.
        """
        if self.isAttached():
            return self._attached

        self.preAttach()

        self.postAttach()
        return self._attached

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusBaseWidget.getQtDesignerPluginInfo()
        ret["module"] = "taurus.qt.qtgui.tree"
        ret["group"] = "Taurus Views"
        ret["icon"] = "designer:listview.png"
        return ret


class TaurusModelSelectorTree(TaurusWidget):
    addModels = Qt.pyqtSignal("QStringList")

    def __init__(self, parent=None, selectables=None, buttonsPos=None, designMode=None):
        TaurusWidget.__init__(self, parent)
        if selectables is None:
            selectables = [
                TaurusElementType.Attribute,
                TaurusElementType.Member,
                TaurusElementType.Device,
            ]
        self._selectables = selectables

        # tree
        self._deviceTree = TaurusDbTreeWidget(perspective=TaurusElementType.Device)

        self._deviceTree.getQModel().setSelectables(self._selectables)
        # self._deviceTree.setUseParentModel(True)
        self._deviceTree.modelObj = TaurusArchivingDatabase()

        # toolbar
        self.toolbar = Qt.QToolBar("TangoSelector toolbar")
        self.toolbar.setIconSize(Qt.QSize(16, 16))
        self.toolbar.setFloatable(False)
        self._addSelectedAction = self.toolbar.addAction(
            Qt.QIcon.fromTheme("list-add"), "Add selected", self.on_add_selected
        )

        # defines the layout
        self.set_buttons_pos(buttonsPos)

        self._deviceTree.recheckTaurusParent()  # NOT WORKING????
        # @todo: This is Workaround because UseSetParentModel is giving trouble again!
        self.modelChanged.connect(self._deviceTree.setModel)

    def set_buttons_pos(self, buttonsPos):
        # we must delete the previous layout before we can set a new one
        currlayout = self.layout()
        if currlayout is not None:
            currlayout.deleteLater()
            Qt.QCoreApplication.sendPostedEvents(currlayout, Qt.QEvent.DeferredDelete)
        # add to layout
        if buttonsPos is None:
            self.setLayout(Qt.QVBoxLayout())
            self.layout().addWidget(self._deviceTree)
        elif buttonsPos == Qt.Qt.BottomToolBarArea:
            self.toolbar.setOrientation(Qt.Qt.Horizontal)
            self.setLayout(Qt.QVBoxLayout())
            self.layout().addWidget(self._deviceTree)
            self.layout().addWidget(self.toolbar)
        elif buttonsPos == Qt.Qt.TopToolBarArea:
            self.toolbar.setOrientation(Qt.Qt.Horizontal)
            self.setLayout(Qt.QVBoxLayout())
            self.layout().addWidget(self.toolbar)
            self.layout().addWidget(self._deviceTree)
        elif buttonsPos == Qt.Qt.LeftToolBarArea:
            self.toolbar.setOrientation(Qt.Qt.Vertical)
            self.setLayout(Qt.QHBoxLayout())
            self.layout().addWidget(self.toolbar)
            self.layout().addWidget(self._deviceTree)
        elif buttonsPos == Qt.Qt.RightToolBarArea:
            self.toolbar.setOrientation(Qt.Qt.Vertical)
            self.setLayout(Qt.QHBoxLayout())
            self.layout().addWidget(self._deviceTree)
            self.layout().addWidget(self.toolbar)
        else:
            raise ValueError("Invalid buttons position")

    def get_selected_models(self):
        selected = []
        try:
            from taurus.core.tango.tangodatabase import TangoDevInfo, TangoAttrInfo
        except:
            return selected
        for item in self._deviceTree.selectedItems():
            nfo = item.itemData()
            if isinstance(nfo, TangoDevInfo):
                selected.append(nfo.fullName())
            elif isinstance(nfo, TangoAttrInfo):
                selected.append("%s/%s" % (nfo.device().fullName(), nfo.name()))
            else:
                self.info("Unknown item '%s' in selection" % repr(nfo))
        return selected

    def on_add_selected(self):
        self.addModels.emit(self.get_selected_models())

    def tree_view(self):
        return self._deviceTree.treeView()

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusWidget.getQtDesignerPluginInfo()
        ret["module"] = "taurus.qt.qtgui.panel"
        ret["icon"] = "designer:listview.png"
        ret["container"] = False
        ret["group"] = "Taurus Views"
        return ret
