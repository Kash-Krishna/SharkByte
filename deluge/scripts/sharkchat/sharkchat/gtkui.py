#
# gtkui.py
#
# Copyright (C) 2009 Rachel Law <rlaw001@ucr.edu>
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

import datetime, subprocess
import os, sys, threading, time
from db_interface import db_interface
from random import randint
from thread import *


# Sweet, makes an easy window base class to work with :D
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


class SharkChat(BaseDialog):
    """Torrent search dialog."""

    def __init__(self):
        super(SharkChat, self).__init__('SharkChat',
            ('Cancel', gtk.RESPONSE_NO, 'Refresh', gtk.RESPONSE_YES), ui_file='SharkChat.ui')

        self.last_update_time = datetime.datetime.now()

        self.sharkchat_textview = self.builder.get_object('messages_textview')
        self.sendto_entry = self.builder.get_object('sendto_entry')
        self.message_entry = self.builder.get_object('message_entry')
        self.send_button = self.builder.get_object('send_button')
        self.chat_view = self.builder.get_object('treeview1')

        # make my own liststore!!! >O
        #self.liststore1 = self.builder.get_object('liststore1')

        # can connect via connect(), or within the glade file
        #   gobject.GObject.connect
        #   def connect(detailed_signal, handler, ...)        
        #self.send_button.connect("clicked", self.OnSendChat)

        #Add all of the List Columns to the treeview
        self.AddTreeColumns("To", 0)
        self.AddTreeColumns("From", 1)
        self.AddTreeColumns("Message", 2)
        self.AddTreeColumns("Time", 3)
    
        #Create the listStore Model to use with the chat_view
        self.messages_list = gtk.ListStore(str, str, str, str)
        #Attache the model to the treeView
        self.chat_view.set_model(self.messages_list)

    def AddTreeColumns(self, title, columnId):
        """This function adds a column to the list view.
        First it create the gtk.TreeViewColumn and then set
        some needed properties"""
                        
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=columnId)
        column.set_resizable(True)      
        column.set_sort_column_id(columnId)
        self.chat_view.append_column(column)

    def OnSendChat(self, widget):
        # void gtk_entry_set_text (GtkEntry *entry, const gchar *text);
        sendto = self.sendto_entry.get_text()
        message = self.message_entry.get_text()
        # self.sendto_entry.set_text("");
        self.message_entry.set_text("");
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



        db_api = db_interface()
        # self.client_thread.communicate(str(sendto))
        # self.client_thread.communicate(str(message))

        # MY SCHEMA
        # def insert_new_message(self, msgid, message_text, to_user_id, from_user_id, time):
        # db_api.insert_new_message(str(randint(0,999999)), str(message), str(sendto), "MYSELF", str(now))

        # KEVIN SCHEMA
        db_api.insert_new_message(str(randint(0,999999)), str(message), str(sendto), "me", str(now))
        # new_messages = db_api.insert_new_message(self.last_update_time, now)
        entry_list = [sendto, "me", message, now]
        self.messages_list.append(entry_list)

    def OnRefreshMessages(self, widget):
        db_api = db_interface()
        now = datetime.datetime.now()
        new_msgs = db_api.get_new_columns(self.last_update_time, now)
        self.messages_list.clear()
        for msg in new_msgs:
            """messages schema: 
                                msg_id INT PRIMARY KEY,
                                time_sent TEXT NOT NULL,
                                msg TEXT, 
                                sender_uid TEXT NOT NULL, 
                                tag TEXT 

                interface schema: To, From, Message, Time

            """
            # KEVIN
            msg_row = ["me", str(msg[3]), str(msg[2]), str(msg[1])]
            print msg_row
            self.messages_list.append(msg_row)
        




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



class GtkUI(GtkPluginBase):
    def enable(self):
        self.glade = gtk.glade.XML(get_resource("config.glade"))

        self.plugin_manager = component.get("PluginManager")
        self.tb_separator = self.plugin_manager.add_toolbar_separator()
        self.tb_search = self.plugin_manager.add_toolbar_button(self.start_sharkchat,
            label="SharkChat", stock=gtk.STOCK_FIND, tooltip="SharkChat")

        component.get("Preferences").add_page("SharkChat", self.glade.get_widget("prefs_box"))
        component.get("PluginManager").register_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").register_hook("on_show_prefs", self.on_show_prefs)

        # client.py threads :)
        # client_command = "python /home/rlaw/Documents/cs179_kash/youtor/sub_sys/client/client.py"
        # self.client_thread = subprocess.Popen(client_command, shell=True, stdin=subprocess.PIPE)

    def disable(self):
        self.plugin_manager.remove_toolbar_button(self.tb_search)
        self.plugin_manager.remove_toolbar_button(self.tb_separator)

        component.get("Preferences").remove_page("SharkChat")
        component.get("PluginManager").deregister_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").deregister_hook("on_show_prefs", self.on_show_prefs)

    @defer.inlineCallbacks
    def start_sharkchat(self, widget):
        """Search and add torrents to download queue."""
        search_dialog = SharkChat()
        response = yield search_dialog.run()

    def on_apply_prefs(self):
        log.debug("applying prefs for SharkChat")
        config = {
            "test":self.glade.get_widget("txt_test").get_text()
        }
        client.sharkchat.set_config(config)

    def on_show_prefs(self):
        client.sharkchat.get_config().addCallback(self.cb_get_config)

    def cb_get_config(self, config):
        "callback for on show_prefs"
        self.glade.get_widget("txt_test").set_text(config["test"])
