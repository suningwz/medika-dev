# -*- coding: utf-8 -*-
{
    'name': "Import Member",

    'summary': """
       Custom SQL Import Member""",

    'description': """
        Custom SQL Import Member
    """,

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_membership', 'asb_membership_member', 'asb_state_city'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_member_views.xml',
    ],
}
