odoo.define('asb_helpline_monitoring_detail_chart.BillingChart', function (require) {
    'use strict';
    // console.log('helpline case monitoring js custom');

    var view_registry = require('web.view_registry');
    var rpc = require('web.rpc');
    var qweb = require('web.qweb');

    var BillingChart = qweb.Renderer.extend({
        async _render() {
            await this._super.apply(this, arguments);
            this.active_id = this.state.context.active_id;
            this.render_billing_chart(this.active_id);
        },

        render_billing_chart: function (active_id) {
            var self = this;
            rpc.query({
                model: 'guarantee.letter',
                method: 'get_billing_data',
                args: [active_id],
            }).then(function (result) {
                var ctx = document.getElementById("canvas_billing").getContext('2d');

                // Define the data
                var billing = result.billing;

                var labels = result.labels; // Add labels to array
                // End Defining data

                // Create Chart for General Condition
                if (window.myCharts1 != undefined)
                    window.myCharts1.destroy();
                window.myCharts1 = new Chart(ctx, {
                    //var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'billing', // Name the series
                            data: billing, // Specify the data values array
                            backgroundColor: '#FF5C58',
                            borderColor: '#FF5C58',

                            borderWidth: 1, // Specify bar border width
                            type: 'line', // Set this data to a line chart
                            fill: false
                        }]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        title: {
                            display: true,
                            text: result.title,
                        },
                        scales: {
                            yAxes: [{
                                ticks: {
                                    callback: function (tick) {
                                        return result.currency_label + ' ' + tick.toLocaleString();
                                    }
                                },
                            }],
                            xAxes: [{
                                offset: true
                            }]
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                            // bodyFontColor: 'rgba(0,0,0,1)',
                            // titleFontSize: 13,
                            // titleFontColor: 'rgba(0,0,0,1)',
                            // backgroundColor: 'rgba(255,255,255,0.6)',
                            // borderColor: 'rgba(0,0,0,0.2)',
                            // borderWidth: 2,
                            callbacks: {
                                label: function (tooltipItem, data) {
                                    var val_tooltip = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                                    return "Billing : " + result.currency_label + ". " + val_tooltip.toLocaleString();
                                }
                            },
                        }
                    }
                });
            });
        },

    });

    var QwebBillingView = qweb.View.extend({
        config: _.extend({}, qweb.View.prototype.config, {
            Renderer: BillingChart,
        }),

        withSearchBar: false,
    })

    view_registry.add('billing_chart', QwebBillingView);

    return BillingChart;

});