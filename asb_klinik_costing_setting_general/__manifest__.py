# -*- coding: utf-8 -*-
{
    'name'          :   "Master Setting Costing General Klinik",

    'summary'       :   """
                        Module Master Setting Costing General Klinik
                        """,

    'description'   :   """
                        Module Master Setting Costing General Klinik
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
                            'product',
                            'asb_klinik_costing_team',
                            'asb_klinik_master_cost_allocation',
                            'asb_klinik_master_product',
                        ],

    # always loaded
    'data'          :   [
                            'security/ir.model.access.csv',
                            'views/costing_setting_general_view.xml',
                            'views/config_certificate_list_view.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
}
