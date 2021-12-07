# -*- coding: utf-8 -*-
{
    'name': "Helpline Preadmission",

    'summary': """Custom Helpline Preadmission""",

    'description': """Custom Helpline Preadmission for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail','portal', 'web', 'asb_membership_member','asb_membership_client', 'asb_membership', 'asb_master', 'asb_helpline_call_record'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/preadmission_views.xml',
        'views/call_record_views.xml',
    ],
    'qweb': [
        'static/src/xml/preadmission_dashboard_template.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
