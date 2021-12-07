# -*- coding: utf-8 -*-
{
    'name'          :   "Master Costing Klinik",

    'summary'       :   """
                        Module Master Costing Klinik
                        """,

    'description'   :   """
                        Module Master Costing Klinik
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
                            'asb_klinik_costing_team',
                            'asb_klinik_costing_setting_general',
                            'asb_klinik_costing_setting_onsite',
                            'asb_klinik_costing_package',
                        ],

    # always loaded
    'data'          :   [
                            'security/ir.model.access.csv',
                            'views/views.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
    'application'   : True,
}
