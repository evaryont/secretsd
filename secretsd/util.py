import dbus
import dbus.service

from .exception import InvalidArgsException

NullObject = dbus.ObjectPath("/")

class BusObjectWithProperties():
    PROPERTIES = {}

    @dbus.service.method("org.freedesktop.DBus.Properties", "ss", "v",
                         path_keyword="path")
    def Get(self, interface, property, path=None):
        if interface == self.INTERFACE:
            if property in self.PROPERTIES:
                getter, setter, value = self.PROPERTIES[property]
                if getter:
                    value = getter(self, path)
                return value
            else:
                raise InvalidArgsException("No such property %r" % str(property))
        else:
            raise InvalidArgsException("No such interface %r" % str(interface))

    @dbus.service.method("org.freedesktop.DBus.Properties", "s", "a{sv}",
                         path_keyword="path")
    def GetAll(self, interface, path=None):
        if interface == self.INTERFACE:
            out = {}
            for name, (getter, setter, value) in self.PROPERTIES.items():
                if getter:
                    value = getter(self, path)
                out[name] = value
            return out
        else:
            raise InvalidArgsException("No such interface %r" % str(interface))

    @dbus.service.method("org.freedesktop.DBus.Properties", "ssv", "",
                         path_keyword="path")
    def Set(self, interface, property, value, path=None):
        if interface == self.INTERFACE:
            if property in self.PROPERTIES:
                getter, setter, _ = self.PROPERTIES[property]
                if setter:
                    setter(self, path, value)
                else:
                    raise InvalidArgsException("Property %r is read-only" % str(property))
            else:
                raise InvalidArgsException("No such property %r" % str(property))
        else:
            raise InvalidArgsException("No such interface %r" % str(interface))

    @dbus.service.signal("org.freedesktop.DBus.Properties", "sa{sv}as")
    def PropertiesChanged(self, interface, changed_props, invalidated_props):
        pass
