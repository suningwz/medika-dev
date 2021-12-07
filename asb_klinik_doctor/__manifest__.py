# -*- coding: utf-8 -*-
{
    'name'          : 'Doctor',
    'version'       : '0.1',
    'author'        : 'PT Arkana Solusi Bisnis',
    'license'       : 'OPL-1',
    'category'      : 'Doctor',
    'website'       : 'http://www.arkana.co.id',
    'summary'       : 'Custom Doctor',
    'description'   :   '''
                            Custom Doctor Module for Medika
                        ''',
    'depends'       : [
                        'base', 
                        'mail', 
                        'portal',
                        'asb_klinik_doctor_team',
                        'asb_klinik_doctor_umum_antrian_pasien',
                        'asb_klinik_doctor_gigi_antrian_pasien',
                        'asb_klinik_doctor_mata_antrian_pasien',
                        'asb_klinik_doctor_jantung_antrian_pasien',
                        'asb_klinik_doctor_umum_configuration_anamnesa',
                        'asb_klinik_doctor_umum_configuration_pemeriksaan_fisik',
                        'asb_klinik_doctor_umum_resep_obat',
                        'asb_klinik_doctor_umum_biaya_mc',
                        'asb_klinik_doctor_umum_nilai_skor',
                      ],
    'data'          : [
                        'views/doctor_views.xml',
                      ],
    'installable'   : True,
    'auto_install'  : False,
    'application'   : True,
}
