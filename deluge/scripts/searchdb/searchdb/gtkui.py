#
# gtkui.py
#
# Copyright (C) 2009 SharkByte <Kash@sharkbyte.com>
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

from dbInterface import db_interface


class BaseDialog(gtk.Dialog):
    """Base dialog class for plugin dialogs (based on Deluge BaseDialog)."""

    def __init__(self, title, buttons, ui_file=None, parent=None):
        super(BaseDialog, self).__init__(
            title=title,
            parent=parent if parent else component.get("MainWindow").window,
            flags=(gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT |
                   gtk.DIALOG_NO_SEPARATOR),
            buttons=buttons)

        self.connect("delete-event", self._on_delete_event)
        self.connect("response", self._on_response)

        if ui_file is not None:
            self._load_ui(ui_file)

    def _load_ui(self, ui_file):
        """Load dialog content using root object from ui file."""
        self.builder = gtk.Builder()
        self.builder.add_from_file(get_resource(ui_file))
        self.root = self.builder.get_object('root')

        self.get_content_area().pack_start(self.root)
        self.builder.connect_signals(self)

    def _on_delete_event(self, widget, event):
        self.deferred.callback(gtk.RESPONSE_DELETE_EVENT)
        self.destroy()

    def _on_response(self, widget, response):
        self.deferred.callback(response)
        self.destroy()

    def run(self):
        """
        Shows the dialog and returns a Deferred object.
        The deferred, when fired will contain the response ID.
        """
        self.deferred = defer.Deferred()
        self.show()
        return self.deferred


class SearchDialog(BaseDialog):
    """Torrent search dialog."""

    def __init__(self):
        super(SearchDialog, self).__init__('Search',
            ('Cancel', gtk.RESPONSE_NO, 'Search', gtk.RESPONSE_YES), ui_file='searchWindow.ui')

        self.set_default_response(gtk.RESPONSE_YES)

        self.search_type = 0
        radio_buttons = {'by_name': "torrent_name",
                         'by_age': "upload_date_time",
                         'by_uploader': "uploader",
                         'by_size': "file_size",
                         'search_all': 0}

        for name, age in radio_buttons.iteritems():
            button = self.builder.get_object(name)
            button.connect("toggled", self._on_radio_toggled, age)

        self.query = self.builder.get_object('query_entry')
        self.query.set_activates_default(True)
        self.query.grab_focus()

    @property
    def query_text(self):
        """Text entered by the user."""
        return self.query.get_text()

    @property
    def query_type(self):
        """Query String entered by user"""
        return self.search_type

    def _on_radio_toggled(self, widget, data=None):
        """Checks if radio_buttons get toggled"""
        if (widget.get_active()):
            self.search_type = data


class ResultsDialog(BaseDialog):
    """Torrent results dialog."""

    SELECTED = 6
    MAG_LINK = 7

    def __init__(self):
        super(ResultsDialog, self).__init__('Results',
            ('Cancel', gtk.RESPONSE_CLOSE,
             'Add to Queue', gtk.RESPONSE_YES),
            ui_file='resultsWindow.ui')

        self.set_default_response(gtk.RESPONSE_YES)
        self.results_store = self.builder.get_object('results_store')

    def get_torrent_list(self, results):
        """gets meta_data from DB into the list to display"""
        self.results_store.clear()
        for result in results:
            """title | size | uploader | date | seeds | leeches | Add2Q | mag_link"""
            row = [result[0], result[1], result[4], result[5], str(result[2]),
                   str(result[3]), False, result[6]]
            self.results_store.append(row)    

    @property
    def selected(self):
        """Return Magnet links for torrents selection from user."""
        selected = [
            t[self.MAG_LINK] for t in self.results_store if t[self.SELECTED]
        ]
        return selected

    def on_toggled(self, renderer, path):
        """Update torrent selection box in the store."""
        current_value = renderer.get_active()
        tree_iter = self.results_store.get_iter_from_string(path)
        self.results_store.set(tree_iter, self.SELECTED, not current_value)


class GtkUI(GtkPluginBase):
    def enable(self):
        self.plugin_manager = component.get("PluginManager")
        self.tb_separator = self.plugin_manager.add_toolbar_separator()
        self.tb_search = self.plugin_manager.add_toolbar_button(self.search,
            label="Test", stock=gtk.STOCK_FIND, tooltip="Search IsoHunt")

    def disable(self):
        self.plugin_manager.remove_toolbar_button(self.tb_search)
        self.plugin_manager.remove_toolbar_button(self.tb_separator)

    @defer.inlineCallbacks
    def search(self, widget):
        """Search and add torrents to download queue."""
        search_dialog = SearchDialog()
        response = yield search_dialog.run()

        if response == gtk.RESPONSE_YES:
                      
            search_type = search_dialog.query_type
            query = search_dialog.query_text
            
            db_api = db_interface()

            results_dialog = ResultsDialog()

            if search_type != 0:
                results_dialog.get_torrent_list(db_api.find_by_filter(search_type, query))

            else:
                results_dialog.get_torrent_list(db_api.get_all_columns())

            response = yield results_dialog.run()

            if response == gtk.RESPONSE_YES:
                selected = results_dialog.selected

                for torrent in selected:
                    component.get("Core").add_torrent_magnet(torrent, {})
