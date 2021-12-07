# -*- coding: utf-8 -*-
{
    'name': "Membership Member Limit",

    'summary': """
        Custom Membership Member Limit""",

    'description': """
        Custom Membership Member Limit for PT. Medika Plaza
    """,

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    # 'depends': ['base', 'asb_membership_member', 'asb_helpline_guarantee_letter', 'hr_expense'],
    'depends': ['base', 'asb_membership_member', 'asb_helpline_call_record'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/member_views.xml',
        # 'views/guarantee_letter_views.xml',
        'views/call_record_views.xml',
    ],
    'qweb': [
        'static/src/xml/membership_member_limit_dashboard.xml',
    ],
    'installable': True,
    'application': True,
}
