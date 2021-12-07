# -*- coding: utf-8 -*-
{
    'name'          :   "Doctor Team Klinik",

    'summary'       :   """
                        Module Doctor Team Klinik
                        """,

    'description'   :   """
                        Module Doctor Team Klinik
                        """,

    'author'        :   "PT. Arkana Solusi Bisnis",
    'website'       :   "https://arkana.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category'      :   'Uncategorized',
    'version'       :   '0.1',

    # any module necessary for this one to work correctly
    'depends'       :   [
                            'base', 
                            'mail',
                        ],

    # always loaded
    'data'          :   [
                            'security/doctor_team_security.xml',
                            'security/ir.model.access.csv',
                            'views/views.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
}
