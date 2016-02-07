

Deluge.SearchGrid = Ext.extend(Ext.grid.GridPanel, {
    title: 'Search Results',
    columns: [
        {
            //id:'name'
            header: _('Name'),
            width: 350,
            dataIndex: 'name'
        },{
            header: _('Size'),
            width: 75,
            dataIndex: 'size'
        },{
            header: _('Date Uploaded'),
            width: 90,
            dataIndex: 'date'
        },{
            header: _('Uploader'),
            width: 100,
            dataIndex: 'uploader'
        },{
            header: _('Seeds'),
            width: 60,
            dataIndex: 'seeds'
        },{
            header: _('Leechers'),
            width: 60,
            dataIndex: 'leechers'
        }
    ],

    height: 100,
    width: 200,
   
    
});

