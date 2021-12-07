# -*- coding: utf-8 -*-
{
    'name'          :   "Master Ketenagaan Klinik",

    'summary'       :   """
                        Module Master Ketenagaan Klinik
                        """,

    'description'   :   """
                        Module Master Ketenagaan Klinik
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
                            'asb_klinik_master_personil'
                        ],

    # always loaded
    'data'          :   [
                            'security/ir.model.access.csv',
                            'data/master_ketenagaan_data.xml',
                            'views/master_ketenagaan_view.xml',
                            'views/res_users_view.xml'
                        ],
    'installable'   : True,
    'auto_install'  : False,
}
