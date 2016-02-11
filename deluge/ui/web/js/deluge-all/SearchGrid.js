

var searchStore = Ext.create(Ext.data.Store, {
    //storeId: 'searchData',
    
    fields: [
        'name',// type: 'string'},
        'size'/*, type: 'number'},
        {name: 'date', type: 'date'},
        {name: 'uploader', type: 'string'},
        {name: 'seeds', type: 'number'},
        {name: 'leechers', type: 'number'}*/
    ],
    data: [ 
        {name: "PoI", size: "1.2"},
        //, date: '2014/09/24', uploader: 'YIFY', seeds: 300, leechers: 4721},
        {name: "Thor", size: "3.2"},
        //, date: '2013/04/04', uploader: 'Extr', seeds: 109, leechers: 421},
        {name: "Up", size: "3.5"}
        //, date: '2012/010/14', uploader: 'YIFY', seeds: 299, leechers: 4701}
    ]
 
});

function nameRenderer(value){
    return "PoI";
}

Deluge.SearchGrid = Ext.extend(Ext.grid.GridPanel, {
    
    store: searchStore,
    stateful: true,
    columns: [
        {
            //id:'name'
            header: _('Name'),
            width: 350,
            dataIndex: 'name',
            sortable: true,
            renderer: nameRenderer,
            flex: 1
        },{
            header: _('Size'),
            width: 75,
            dataIndex: 'size',
            sortable: true
            /*
        },{
            header: _('Date Uploaded'),
            width: 90,
            dataIndex: 'date',
            xtype: 'datecolumn',
            format: 'Y-m-d'
        },{
            header: _('Uploader'),
            width: 100,
            dataIndex: 'uploader'
        },{
            header: _('Seeds'),
            width: 60,
            dataIndex: 'seeds',
            xtype: 'numbercolumn',
            format: '0,000'
        },{
            header: _('Leechers'),
            width: 60,
            dataIndex: 'leechers',
            xtype: 'numbercolumn',
            format: '0,000'
*/
        }
    ],

    //renderTo: Ext.getBody(),

    constructor: function(config) {
        config = Ext.apply({
            //id: 'searchGrid',
            store: searchStore,
            columns: this.columns,
            region: 'center',
            stripeRows: true            
            //autoExpandColumn: 'name',
			//autoExpandMin: 150,
            //margins: '5 5 0 0'
/*
            view: new Ext.ux.grid.BufferView({
                rowHeight: 26,
                scrollDelay: false
            })
*/
        }, config);

        Deluge.SearchGrid.superclass.constructor.call(this,config);
         //this.getStore().loadData(this.data);
    },
    initComponent: function() {
        Deluge.SearchGrid.superclass.initComponent.call(this);  
    }
   
       
});

