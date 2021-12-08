odoo.define('asb_master_provider_activity.filter_button', function (require) {
    "use strict";
    
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry')

    var ExportListController = ListController.extend({
        events: _.extend({}, ListController.prototype.events, {
            'click .oe_filter_button': '_onClickExport',
        }),

        _onClickExport: function() {
            var self = this;
            self.do_action({
                name: 'Export Provider Activity',
                type: 'ir.actions.act_window',
                res_model: 'export.provider.activity',
                target: 'new',
                views: [[false, 'form']],
            });
        },
    });

    var ExportListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: ExportListController,
        }),
    });

    view_registry.add('export_button', ExportListView);

})