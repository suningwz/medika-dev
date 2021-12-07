# -*- coding: utf-8 -*-
{
    'name'          :   "Master Dokumen Klinik",

    'summary'       :   """
                        Module Master Dokumen Klinik
                        """,

    'description'   :   """
                        Module Master Dokumen Klinik
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
                            'asb_state_city',
                        ],

    # always loaded
    'data'          :   [
                            'security/ir.model.access.csv',
                            'views/config_jenis_dokumen_view.xml',
                            'views/master_dokumen_view.xml',
                            'data/master_jenis_dokumen_data.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
}
