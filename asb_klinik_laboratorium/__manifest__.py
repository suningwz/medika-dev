# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
{
    'name'          : 'Laboratorium Klinik',
    'version'       : '0.1',
    'author'        : 'PT Arkana Solusi Bisnis',
    'license'       : 'OPL-1',
    'category'      : 'Antrian Pasien Laboratorium Klinik',
    'website'       : 'http://www.arkana.co.id',
    'summary'       : 'Custom Antrian Pasien Laboratorium Klinik',
    'description'   :   '''
                            Custom Antrian Pasien Laboratorium Klinik Module for Medika
                        ''',
    'depends'       : [
                        'base',
                        'mail',
                        'portal',
                        'product',
                        'asb_klinik_master_data_klinik',
                        'asb_klinik_costing',
                        'asb_klinik_admission',
                        'asb_klinik_admission_poli_perawat',
                        'asb_klinik_doctor',
                      ],

    'data'          : [
                        'security/laboratorium_security.xml',
                        'views/antrian_laboratorium_views.xml',
                      ],
    'installable'   : True,
    'auto_install'  : False,
    'application'   : False,
}