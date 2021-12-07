# -*- coding: utf-8 -*-
{
    'name': "Helpline Case Monitoring Chart",

    'summary': """Custom Helpline Helpline Case Monitoring Chart""",

    'description': """Custom Helpline Helpline Case Monitoring Chart for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['web', 'base', 'asb_helpline_guarantee_letter', 'asb_helpline_monitoring_detail', 'web'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/assets_load.xml',
        'views/monitoring_detail_views.xml',
        'views/monitoring_detail_chart_views.xml',
        'views/billing_chart_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
