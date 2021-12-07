# -*- coding: utf-8 -*-
{
    'name': "Helpline Source",

    'summary': """Custom Helpline Source""",

    'description': """Custom Helpline Source for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_helpline', 'asb_helpline_call_record'],
    'data': [
        'security/ir.model.access.csv',
        'views/source_views.xml',
        'views/call_record_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
