# -*- coding: utf-8 -*-
{
    'name'          :   "Master Cost Allocation Klinik",

    'summary'       :   """
                        Module Master Cost Allocation Klinik
                        """,

    'description'   :   """
                        Module Master Cost Allocation Klinik
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
                            'security/ir.model.access.csv',
                            'views/master_cost_allocation_view.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
}
