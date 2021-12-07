# -*- coding: utf-8 -*-
{
    'name'          : 'Doctor Umum Nilai Skor',
    'version'       : '0.1',
    'author'        : 'PT Arkana Solusi Bisnis',
    'license'       : 'OPL-1',
    'category'      : 'Doctor Nilai Skor',
    'website'       : 'http://www.arkana.co.id',
    'summary'       : 'Custom Doctor Nilai Skor',
    'description'   :   '''
                            Custom Doctor : Nilai Skor Module for Medika
                        ''',
    'depends'       : [ 
                        'base', 
                        'mail', 
                        'portal',
                        'asb_klinik_doctor_umum_antrian_pasien', 
                      ],
    'data'          : [
                        # 'security/ir.model.access.csv',
                        'views/asb_docktor_umum_nilai_skor_views.xml',
                      ],
    'installable'   : True,
    'auto_install'  : False,
    'application'   : False,
}
