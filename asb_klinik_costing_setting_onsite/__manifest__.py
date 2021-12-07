# -*- coding: utf-8 -*-
{
    'name'          :   "Master Setting Costing Onsite Klinik",

    'summary'       :   """
                        Module Master Setting Costing Onsite Klinik
                        """,

    'description'   :   """
                        Module Master Setting Costing Onsite Klinik
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
                        ],

    # always loaded
    'data'          :   [
                            'security/ir.model.access.csv',
                            'views/config_equipment_list_view.xml',
                            'views/config_team_member_view.xml',
                            'views/config_transportasi_akomodasi_view.xml',
                            'views/costing_setting_onsite_view.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
}
