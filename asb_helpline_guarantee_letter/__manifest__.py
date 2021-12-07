# -*- coding: utf-8 -*-
{
    'name': "Helpline Guarantee Letter",

    'summary': """Custom Helpline Guarantee Letter""",

    'description': """Custom Helpline Guarantee Letter for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'portal', 'asb_eclaim', 'asb_productivity_eclaim','asb_membership_member', 'asb_membership_member_limit', 'asb_membership_client', 'asb_membership', 'asb_master', 'asb_helpline', 'asb_helpline_call_record', 'asb_helpline_activity_log', 'asb_master_diagnosis', 'asb_master_provider', 'asb_master_benefit', 'asb_master_configuration_benefit'],
    'data': [
        'security/ir.model.access.csv',
        'reports/template_gl.xml',
        'reports/template_lmi.xml',
        'views/assets.xml',
        'views/master_practitioner_views.xml',
        'views/master_surgery_views.xml',
        'views/final_gl_views.xml',
        'views/decline_reason_views.xml',
        'views/claim_reject_views.xml',
        'views/preadmission_views.xml',
        'views/guarantee_letter_views.xml',
        'views/gl_template_views.xml',
        'views/call_record_views.xml',
        'views/res_company_views.xml',
        'views/case_history_views.xml',
        'views/provider_views.xml',
        'views/activity_log_views.xml',
        'views/member_limit_views.xml',
        'data/guarantee_letter_daily_fu.xml',
        'data/initial_gl_email_template.xml',
        'data/final_gl_email_template.xml',
        'wizard/confirm_send_email_views.xml'
    ],
    'qweb': [
        'static/src/xml/preadmission_dashboard_template.xml',
        'static/src/xml/guarantee_letter_dashboard_template.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
