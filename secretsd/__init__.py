import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import logging
import os
import xdg.BaseDirectory

from .database import SecretsDatabase
from .service import SecretService
from .password import get_encryption_key

os.umask(0o077)

db_dir = xdg.BaseDirectory.save_data_path("nullroute.eu.org/secretsd")
db_path = os.path.join(db_dir, "secrets.db")

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
sdb = SecretsDatabase(db_path, get_encryption_key())
svc = SecretService(bus, sdb)

loop = GLib.MainLoop()
loop.run()
