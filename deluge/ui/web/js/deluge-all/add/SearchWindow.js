
Ext.namespace('Deluge.add');

Deluge.add.SearchWindow = Ext.extend(Deluge.add.Window, {

	title: _('Search for Torrents'),
	layout: 'border',
	width: 890,
	height: 650,
	bodyStyle: 'padding: 10px 5px;',
	buttonAlign: 'right',
	closeAction: 'hide',
	closable: true,
	plain: true,
	iconCls: 'x-deluge-add-window-icon',

	initComponent: function() {
		Deluge.add.SearchWindow.superclass.initComponent.call(this);

		this.addButton(_('Cancel'), this.onCancelClick, this);
		this.addButton(_('Add'), this.onAddClick, this);

		function torrentRenderer(value, p, r) {
			if (r.data['info_hash']) {
				return String.format('<div class="x-deluge-add-torrent-name">{0}</div>', value);
			} else {
				return String.format('<div class="x-deluge-add-torrent-name-loading">{0}</div>', value);
			}
		}

		this.list = new Ext.list.ListView({
			store: new Ext.data.SimpleStore({
				fields: [
					{name: 'info_hash', mapping: 1},
					{name: 'text', mapping: 2}
				],
				id: 0
			}),
			columns: [{
				id: 'torrent',
				width: 150,
				sortable: true,
				renderer: torrentRenderer,
				dataIndex: 'text'
			}],
			stripeRows: true,
			singleSelect: true,
			listeners: {
				'selectionchange': {
					fn: this.onSelect,
					scope: this
				}
			},
			hideHeaders: true,
			autoExpandColumn: 'torrent',
			height: '100%',
			autoScroll: true
		});

        this.grid = new Deluge.SearchGrid();
/*        
        this.grid = new Ext.grid.GridPanel({
            store: new Ext.data.SimpleStore({
                fields: [
                    {name: 'Name', type: 'string'},
                    {name: 'size', type: 'string'}
                ],
                data: [
                    {Name: "PoI", size: "3.2"},
                    {Name: "Thor", size: "1.3"}
                ]
            }),
            columns: [{
                {
                    text: 'Name',
                    dataIndex: 'Name',
                    flex: 1
                },{
                    text: 'Size',
                    dataIndex: 'size'
                }
            }],
            height: 300,
            width: 600
            //renderTo: Ext.getBody()
        });
*/
        this.add({
			region: 'center',
			items: [this.grid],
			margins: '5 5 5 5',
			bbar: new Ext.Toolbar({
				items: [{
					iconCls: 'x-deluge-add-file',
					text: _('File'),
					handler: this.onFile,
					scope: this
				}, {
					text: _('Url'),
					iconCls: 'icon-add-url',
					handler: this.onUrl,
					scope: this
				}, {
					text: _('Infohash'),
					iconCls: 'icon-add-magnet',
					hidden: true,
					disabled: true
				}, '->', {
					text: _('Remove'),
					iconCls: 'icon-remove',
					handler: this.onRemove,
					scope: this
				}]
			})
		});

		this.optionsPanel = this.add(new Deluge.add.OptionsPanel());
		this.on('hide', this.onHide, this);
		this.on('show', this.onShow, this);
	},

	clear: function() {
		this.list.getStore().removeAll();
		this.optionsPanel.clear();
	},

	onAddClick: function() {
		var torrents = [];
		if (!this.list) return;
		this.list.getStore().each(function(r) {
			var id = r.get('info_hash');
			torrents.push({
				path: this.optionsPanel.getFilename(id),
				options: this.optionsPanel.getOptions(id)
			});
		}, this);

		deluge.client.web.add_torrents(torrents, {
			success: function(result) {
			}
		})
		this.clear();
		this.hide();
	},

	onCancelClick: function() {
		this.clear();
		this.hide();
	},

	onFile: function() {
		if (!this.file) this.file = new Deluge.add.FileWindow();
		this.file.show();
	},

	onHide: function() {
		this.optionsPanel.setActiveTab(0);
		this.optionsPanel.files.setDisabled(true);
		this.optionsPanel.form.setDisabled(true);
	},

	onRemove: function() {
		if (!this.list.getSelectionCount()) return;
		var torrent = this.list.getSelectedRecords()[0];
		this.list.getStore().remove(torrent);
		this.optionsPanel.clear();

		if (this.torrents && this.torrents[torrent.id]) delete this.torrents[torrent.id];
	},

	onSelect: function(list, selections) {
		if (selections.length) {
			var record = this.list.getRecord(selections[0]);
			this.optionsPanel.setTorrent(record.get('info_hash'));
		} else {
			this.optionsPanel.files.setDisabled(true);
			this.optionsPanel.form.setDisabled(true);
		}
	},

	onShow: function() {
		if (!this.url) {
			this.url = new Deluge.add.UrlWindow();
			this.url.on('beforeadd', this.onTorrentBeforeAdd, this);
			this.url.on('add', this.onTorrentAdd, this);
			this.url.on('addfailed', this.onTorrentAddFailed, this);
		}

		if (!this.file) {
			this.file = new Deluge.add.FileWindow();
			this.file.on('beforeadd', this.onTorrentBeforeAdd, this);
			this.file.on('add', this.onTorrentAdd, this);
			this.file.on('addfailed', this.onTorrentAddFailed, this);
		}

		this.optionsPanel.form.getDefaults();
	},

	onTorrentBeforeAdd: function(torrentId, text) {
		var store = this.list.getStore();
		store.loadData([[torrentId, null, text]], true);
	},

	onTorrentAdd: function(torrentId, info) {
		var r = this.list.getStore().getById(torrentId);
		if (!info) {
			Ext.MessageBox.show({
				title: _('Error'),
				msg: _('Not a valid torrent'),
				buttons: Ext.MessageBox.OK,
				modal: false,
				icon: Ext.MessageBox.ERROR,
				iconCls: 'x-deluge-icon-error'
			});
			this.list.getStore().remove(r);
		} else {
			r.set('info_hash', info['info_hash']);
			r.set('text', info['name']);
			this.list.getStore().commitChanges();
			this.optionsPanel.addTorrent(info);
			this.list.select(r);
		}
	},

	onTorrentAddFailed: function(torrentId) {
		var store = this.list.getStore();
		var torrentRecord = store.getById(torrentId);
		if (torrentRecord) {
			store.remove(torrentRecord);
		}
	},

	onUrl: function(button, event) {
		this.url.show();
	}
});
