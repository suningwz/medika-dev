odoo.define('asb_eclaim_finance.eclaim_finance_dashboard', function (require) {
    "use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var ListModel = require('web.ListModel');
    var ListRenderer = require('web.ListRenderer');
    var ListView = require('web.ListView');
    var SampleServer = require('web.SampleServer');
    var view_registry = require('web.view_registry');
    var QWeb = core.qweb;

    let dashboardValues;
    SampleServer.mockRegistry.add('guarantee.letter/retrieve_eclaim_finance_dashboard', () => {
        return Object.assign({}, dashboardValues);
    });

    var EclaimFinanceListDashboardController = ListController.extend({
        custom_events: _.extend({}, ListController.prototype.custom_events, {
            dashboard_open_action: '_onDashboardOpenAction',
        }),
        _onDashboardOpenAction: function (e) {
            return this.do_action(e.data.action_name,
                { additional_context: JSON.parse(e.data.action_context) });
        },
    });

    var EclaimFinanceListDashboardRenderer = ListRenderer.extend({
        // events: _.extend({}, ListRenderer.prototype.events, {
        //     'click .o_dashboard_action': '_onDashboardActionClicked',
        // }),
        _renderView: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                var values = self.state.dashboardValues;
                self.$el.parent().find('.o_eclaim_finance_dashboard').remove()
                var eclaim_finance_dashboard = $(QWeb.render('asb_eclaim_finance.EclaimFinanceDashboard', {
                    values: values,
                }));
                eclaim_finance_dashboard.find('.o_dashboard_action').on('click', self._onDashboardActionClicked.bind(self))
                self.$el.before(eclaim_finance_dashboard);
            });
        },

        _onDashboardActionClicked: function (e) {
            e.preventDefault();
            console.log(this)
            var $action = $(e.currentTarget);
            this.trigger_up('dashboard_open_action', {
                // action_name: $action.attr('name') + "_list",
                action_name: $action.attr('name'),
                action_context: $action.attr('context'),
            });
        },
    });


    var EclaimFinanceListDashboardModel = ListModel.extend({
        init: function () {
            this.dashboardValues = {};
            this._super.apply(this, arguments);
        },

        __get: function (localID) {
            var result = this._super.apply(this, arguments);
            if (_.isObject(result)) {
                result.dashboardValues = this.dashboardValues[localID];
            }
            return result;
        },

        __load: function () {
            return this._loadDashboard(this._super.apply(this, arguments));
        },

        __reload: function () {
            return this._loadDashboard(this._super.apply(this, arguments));
        },

        _loadDashboard: function (super_def) {
            var self = this;
            var dashboard_def = this._rpc({
                model: 'guarantee.letter',
                method: 'retrieve_eclaim_finance_dashboard',
            });
            return Promise.all([super_def, dashboard_def]).then(function (results) {
                var id = results[0];
                dashboardValues = results[1];
                self.dashboardValues[id] = dashboardValues;
                return id;
            });
        },
    });


    var EclaimFinanceListDashboardView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Model: EclaimFinanceListDashboardModel,
            Renderer: EclaimFinanceListDashboardRenderer,
            Controller: EclaimFinanceListDashboardController,
        }),

    });

    view_registry.add('eclaim_finance_list_dashboard', EclaimFinanceListDashboardView);

});