#
# gtkui.py
#
# Copyright (C) 2009 SharkByte <Kash@SharkByte.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#

import gtk

from deluge.log import LOG as log
from deluge.ui.client import client
from deluge.plugins.pluginbase import GtkPluginBase
import deluge.component as component
import deluge.common

from twisted.internet import defer

from common import get_resource

class SearchWindow(gtk.Dialog):
    """SearchWindow to search for torrents"""
    def __init__(self):
        super(SearchWindow, self).__init__(title="Search",
            parent = component.get("MainWindow").window,
            flags = (gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_NO_SEPARATOR),
            buttons = ("Cancel", gtk.RESPONSE_NO, "Search", gtk.RESPONSE_YES)
        )

        self.connect("delete-event", self._on_delete_event)
        self.connect("response", self._on_response)

        ui_file = "searchWindow.ui"
        self._load_ui(ui_file)

        self.set_default_response(gtk.RESPONSE_YES)

        self.age = 0

        radio_buttons = {
            "1d_radio": 1,
            "7d_radio": 7,
            "1m_radio": 30,
            "1y_radio": 365,
            "all_radio": 0,
        }

        for name, age in radio_buttons.iteritems():
            button = self.builder.get_object(name)
            button.connect("toggled", self._on_radio_toggled, age)

        self.query = self.builder.get_object("query_entry")
        self.query.set_activates_default(True)
        self.query.grab_focus()

    @property
    def query_value(self):
        return self.query.get_text()

    @property
    def query_age(self):
        return self.age

    def _on_radio_toggled(self, widget, data=None):
        if(widget.get_active()):
            self.age = data

    def _load_ui(self, ui_file):
        """Load content using root object from ui file // test this later"""
        self.builder = gtk.Builder()
        self.builder.add_from_file(get_resource(ui_file))
        self.root = self.builder.get_object("root")
        self.get_content_area().pack_start(self.root)
        self.builder.connect_signals(self)

    def _on_delete_event(self, widget, event):
        self.deferred.callback(gtk.RESPONSE_DELETE_EVENT)
        self.destroy()

    def _on_response(self, widget, response):
        self.deferred.callback(response)
        self.destroy()

    def run(self):
        """Shows the dialog and returns a deferred object // test later"""
        self.deferred = defer.Deferred()
        self.show()
        return self.deferred
    
    @property
    def query_string(self):
        """Return string entered by user"""
        return self.query.get_text()

    
    

class GtkUI(GtkPluginBase):
    def enable(self):
        self.glade = gtk.glade.XML(get_resource("config.glade"))

        component.get("Preferences").add_page("Search", self.glade.get_widget("prefs_box"))
        component.get("PluginManager").register_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").register_hook("on_show_prefs", self.on_show_prefs)

        self.plugin_manager = component.get("PluginManager")
        self.tbar_seperator = self.plugin_manager.add_toolbar_separator()
        self.tbar_search = component.get("ToolBar").add_toolbutton(self.search,
            label="Testing", stock=gtk.STOCK_FIND, tooltip="Use the crawler")

    def disable(self):
        component.get("Preferences").remove_page("Search")
        component.get("PluginManager").deregister_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").deregister_hook("on_show_prefs", self.on_show_prefs)
        self.plugin_manager.remove_toolbar_button(self.tbar_search)
        self.plugin_manager.remove_toolbar_button(self.tbar_seperator)

    def on_apply_prefs(self):
        log.debug("applying prefs for Search")
        config = {
            "test":self.glade.get_widget("txt_test").get_text()
        }
        client.search.set_config(config)

    def on_show_prefs(self):
        client.search.get_config().addCallback(self.cb_get_config)

    def cb_get_config(self, config):
        "callback for on show_prefs"
        self.glade.get_widget("txt_test").set_text(config["test"])

    def search(self, widget):
        """UI to search for torrents to download"""
        searchWindow = SearchWindow()
        searchWindow.run()
        
