# -*- coding: utf-8 -*-
{
    'name': "Helpline Call Record",

    'summary': """Custom Helpline Call Record""",

    'description': """Custom Helpline Call Record for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail','portal', 'asb_membership_member', 'asb_membership_client', 'asb_membership', 'asb_master_provider', 'asb_helpline_issued', 'asb_helpline'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'data/source_data.xml',
        'views/source_views.xml',
        'views/call_record_views.xml',
    ],
    'qweb': [
        'static/src/xml/call_record_dashboard_template.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
