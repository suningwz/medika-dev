# -*- coding: utf-8 -*-
{
    'name': "Payment Finance",

    'summary': """Custom Payment Finance""",

    'description': """Custom Payment Finance for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'portal', 'asb_payment', 'asb_eclaim_batch', 'asb_helpline_guarantee_letter', 'asb_master_provider'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/finance_views.xml',
        'views/payment_wizard_views.xml',
        'views/rebate_views.xml',
    ],
    # 'qweb': [
    #     'static/src/xml/eclaim_finance_dashboard_template.xml',
    # ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
