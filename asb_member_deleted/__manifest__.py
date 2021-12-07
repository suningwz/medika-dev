# -*- coding: utf-8 -*-
{
    'name': "Member Deleted",
    'summary': "Custom Member Deleted",
    'description': "This menu used to save member deleted",
    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_master', 'asb_membership', 'asb_membership_member', 'mail', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/remarks_member_deleted_views.xml',
        'views/member_deleted_views.xml'
    ],
}