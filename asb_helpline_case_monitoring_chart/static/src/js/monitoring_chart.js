odoo.define('asb_helpline_case_monitoring_chart.MonitoringChart', function (require) {
    'use strict';
    // console.log('helpline case monitoring js custom');

    var view_registry = require('web.view_registry');
    var rpc = require('web.rpc');
    var qweb = require('web.qweb');

    var MonitoringChart = qweb.Renderer.extend({
        async _render() {
            await this._super.apply(this, arguments);
            this.active_id = this.state.context.active_id;
            this.render_case_monitoring_chart(this.active_id);
        },

        render_case_monitoring_chart: function (active_id) {
            var self = this;
            rpc.query({
                model: 'case.monitoring',
                method: 'get_monitoring_detail_data',
                args: [active_id],
            }).then(function (result) {
                var ctx = document.getElementById("canvas_monitoring").getContext('2d');

                // Define the data
                var sistole = result.sistole;
                var diastole = result.diastole;
                var temperature = result.temperature;
                var heart_rate = result.heart_rate;
                var respiratory_rate = result.respiratory_rate;

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
                            label: 'Sistole', // Name the series
                            data: sistole, // Specify the data values array
                            backgroundColor: '#FF5C58',
                            borderColor: '#FF5C58',

                            borderWidth: 1, // Specify bar border width
                            type: 'line', // Set this data to a line chart
                            fill: false
                        },
                        {
                            label: 'Diastole', // Name the series
                            data: diastole, // Specify the data values array
                            backgroundColor: '#14279B',
                            borderColor: '#14279B',

                            borderWidth: 1, // Specify bar border width
                            type: 'line', // Set this data to a line chart
                            fill: false
                        },
                        {
                            label: 'Temperature', // Name the series
                            data: temperature, // Specify the data values array
                            backgroundColor: '#77D970',
                            borderColor: '#77D970',

                            borderWidth: 1, // Specify bar border width
                            type: 'line', // Set this data to a line chart
                            fill: false
                        },
                        {
                            label: 'Heart Rate', // Name the series
                            data: heart_rate, // Specify the data values array
                            backgroundColor: '#FEE440',
                            borderColor: '#FEE440',

                            borderWidth: 1, // Specify bar border width
                            type: 'line', // Set this data to a line chart
                            fill: false
                        },
                        {
                            label: 'Respiratory Rate', // Name the series
                            data: respiratory_rate, // Specify the data values array
                            backgroundColor: '#664E88',
                            borderColor: '#664E88',

                            borderWidth: 1, // Specify bar border width
                            type: 'line', // Set this data to a line chart
                            fill: false
                        },
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        title: {
                            display: true,
                            text: result.title,
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
                            // callbacks: {
                            //     label: function (tooltipItem, data) {
                            //         var val_tooltip = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                            //         return result.currency_label + " : " + val_tooltip.toLocaleString();
                            //     }
                            // },
                        }
                    }
                });
            });
        },

    });

    var QwebMonitoringView = qweb.View.extend({
        config: _.extend({}, qweb.View.prototype.config, {
            Renderer: MonitoringChart,
        }),

        withSearchBar: false,
    })

    view_registry.add('monitoring_chart', QwebMonitoringView);

    return MonitoringChart;

});