# -*- coding: utf-8 -*-
{
    'name': "Helpline Case Monitoring Chart",

    'summary': """Custom Helpline Helpline Case Monitoring Chart""",

    'description': """Custom Helpline Helpline Case Monitoring Chart for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_helpline_case_monitoring', 'web'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/assets_load.xml',
        'views/case_monitoring_views.xml',
        'views/case_monitoring_chart_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
