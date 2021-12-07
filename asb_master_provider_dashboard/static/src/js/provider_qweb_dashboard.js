odoo.define('asb_master_provider_dashboard.provider_qweb_dashboard', function (require) {
    "use strict";
    var qweb = require('web.qweb');
    var view_registry = require('web.view_registry');
    var rpc = require('web.rpc');

    var CustomLineChart = qweb.Renderer.extend({
        init(parent, state, params){
            this._super.apply(this, arguments)
            this.subViewsFields = params.subViewmap
        },

        willStart() {
            // dijalankan setelah init
            const subviewParams = {
                modelName: "res.partner",
                useSampleModel: false,
                withButtons: false,
                withSearchPanel: false,
                withControlPanel: false,
                limit: 100000000,
            }
            subviewParams.searchQuery = {
                domain: [['provider', '=', true]],
            }

            // get view map dari view registri
            const GoogleMapView = view_registry.get("google_map");
            // create new objek dari view yang ditambahin
            const subViewmap = new GoogleMapView(this.subViewsFields["google_map"], subviewParams);
            // get controller dari view yang ditambahin
            const defMap = subViewmap.getController(this).then((controller) => {
                this.controllerMap = controller;
                return this.controllerMap.appendTo(document.createDocumentFragment());
            })
            return Promise.all([this._super.apply(this, arguments), defMap])

        },

        async _render() {
            await this._super.apply(this, arguments);
            this.active_id = this.state.context.active_id;
            this.render_jumlah_provider_chart(this.active_id);
            this.render_penambahan_jumlah_provider_chart(this.active_id);
            this.render_penambahan_rebate_chart(this.active_id);
            this.render_provider_base_location(this.active_id);

            this.$el.find('.map_view').html(this.controllerMap.$el)
        },

        render_jumlah_provider_chart: function (active_id) {
            rpc.query({
                model: 'res.partner',
                method: 'get_jumlah_provider',
                args: [active_id],
            }).then(function (result) {
                var ctx = document.getElementById("canvas").getContext('2d');
                var count = result.count;
                var labels = result.labels; // Add labels to array
                // End Defining data
                
                // Create Chart 
                if (window.myCharts1 != undefined)
                window.myCharts1.destroy();
                window.myCharts1 = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Jumlah Provider', // Name the series
                            data: count, // Specify the data values array
                            backgroundColor: '#FF5C58',
                            borderColor: '#FF5C58',
                            
                            borderWidth: 1, // Specify bar border width
                            type: 'line', // Set this data to a line chart
                            fill: false
                        },
                    ]
                },
                options: {
                    maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    title: {
                        display: true,
                        text: result.title,
                    },
                    scales: {
                        xAxes: [{
                            gridLines: {
                                drawOnChartArea: false
                            }
                        }],
                        yAxes: [{
                            gridLines: {
                                drawOnChartArea: false
                            }
                        }]
                    },
                    legend: { display: false },
                    responsive: false,
                    tooltips: {enabled: false},
                    animation: {
                        duration: 0.5,
                        onComplete: function () {
                            // render the value of the chart above the bar
                            // alert("idihhhh");
                            var ctx = this.chart.ctx;
                            ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, 'normal', Chart.defaults.global.defaultFontFamily);
                                    ctx.fillStyle = this.chart.config.options.defaultFontColor;
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'bottom';
                                    this.data.datasets.forEach(function (dataset) {
                                        for (var i = 0; i < dataset.data.length; i++) {
                                            var model = dataset._meta[Object.keys(dataset._meta)[0]].data[i]._model;
                                            ctx.fillText(dataset.data[i], model.x, model.y - 5);
                                        }
                                    });
                                }
                            }
                        },
                    });
                });
            },
        
        render_penambahan_jumlah_provider_chart: function (active_id) {
            rpc.query({
                model: 'res.partner',
                method: 'get_penambahan_jumlah_provider',
                args: [active_id],
            }).then(function (result) {
                var ctx_2 = document.getElementById("canvas2").getContext('2d');
                var count_2 = result.count;
                var labels_2 = result.labels; // Add labels to array
                // End Defining data

                // Create Chart 
                if (window.myCharts2 != undefined)
                    window.myCharts2.destroy();
                    window.myCharts2 = new Chart(ctx_2, {
                        type: 'line',
                        data: {
                            labels: labels_2,
                            datasets: [{
                                label: 'Penambahan Jumlah Provider', // Name the series
                                data: count_2, // Specify the data values array
                                backgroundColor: '#FF5C58',
                                borderColor: '#FF5C58',

                                borderWidth: 1, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            },
                            ]
                        },
                        options: {
                            maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                            title: {
                                display: true,
                                text: result.title,
                            },
                            scales: {
                                xAxes: [{
                                    gridLines: {
                                        drawOnChartArea: false
                                    }
                                }],
                                yAxes: [{
                                    gridLines: {
                                        drawOnChartArea: false
                                    }
                                }]
                            },
                            legend: { display: false },
                            responsive: false,
                            tooltips: { enabled: false },
                            animation: {
                                duration: 0.5,
                                onComplete: function () {
                                    // render the value of the chart above the bar
                                    // alert("idihhhh");
                                    var ctx = this.chart.ctx;
                                    ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, 'normal', Chart.defaults.global.defaultFontFamily);
                                    ctx.fillStyle = this.chart.config.options.defaultFontColor;
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'bottom';
                                    this.data.datasets.forEach(function (dataset) {
                                        for (var i = 0; i < dataset.data.length; i++) {
                                            var model = dataset._meta[Object.keys(dataset._meta)[0]].data[i]._model;
                                            ctx.fillText(dataset.data[i], model.x, model.y - 5);
                                        }
                                    });
                                }
                            }
                        }
                    });

                });
            },
        
        render_penambahan_rebate_chart: function (active_id) {
            rpc.query({
                model: 'res.partner',
                method: 'get_penambahan_rebate',
                args: [active_id],
            }).then(function (result) {
                var ctx_3 = document.getElementById("canvas3").getContext('2d');
                var count_3 = result.count;
                var labels_3 = result.labels; // Add labels to array
                // End Defining data

                // Create Chart 
                if (window.myCharts3 != undefined)
                    window.myCharts3.destroy();
                    window.myCharts3 = new Chart(ctx_3, {
                        type: 'line',
                        data: {
                            labels: labels_3,
                            datasets: [{
                                label: 'Penambahan Rebate', // Name the series
                                data: count_3, // Specify the data values array
                                backgroundColor: '#FF5C58',
                                borderColor: '#FF5C58',

                                borderWidth: 1, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            },
                            ]
                        },
                        options: {
                            maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                            title: {
                                display: true,
                                text: result.title,
                            },
                            scales: {
                                xAxes: [{
                                    gridLines: {
                                        drawOnChartArea: false
                                    }
                                }],
                                yAxes: [{
                                    gridLines: {
                                        drawOnChartArea: false
                                    }
                                }]
                            },
                            legend: {display: false},
                            responsive: false,
                            tooltips: { enabled: false },
                            animation: {
                                duration: 100,
                                onComplete: function () {
                                    // render the value of the chart above the bar
                                    // alert("idihhhh");
                                    var ctx = this.chart.ctx;
                                    ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, 'normal', Chart.defaults.global.defaultFontFamily);
                                    ctx.fillStyle = this.chart.config.options.defaultFontColor;
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'bottom';
                                    this.data.datasets.forEach(function (dataset) {
                                        for (var i = 0; i < dataset.data.length; i++) {
                                            var model = dataset._meta[Object.keys(dataset._meta)[0]].data[i]._model;
                                            ctx.fillText(dataset.data[i], model.x, model.y - 5);
                                        }
                                    });
                                }
                            }
                        }
                    });
                });
            },
        
        render_provider_base_location: function (active_id) {
            rpc.query({
                model: 'res.partner',
                method: 'get_provider_base_location',
                args: [active_id],
            }).then(function (result) {
                var ctx_4 = document.getElementById("canvas4").getContext('2d');
                var count_4 = result.count;
                var labels_4 = result.labels;
                var barColors = result.barColors; // Add labels to array
                // End Defining data

                // Create Chart 
                if (window.myCharts4 != undefined)
                    window.myCharts4.destroy();
                    window.myCharts4 = new Chart(ctx_4, {
                        // type: 'line',
                        type: "pie",
                        data: {
                            labels: labels_4,
                            datasets: [{
                                backgroundColor: barColors,
                                data: count_4
                            }]
                        },
                        options: {
                            title: {
                                display: true,
                                text: result.title,
                            },
                            responsive: false,
                        }
                    });
                });
            },


    });

    var QwebProviderController = qweb.Controller.extend({
        events: _.extend({}, qweb.Controller.prototype.events, {
            'click .o_dashboard_action': '_onClickProviderQwebDashboard',
        }),

        _onClickProviderQwebDashboard(ev) {
            var $action = $(ev.currentTarget);
            return this.do_action($action.attr('name'),
                { additional_context: JSON.parse($action.attr('context')) });
        },
        
    });

    var QwebProviderView = qweb.View.extend({
        config: _.extend({}, qweb.View.prototype.config, {
            Controller: QwebProviderController,
            Renderer: CustomLineChart,
        }),
        withSearchBar: false,

        // ambil data google map (semacam request api)
        _loadData(model){
            const loadViewsMap = model.loadViews("res.partner", {}, [[false, 'google_map']])
                                .then( viewFields => {
                                    this.rendererParams.subViewmap = viewFields
                                })
            return Promise.all([this._super.apply(this, arguments), loadViewsMap])
                                .then( results => results[0])
        },


    })

    view_registry.add('QwebProvider', QwebProviderView);

});