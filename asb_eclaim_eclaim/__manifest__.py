# -*- coding: utf-8 -*-
{
    'name': "E-Claim",

    'summary': """Custom E-Claim""",

    'description': """Custom E-Claim for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_eclaim', 'asb_master_provider', 'asb_eclaim_document', 'asb_eclaim_item', 'asb_helpline_guarantee_letter', 'asb_membership_client', 'asb_membership_member', 'asb_binary_newtab', 'mail', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        # 'wizard/eclaim_wizard_views.xml',
        'views/eclaim_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
