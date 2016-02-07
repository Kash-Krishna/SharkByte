

Deluge.SearchGrid = Ext.extend(Ext.grid.GridPanel, {
    title: 'Search Results',
    columns: [
        {
            header: _('Name'),
            dataIndex: 'name'
        },{
            header: _('Size'),
            dataIndex: 'size'
        }
    ],

    height: 300,
    width: 500
    
});

