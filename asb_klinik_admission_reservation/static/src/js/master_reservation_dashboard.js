odoo.define('asb_klinik_admission_reservation.master_reservation_dashboard', function (require) {
"use strict";

var core            = require('web.core');
var ListController  = require('web.ListController');
var ListModel       = require('web.ListModel');
var ListRenderer    = require('web.ListRenderer');
var ListView        = require('web.ListView');
var SampleServer    = require('web.SampleServer');
var view_registry   = require('web.view_registry');
var QWeb            = core.qweb;

let dashboardValues;
SampleServer.mockRegistry.add('master.reservation/retrieve_dashboard', () => {
    return Object.assign({}, dashboardValues);
});

//--------------------------------------------------------------------------
// List View
//--------------------------------------------------------------------------

var ReservationListDashboardController = ListController.extend({

    custom_events: _.extend({}, ListController.prototype.custom_events, {
        dashboard_open_action: '_onDashboardOpenAction',
    }),

    _onDashboardOpenAction: function (e) {
        return this.do_action(e.data.action_name,
            {additional_context: JSON.parse(e.data.action_context)});
    },

});

var ReservationListDashboardRenderer = ListRenderer.extend({

    events:_.extend({}, ListRenderer.prototype.events, {
        'click .o_reservation_action': '_onDashboardActionClicked',
    }),

    _renderView: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            var values = self.state.dashboardValues;
            var reservation_dashboard = QWeb.render('asb_klinik_admission_reservation.ReservationDashboard', {
                values: values,
            });
            self.$el.prepend(reservation_dashboard);
        });
    },

    _onDashboardActionClicked: function (e) {
        e.preventDefault();
        var $action = $(e.currentTarget);
        this.trigger_up('dashboard_open_action', {
            action_name: $action.attr('name')+"_list",
            action_context: $action.attr('context'),
        });
    },

});

var ReservationListDashboardModel = ListModel.extend({

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
            model: 'master.reservation',
            method: 'retrieve_dashboard',
        });
        return Promise.all([super_def, dashboard_def]).then(function(results) {
            var id = results[0];
            dashboardValues = results[1];
            self.dashboardValues[id] = dashboardValues;
            return id;
        });
    },

});

var ReservationListDashboardView = ListView.extend({

    config: _.extend({}, ListView.prototype.config, {
        Model : ReservationListDashboardModel,
        Renderer : ReservationListDashboardRenderer,
        Controller : ReservationListDashboardController,
    }),

});

view_registry.add('master_reservation_list_dashboard', ReservationListDashboardView);

});
