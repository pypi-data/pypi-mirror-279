import fandango as fn
from tango import DevFailed
from taurus.core.tango.tangodatabase import (
    TangoDatabase,
    TangoDatabaseCache,
    TangoServInfo,
    TangoDevTree,
    TangoServerTree,
    TangoDevClassInfo,
    Device,
    TangoDevInfo,
)
from taurus.core.util.containers import CaselessDict

from pyhdbpp import get_default_reader


class TaurusArchivingCache(TangoDatabaseCache):

    def refresh(self):
        db = self.db
        db_dev_name = "/".join((db.getFullName(), db.dev_name()))
        if hasattr(Device(db_dev_name), "DbMySqlSelect"):
            # optimization in case the db exposes a MySQL select API
            query = "SELECT name, alias, exported, host, server, class " + "FROM device"
            r = db.command_inout("DbMySqlSelect", query)
            row_nb, column_nb = r[0][-2:]
            data = r[1]
            assert row_nb == len(data) / column_nb
        else:
            # fallback using tango commands (slow but works with sqlite DB)
            # see http://sf.net/p/tauruslib/tickets/148/
            data = []
            all_alias = {}
            all_devs = db.get_device_name("*", "*")
            all_exported = db.get_device_exported("*")
            for k in db.get_device_alias_list("*"):  # Time intensive!!
                all_alias[db.get_device_alias(k)] = k
            for d in all_devs:  # Very time intensive!!
                _info = db.command_inout("DbGetDeviceInfo", d)[1]
                name, ior, level, server, host, started, stopped = _info[:7]
                klass = db.get_class_for_device(d)
                alias = all_alias.get(d, "")
                exported = str(int(d in all_exported))
                data.extend((name, alias, exported, host, server, klass))
            column_nb = 6  # len ((name, alias, exported, host, server, klass))

        CD = CaselessDict
        dev_dict, serv_dict, klass_dict, alias_dict = CD(), {}, {}, CD()
        arch_devs = self.db.get_archived_devices_list()

        for i in range(0, len(data), column_nb):
            name, alias, exported, host, server, klass = data[i : i + column_nb]
            if name.lower() not in arch_devs:
                continue
            if name.count("/") != 2:
                continue  # invalid/corrupted entry: just ignore it
            if server.count("/") != 1:
                continue  # invalid/corrupted entry: just ignore it
            if not len(alias):
                alias = None

            serv_dict[server] = si = serv_dict.get(
                server, TangoServInfo(self, name=server, full_name=server)
            )

            klass_dict[klass] = dc = klass_dict.get(
                klass, TangoDevClassInfo(self, name=klass, full_name=klass)
            )

            full_name = "%s/%s" % (db.getFullName(), name)
            dev_dict[name] = di = TangoDevInfo(
                self,
                name=name,
                full_name=full_name,
                alias=alias,
                server=si,
                klass=dc,
                exported=exported,
                host=host,
            )

            si.addDevice(di)
            dc.addDevice(di)
            if alias is not None:
                alias_dict[alias] = di

        self._devices = dev_dict
        self._device_tree = TangoDevTree(dev_dict)
        self._server_tree = TangoServerTree(serv_dict)
        self._servers = serv_dict
        self._klasses = klass_dict
        self._aliases = alias_dict

    def refreshAttributes(self, device):
        attrs = []
        try:
            db = self.db
            name = device.name()
            attrs = sorted(self.db.get_device_attribute_list(name, "*"))
        except DevFailed as df:
            pass
        device.setAttributes(attrs)


class TaurusArchivingDatabase(TangoDatabase):

    def __init__(self, host=None, port=None, parent=None):
        TangoDatabase.__init__(self, host=host, port=port, parent=parent)
        self._reader = get_default_reader()
        self._archived_devs = None

    @fn.objects.Cached(depth=10, expire=120.0)
    def get_archived_devices_list(self, active=True, attrs=None):
        attrs = attrs or self.get_archived_attributes_list(active)
        self._archived_devs = sorted(
            set(fn.tango.get_normal_name(a).rsplit("/", 1)[0] for a in attrs)
        )
        return self._archived_devs

    def get_archived_attributes_list(self, active=True):
        # already cached internally
        attrs = self._reader.get_attributes(active)
        return attrs

    def get_device_attribute_list(self, dev_name, wildcard="*"):
        dev_name = fn.tango.get_normal_name(dev_name)
        attrs = self._reader.get_attributes(active=True)
        dattrs = [a.rsplit("/")[-1] for a in attrs if (dev_name + "/").lower() in a]
        return [a for a in dattrs if fn.clmatch(wildcard, a)]

    def cache(self):
        if self._dbCache is None:
            self._dbCache = TaurusArchivingCache(self)
        return self._dbCache
