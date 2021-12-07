{
    'name'          :   "Master Package Klinik",

    'summary'       :   """
                        Module Master Package Klinik
                        """,

    'description'   :   """
                        Module Master Package Klinik
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
                            'form_style_adjustment', 
                            'asb_klinik_costing_team',
                            'asb_klinik_master_personil',
                            'asb_klinik_costing_setting_general',
                            'asb_klinik_costing_setting_onsite',
                        ],

    # always loaded
    'data'          :   [
                            'security/ir.model.access.csv',
                            'data/list_package_mcu_data.xml',
                            'data/package_mcu_data.xml',
                            'views/examination_list_view_tree.xml',
                            'views/preview_list_package_mcu_view.xml',
                            'views/list_package_mcu_house_view.xml',
                            'views/list_package_mcu_onsite_view.xml',
                            'views/package_mcu_house_view.xml',
                            'views/package_mcu_onsite_view.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
}