from odoo import _, api, fields, models, tools, SUPERUSER_ID
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
import mysql.connector
import re

class LabMySQLConnect(models.AbstractModel):
    _name           = 'lab.mysql.connect'
    _description    = 'Lab Mysql Connect'
    
    def _initConn(self):
        database_username = self.env['ir.config_parameter'].sudo().get_param('login_mariadb_user')
        database_password = self.env['ir.config_parameter'].sudo().get_param('login_mariadb_password')
        database_name = self.env['ir.config_parameter'].sudo().get_param('login_mariadb_database')
        port = self.env['ir.config_parameter'].sudo().get_param('login_mariadb_port')
        localhost = self.env['ir.config_parameter'].sudo().get_param('login_mariadb_host')
        
        return database_username, database_password, database_name, port, localhost
    
    def _get_authentication(self):
        database_username, database_password, database_name, port, localhost = self._initConn()
        global connection
        
        connection = mysql.connector.connect(
            user=database_username,
            password=database_password,
            host=localhost,
            port=port,
            database=database_name,
        )
        
        return connection
        
    def _check_data_to_mysql(self, vals):
        connection      = self._get_authentication()
        cursor          = connection.cursor()
        
        data_examination    = []
        if vals['examination_list_ids']:
            for record in vals['examination_list_ids']:
                examination_ids     = self.env['product.product'].sudo().search([('is_service', '=', True)]).filtered(lambda r: record in r.ids)
                if examination_ids.kode_lis == False and re.search('Laborator', str(examination_ids.poli_unit_id.nama_poli_unit), re.IGNORECASE):
                    raise ValidationError("Tindakan Laboratorium yang didaftarkan tidak memiliki Kode LIS")
                if examination_ids.kode_lis != False and re.search('Laborator', str(examination_ids.poli_unit_id.nama_poli_unit), re.IGNORECASE):
                    data_examination    += [(rec.kode_lis, rec.name) for rec in examination_ids if examination_ids]
        
        order_testid        = '~'.join(list(map("^".join, data_examination))) if data_examination else None
        clinician           = "{0}^{1}".format(vals['kode'], vals['nama_dokter']) if vals['kode'] and vals['nama_dokter'] else None
        jenis_kelamin       = 1 if vals['jenis_kelamin'] == 'laki' else 2 if vals['jenis_kelamin'] == 'perempuan' else 0
        tanggal_registrasi  = vals['tanggal_registrasi']
        tanggal_lahir       = vals['tanggal_lahir']
        kelurahan_kecamatan = "{0}, {1}".format(vals['kelurahan_name'], vals['kecamatan_name']) if vals['kelurahan_name'] and vals['kecamatan_name'] else None
        kota_provinsi       = "{0}, {1}".format(vals['city_name'], vals['state_name']) if vals['city_name'] and vals['state_name'] else None
                
        cursor.execute("SELECT ONO FROM lis_order WHERE ONO = '{}'".format(vals['name']))
        result = cursor.fetchall()        
        
        update              = ( "UPDATE lis_order SET "
                                "PID = %(PID)s, PNAME = %(PNAME)s,  ADDRESS1 = %(ADDRESS1)s, ADDRESS2 = %(ADDRESS2)s, ADDRESS3 =  %(ADDRESS3)s, ADDRESS4 = %(ADDRESS4)s,"
                                "SEX = %(SEX)s, ORDER_CONTROL = %(ORDER_CONTROL)s, PTYPE = %(PTYPE)s, BIRTH_DT = %(BIRTH_DT)s, REQUEST_DT = %(REQUEST_DT)s,"
                                "PRIORITY = %(PRIORITY)s, VISITNO = %(VISITNO)s, CLINICIAN = %(CLINICIAN)s, ORDER_TESTID = %(ORDER_TESTID)s " 
                                "WHERE ONO = %(ONO)s")
        
        create              = ( "INSERT INTO lis_order "
                                "(PID, PNAME, ADDRESS1, ADDRESS2, ADDRESS3, ADDRESS4, SEX, ORDER_CONTROL, PTYPE, BIRTH_DT, ONO, REQUEST_DT, PRIORITY, VISITNO, CLINICIAN, ORDER_TESTID) "
                                "VALUES (%(PID)s, %(PNAME)s, %(ADDRESS1)s, %(ADDRESS2)s, %(ADDRESS3)s, %(ADDRESS4)s, %(SEX)s, %(ORDER_CONTROL)s, %(PTYPE)s, %(BIRTH_DT)s, %(ONO)s, %(REQUEST_DT)s, %(PRIORITY)s, %(VISITNO)s, %(CLINICIAN)s, %(ORDER_TESTID)s)")
        
        data_pasien = { 
            'ORDER_CONTROL' : 'NW', 'PTYPE' : 'OP', 'PRIORITY' : 'R', 'SEX' : jenis_kelamin, 'BIRTH_DT' : tanggal_lahir,
            'REQUEST_DT' : tanggal_registrasi, 'CLINICIAN' : clinician, 'ORDER_TESTID' : order_testid, 'PID' : vals['no_medical_report'],
            'PNAME' : vals['display_name'], 'ADDRESS1' : vals['street'], 'ADDRESS2' : kelurahan_kecamatan, 'ADDRESS3' : kota_provinsi,
            'ADDRESS4' : vals['country_name'], 'ONO' : vals['name'], 'VISITNO' : vals['name'],
        }
                        
        if result:
            cursor.execute(update, data_pasien)
            connection.commit()
            cursor.close()
            connection.close()
        else:
            cursor.execute(create, data_pasien)
            connection.commit()
            cursor.close()
            connection.close()
    
    def _update_data_to_mysql(self, vals):
        connection       = self._get_authentication()
        cursor           = connection.cursor(buffered=True, dictionary=True)
        ono              = vals['ONO'][0] if vals['ONO'] else 0
        order_testid_val = vals['id_product'] if vals['id_product'] else 0
        data_examination = []
        
        if order_testid_val != 0:
            for record in order_testid_val:
                examination_ids     = self.env['product.product'].sudo().search([('is_service', '=', True)]).filtered(lambda r: record in r.ids)
                data_examination    += [(rec.kode_lis, rec.name) for rec in examination_ids if examination_ids]
        
        order_testid = '~'.join(list(map("^".join, data_examination)))
        cursor.execute("SELECT ONO, ORDER_TESTID FROM lis_order WHERE ONO = '{}'".format(ono))
        result = cursor.fetchall()
        
        if result:
            if result[0]['ORDER_TESTID'] == None:
                cursor.execute("UPDATE lis_order SET ORDER_TESTID = '{1}' WHERE ONO = '{0}'".format(ono, order_testid))
                connection.commit()
                cursor.close()
                connection.close()
            elif result[0]['ORDER_TESTID'] != None:
                if order_testid == result[0]['ORDER_TESTID']:
                    pass
                else:
                    cursor.execute("UPDATE lis_order SET ORDER_TESTID = '{1}', ORDER_CONTROL = 'RP' WHERE ONO = '{0}'".format(ono, order_testid))
                    connection.commit()
                    cursor.close()
                    connection.close()
            else:
                pass
                
        cursor.close()
        connection.close()
        
    def _update_null_lab_to_mysql(self, vals):
        connection  = self._get_authentication()
        cursor      = connection.cursor(buffered=True, dictionary=True)
        ono         = vals['ONO'] if vals['ONO'] else 0
        
        cursor.execute("SELECT ONO, ORDER_TESTID FROM lis_order WHERE ONO = '{}'".format(ono))
        result = cursor.fetchall()
        
        if result:
            if result[0]['ORDER_TESTID'] != None:
                cursor.execute("UPDATE lis_order SET ORDER_TESTID = NULL, ORDER_CONTROL = 'NW' WHERE ONO = '{}'".format(ono))
                connection.commit()
                cursor.close()
                connection.close()
            else:
                pass
        
        cursor.close()
        connection.close()
    