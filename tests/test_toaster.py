#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "cnheider"
__doc__ = """
Created on 27/04/2019

@author: cnheider
"""

import unittest

import warg.toaster as toaster


class ModuleTests(unittest.TestCase):
    """Test module level functions.
  """

    def setUp(self):
        toaster.init("toaster test suite")

    def test_init_uninit(self):
        assert toaster.is_initted()
        self.assertEqual(toaster.get_app_name(), "toaster test suite")

        toaster.de_init()
        assert not toaster.is_initted()

    def test_get_server_info(self):
        r = toaster.get_server_info()
        assert isinstance(r, dict), type(r)

    def test_get_server_caps(self):
        r = toaster.get_server_caps()
        assert isinstance(r, list), type(r)


class NotificationTests(unittest.TestCase):
    """Test notifications.
  """

    def setUp(self):
        toaster.init("toaster test suite")

    def test_basic(self):
        n = toaster.Toast("Title", "Body")
        n.show()
        n.close()

    def test_icon(self):
        n = toaster.Toast("Title", "Body", icon="notification-message-im")
        n.show()
        n.close()

    def test_icon_only(self):
        if "x-canonical-private-icon-only" in toaster.get_server_caps():
            n = toaster.Toast("", "", icon="notification-device-eject")
            n.set_hint_string("x-canonical-private-icon-only", "true")
            n.show()

    def test_urgency(self):
        nl = toaster.Toast("Low", "")
        nl.set_urgency(toaster.URGENCY_LOW)
        nl.show()
        nl.close()

        nn = toaster.Toast("Normal", "")
        nn.set_urgency(toaster.URGENCY_NORMAL)
        nn.show()
        nn.close()

        nu = toaster.Toast("Urgent", "")
        nu.set_urgency(toaster.URGENCY_CRITICAL)
        nu.show()
        nu.close()

    def test_update(self):
        n = toaster.Toast("First message", "Some text", icon="notification-message-im")
        n.show()

        # The icon should stay the same with this
        n.update("Second message", "Some more text")
        n.show()

        # But this should replace the icon
        n.update("Third message", "Yet more text, new icon.", icon="notification-message-email")
        n.show()
        n.close()

    def test_category(self):
        n = toaster.Toast("Plain")
        n.set_category("im.received")
        n.show()
        n.close()

    def test_timeout(self):
        n = toaster.Toast("Plain")
        self.assertEqual(n.get_timeout(), toaster.EXPIRES_DEFAULT)
        n.set_timeout(toaster.EXPIRES_NEVER)
        self.assertEqual(n.get_timeout(), toaster.EXPIRES_NEVER)
        n.set_timeout(5000)
        self.assertEqual(n.get_timeout(), 5000)
        n.show()
        n.close()

    def test_data(self):
        n = toaster.Toast("Plain")
        n._data["a"] = 1
        n.set_data("b", 2)  # pynotify API
        n.show()
        self.assertEqual(n.get_data("a"), 1)  # pynotify API
        self.assertEqual(n._data["b"], 2)
        n.close()

    def test_icon_from_pixbuf(self):
        import gi

        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk

        helper = Gtk.Button()
        pb = helper.render_icon(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG)

        # pb = GdkPixbuf.Pixbuf.new_from_file("examples/applet-critical.png")
        n = toaster.Toast("Icon", "Testing icon from pixbuf")
        n.set_icon_from_pixbuf(pb)
        n.show()
        n.close()

    def test_set_location(self):
        n = toaster.Toast("Location", "Test setting location")
        n.set_location(320, 240)
        n.show()
        n.close()


if __name__ == "__main__":
    unittest.main()
