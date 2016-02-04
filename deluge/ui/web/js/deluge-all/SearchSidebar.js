

Deluge.SearchSidebar = Ext.extend(Ext.Panel, {

	// private
	panels: {},

	// private
	selected: null,

	constructor: function(config) {
		config = Ext.apply({
			id: 'searchsidebar',
			region: 'east',
			cls: 'deluge-sidebar',
			title: _('Search'),
			layout: 'accordion',
			split: true,
			width: 500,
			minSize: 100,
			collapsible: true,
			margins: '5 0 0 5',
			cmargins: '5 0 0 5'
		}, config);
		Deluge.SearchSidebar.superclass.constructor.call(this, config);
	}
});
