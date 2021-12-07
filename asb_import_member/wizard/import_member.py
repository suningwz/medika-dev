from odoo import api, fields, models, _, tools, SUPERUSER_ID
from datetime import date, datetime
import os
import csv
import pandas as pd
import xlrd
import binascii
import tempfile
from odoo.modules import get_module_path
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

class ImportMember(models.TransientModel):
    _name = 'import.member'
    _description = 'Import Member'
    
    name = fields.Char(string='Import Member')
    upload_file = fields.Binary(string='File')
    preview_file = fields.One2many('preview.file', 'import_id', string='Preview')
    preview = fields.Boolean(string='Preview check')

    def read_file(self):
        if self.upload_file:
            fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.upload_file))  # Encode binary file to xlsx
            fp.seek(0)
            body = pd.read_excel(open(fp.name, 'rb'), 0, engine='openpyxl', header=0, na_filter=False, na_values=None, dtype=str)  # Open file xlsx with pandas
            body.fillna('')  # Default cell value
            df = pd.DataFrame(body)
            df = df.astype(str)
            return {
                'df_body': df
            }
        else:
            raise UserError(_("Please Upload a File"))

    
    @api.onchange('upload_file')
    def _onchange_upload_file(self):
        self.preview = False

    def preview_file_button(self):
        vals = [(5,0,0)]
        if self.upload_file:
            sheet = self.read_file()
            df = sheet['df_body']

            for rec in df.index:
                member_values = []

                # Get data from name column in excel

                record_mode = df['ENROLLMENT RECORD MODE'][rec]
                
                # Condition for skip process when value in excel empty
                if record_mode not in ('1','2','3','4','5','6','7','8','9','10','11','12','13'):
                    raise ValidationError(_("Invalid record mode at row %s") % (rec+2))

                record_type = df['RECORD TYPE'][rec]
                payor_id = df['PAYOR ID'][rec]
                company_id = df['COMPANY ID'][rec]
                entity_id = df['ENTITY ID'][rec]
                policy_number = df['POLICY NUMBER'][rec]
                nik = df['NIK'][rec]
                card_number = df['CARD NUMBER'][rec]
                member_number = df['MEMBER NUMBER'][rec]
                suffix_id = df['SUFFIX ID'][rec]
                member_name = df['MEMBER NAME'][rec]
                dob = df['DOB'][rec]
                gender = df['GENDER'][rec]
                join_date = df['JOIN DATE'][rec]
                start_date = df['START DATE'][rec]
                effective_date = df['EFFECTIVE DATE'][rec]
                end_date = df['END DATE'][rec]
                end_policy_date = df['END POLICY DATE'][rec]
                # ip = df['IP'][rec]
                # op = df['OP'][rec]
                # de = df['DE'][rec]
                # eg = df['EG'][rec]
                # ma = df['MA'][rec]
                # mcu = df['MCU'][rec]
                # ot = df['OT'][rec]
                program = df['PROGRAM'][rec]
                plan = df['PLAN'][rec]
                division = df['DIVISION'][rec]
                division_code = df['DIVISION CODE'][rec]
                bank_code = df['BANK CODE'][rec]
                bank_name = df['BANK NAME'][rec]
                account_number = df['ACCOUNT NUMBER'][rec]
                account_name = df['ACCOUNT NAME'][rec]
                bank_branch = df['BANK BRANCH'][rec]
                # rule_bpjs = df['RULE BPJS'][rec]
                # record_type = df['BPJS NUMBER'][rec]
                # record_type = df['CLASSES ROOM OF BPJS PARTICIPANTS  '][rec]
                # record_type = df['NAMES FASKES FKTP  '][rec]
                language = df['LANGUAGE'][rec]
                marital_status = df['MARITAL STATUS'][rec]
                relationship = df['RELATIONSHIP'][rec]
                employee_address = df['EMPLOYEE ADDRESS'][rec]
                address2 = df['ADDRESS2'][rec]
                # record_type = df['ADDRESS3'][rec]
                # record_type = df['ADDRESS4'][rec]
                city = df['CITY'][rec]
                state = df['STATE'][rec]
                postcode = df['POST CODE'][rec]
                telephone_office = df['TELEPHONE – OFFICE'][rec]
                telephone_resident = df['TELEPHONE – RESIDENT'][rec]
                telephone_mobile = df['TELEPHONE - MOBILE'][rec]
                nomor_ktp = df['NOMOR KTP'][rec]
                passport_number = df['PASSPORT NUMBER'][rec]
                passport_country = df['PASSPORT COUNTRY'][rec]
                email_address = df['EMAIL ADDRESS'][rec]
                classification_member = df['CLASSIFICATION MEMBER'][rec]
                employment_status = df['EMPLOYMENT-STATUS'][rec]
                salary = df['SALARY'][rec]
                pre_existing = df['PRE EXISTING'][rec]
                remarks = df['REMARKS'][rec]
                # endorsement_date = df['ENDORSEMENT DATE'][rec]
                member_since = df['MEMBER SINCE'][rec]
                policy_status = df['POLICY STATUS'][rec]
                member_suspended = df['MEMBER SUSPENDED'][rec]
                renewal_activation_date = df['RENEWAL ACTIVATION DATE'][rec]
                internal_use = df['INTERNAL USE'][rec]
                option_mode = df['OPTION MODE'][rec]

                if renewal_activation_date == 'NaT' or renewal_activation_date == '':
                    renewal_activation_date = False

                suffix = self.env['suffix.id'].search([('name','=',suffix_id)])
                bank = self.env['bank.master'].search([('name','=',bank_name)])
                state_id = self.env['res.country.state'].search([('name','=',state)])
                city_id = self.env['res.state.city'].search([('name','=',city)])
                company = self.env['res.partner'].search([('name','=',company_id),('client','=',True)])
                entity = self.env['client.branch'].search([('name','=',entity_id),('client_id','=',company.id)])
                program_id = self.env['client.program'].search([('name','=',program),('client_branch_id','=',entity.id)])
                plan_id = self.env['client.program.plan'].search([('name','=',plan),('program_id','=',program_id.id)])

                member_values = {
                            'row' : rec+2,
                            'record_mode' : record_mode,
                            'record_type': record_type,
                            'payor_id': payor_id,
                            'member_client_id': company.id,
                            'client_branch_id' : entity.id,
                            'policy_number' : policy_number,
                            'nik': nik,
                            'card_number': card_number,
                            # 'member_number': member_number,
                            'suffix_id': suffix.id,
                            'birth_date': dob,
                            'gender': gender,
                            'join_date': join_date,
                            'start_date': start_date,
                            'effective_date_member': effective_date,
                            'end_date': end_date,
                            'end_policy_date': end_policy_date,
                            'division': division,
                            'division_id': division_code,
                            'swift_code': bank_code,
                            'bank_id': bank.id,
                            'bank_account': account_number,
                            'account_name': account_name,
                            'bank_branch': bank_branch,
                            'marital_status': marital_status,
                            'relationship': relationship,
                            'street': employee_address,
                            # 'street2': address2,
                            'city_id': city_id.id,
                            'state_id': state_id.id,
                            'zip': postcode,
                            'tlp_office': telephone_office,
                            'tlp_residence': telephone_resident,
                            'mobile': telephone_mobile,
                            'email': email_address,
                            'identification_no' : nomor_ktp,
                            'passport_no': passport_number,
                            'passport_country': passport_country,
                            'language' : language,
                            'classification_member': classification_member,
                            'employment_status': employment_status,
                            'salary': salary,
                            'pre_existing': pre_existing,
                            'remarks': remarks,
                            'endorsement_date': date.today(),
                            'member_since': member_since,
                            'policy_status': policy_status,
                            'member_suspend': member_suspended,
                            'renewal_activation_date': renewal_activation_date,
                            'name': member_name,
                            'program_id': program_id.id,
                            'program_plan_id': plan_id.id,
                        }
                vals.append((0, 0, member_values))
        self.preview_file = vals
        if self.preview_file:
            self.preview = True
        return {
            'name': "Preview File",
            'type': 'ir.actions.act_window',
            'res_model': 'import.member',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
            

    def mapping_data(self):
        sheet = self.read_file()
        df = sheet['df_body']
        vals = []

        for rec in df.index:
            # order_line = [(5, 0, 0)]
            member_values = []

            # Get data from name column in excel

            record_mode = df['ENROLLMENT RECORD MODE'][rec]
            
            # Condition for skip process when value in excel empty
            if record_mode not in ('1','2','3','4','5','6','7','8','9','10','11','12','13'):
                raise ValidationError(_("Invalid record mode at row %s") % (rec+2))

            record_type = df['RECORD TYPE'][rec]
            payor_id = df['PAYOR ID'][rec]
            company_id = df['COMPANY ID'][rec]
            entity_id = df['ENTITY ID'][rec]
            policy_number = df['POLICY NUMBER'][rec]
            nik = df['NIK'][rec]
            card_number = df['CARD NUMBER'][rec]
            member_number = df['MEMBER NUMBER'][rec]
            suffix_id = df['SUFFIX ID'][rec]
            member_name = df['MEMBER NAME'][rec]
            dob = df['DOB'][rec]
            gender = df['GENDER'][rec]
            join_date = df['JOIN DATE'][rec]
            start_date = df['START DATE'][rec]
            effective_date = df['EFFECTIVE DATE'][rec]
            end_date = df['END DATE'][rec]
            end_policy_date = df['END POLICY DATE'][rec]
            # ip = df['IP'][rec]
            # op = df['OP'][rec]
            # de = df['DE'][rec]
            # eg = df['EG'][rec]
            # ma = df['MA'][rec]
            # mcu = df['MCU'][rec]
            # ot = df['OT'][rec]
            program = df['PROGRAM'][rec]
            plan = df['PLAN'][rec]
            division = df['DIVISION'][rec]
            division_code = df['DIVISION CODE'][rec]
            bank_code = df['BANK CODE'][rec]
            bank_name = df['BANK NAME'][rec]
            account_number = df['ACCOUNT NUMBER'][rec]
            account_name = df['ACCOUNT NAME'][rec]
            bank_branch = df['BANK BRANCH'][rec]
            rule_bpjs = df['RULE BPJS'][rec]
            bpjs_number = df['BPJS NUMBER'][rec]
            bpjs_classes_room = df['CLASSES ROOM OF BPJS PARTICIPANTS  '][rec]
            name_faskes_fktp = df['NAMES FASKES FKTP  '][rec]
            language = df['LANGUAGE'][rec]
            marital_status = df['MARITAL STATUS'][rec]
            relationship = df['RELATIONSHIP'][rec]
            employee_address = df['EMPLOYEE ADDRESS'][rec]
            address2 = df['ADDRESS2'][rec]
            # record_type = df['ADDRESS3'][rec]
            # record_type = df['ADDRESS4'][rec]
            city = df['CITY'][rec]
            state = df['STATE'][rec]
            postcode = df['POST CODE'][rec]
            telephone_office = df['TELEPHONE – OFFICE'][rec]
            telephone_resident = df['TELEPHONE – RESIDENT'][rec]
            telephone_mobile = df['TELEPHONE - MOBILE'][rec]
            nomor_ktp = df['NOMOR KTP'][rec]
            passport_number = df['PASSPORT NUMBER'][rec]
            passport_country = df['PASSPORT COUNTRY'][rec]
            email_address = df['EMAIL ADDRESS'][rec]
            classification_member = df['CLASSIFICATION MEMBER'][rec]
            employment_status = df['EMPLOYMENT-STATUS'][rec]
            salary = df['SALARY'][rec]
            pre_existing = df['PRE EXISTING'][rec]
            remarks = df['REMARKS'][rec]
            # endorsement_date = df['ENDORSEMENT DATE'][rec]
            member_since = df['MEMBER SINCE'][rec]
            policy_status = df['POLICY STATUS'][rec]
            member_suspended = df['MEMBER SUSPENDED'][rec]
            renewal_activation_date = df['RENEWAL ACTIVATION DATE'][rec]
            internal_use = df['INTERNAL USE'][rec]
            option_mode = df['OPTION MODE'][rec]

            if record_mode not in ('1','13'):
                member_values = self.env['res.partner'].search([('card_number','=',card_number),('member','=',True)])

            suffix = self.env['suffix.id'].search([('name','=',suffix_id)])

            if record_mode == '13':
                member_values = self.env['res.partner'].search([('nik','=',nik),('suffix_id','=',suffix.id),('member','=',True)])
            
            if record_mode == '1':
                # search data many2one
                # suffix = self.env['suffix.id'].search([('name','=',suffix_id)])
                bank = self.env['bank.master'].search([('name','=',bank_name)])
                state_id = self.env['res.country.state'].search([('name','=',state)])
                city_id = self.env['res.state.city'].search([('name','=',city)])
                company = self.env['res.partner'].search([('name','=',company_id),('client','=',True)])
                entity = self.env['client.branch'].search([('name','=',entity_id),('client_id','=',company.id)])
                program_id = self.env['client.program'].search([('name','=',program),('client_branch_id','=',entity.id)])
                plan_id = self.env['client.program.plan'].search([('name','=',plan),('program_id','=',program_id.id)])
                check_existing = self.env['res.partner'].search([('card_number','=',card_number),('member','=',True)])

                if check_existing and record_mode == '1':
                    raise ValidationError(_("Record already exist for Card Number [%s] in Member at row %s") % (card_number,rec+2))
                if not company:
                    raise ValidationError(_("Company not found for [%s] in Client at row %s") % (company_id,rec+2))
                if not entity:
                    raise ValidationError(_("Branch not found for [%s] in %s at row %s") % (entity_id,company_id,rec+2))
                if not program_id:
                    raise ValidationError(_("Program not found for [%s] in %s at row %s") % (program,entity_id,rec+2))
                if not plan_id:
                    raise ValidationError(_("Plan not found for [%s] in program %s at row %s") % (plan,program,rec+2))
                # if not bank:
                #     raise ValidationError(_("Bank not found for [%s] at row %s") % (bank_name,rec+2))
                # if not state_id:
                #     raise ValidationError(_("State not found for [%s] in State at row %s") % (state,rec+2))
                # if not city_id:
                #     raise ValidationError(_("City not found for [%s] in City at row %s") % (city,rec+2))
                if not suffix:
                    raise ValidationError(_("Invalid Suffix for [%s] at row %s") % (suffix,rec+2))

                member_values = self.env['res.partner'].create({
                        'record_mode' : record_mode,
                        'member': True,
                        'record_type': record_type,
                        'payor_id': payor_id,
                        'member_client_id': company.id,
                        'client_branch_id' : entity.id,
                        'policy_number' : policy_number,
                        'nik': nik,
                        'card_number': card_number,
                        # 'member_number': member_number,
                        'suffix_id': suffix.id,
                        'name': member_name,
                        'birth_date': dob,
                        'gender': gender,
                        'join_date': join_date,
                        'start_date': start_date,
                        'effective_date_member': effective_date,
                        'end_date': end_date,
                        'end_policy_date': end_policy_date,
                        'division': division,
                        'division_id': division_code,
                        'swift_code': bank_code,
                        'bank_id': bank.id,
                        'bank_account': account_number,
                        'account_name': account_name,
                        'bank_branch': bank_branch,
                        'marital_status': marital_status,
                        'relationship': relationship,
                        'street': employee_address,
                        # 'street2': address2,
                        'city_id': city_id.id,
                        'state_id': state_id.id,
                        'zip': postcode,
                        'tlp_office': telephone_office,
                        'tlp_residence': telephone_resident,
                        'mobile': telephone_mobile,
                        'identification_no' : nomor_ktp,
                        'passport_no': passport_number,
                        'passport_country': passport_country,
                        'language' : language,
                        'email': email_address,
                        'classification_member': classification_member,
                        'employment_status': employment_status,
                        'salary': salary,
                        'pre_existing': pre_existing,
                        'remarks': remarks,
                        'endorsement_date': date.today(),
                        'member_since': member_since,
                        'policy_status': policy_status,
                        'member_suspend': member_suspended,
                        'renewal_activation_date': renewal_activation_date,
                        'program_id': program_id.id,
                        'program_plan_id': plan_id.id,
                    })

            if record_mode == '2':
                bank = self.env['bank.master'].search([('name','=',bank_name)])
                state_id = self.env['res.country.state'].search([('name','=',state)])
                city_id = self.env['res.state.city'].search([('name','=',city)])
                company = self.env['res.partner'].search([('name','=',company_id),('client','=',True)])
                entity = self.env['client.branch'].search([('name','=',entity_id),('client_id','=',company.id)])
                program_id = self.env['client.program'].search([('name','=',program),('client_branch_id','=',entity.id)])
                plan_id = self.env['client.program.plan'].search([('name','=',plan),('program_id','=',program_id.id)])

                # if not bank:
                #     raise ValidationError(_("Record not found for [%s] in Bank Name") % (bank_name))
                # if not state_id:
                #     raise ValidationError(_("Record not found for [%s] in State") % (state))
                # if not city_id:
                #     raise ValidationError(_("Record not found for [%s] in City") % (city))
                    
                member_values.update({
                        'record_mode' : record_mode,
                        'record_type': record_type,
                        'payor_id': payor_id,
                        'member_client_id': company.id,
                        'client_branch_id' : entity.id,
                        'policy_number' : policy_number,
                        'nik': nik,
                        # 'card_number': card_number,
                        # 'member_number': member_number,
                        'suffix_id': suffix.id,
                        'name': member_name,
                        'birth_date': dob,
                        'gender': gender,
                        'division': division,
                        'division_id': division_code,
                        'swift_code': bank_code,
                        'bank_id': bank.id,
                        'bank_account': account_number,
                        'account_name': account_name,
                        'bank_branch': bank_branch,
                        # 'marital_status': marital_status,
                        # 'relationship': relationship,
                        'street': employee_address,
                        # 'street2': address2,
                        'city_id': city_id.id,
                        'state_id': state_id.id,
                        'zip': postcode,
                        'tlp_office': telephone_office,
                        'tlp_residence': telephone_resident,
                        'mobile': telephone_mobile,
                        'identification_no' : nomor_ktp,
                        'passport_no': passport_number,
                        'passport_country': passport_country,
                        'email': email_address,
                        'classification_member': classification_member,
                        'employment_status': employment_status,
                        'salary': salary,
                        'pre_existing': pre_existing,
                        'remarks': remarks,
                        'endorsement_date': date.today(),
                        'member_since': member_since,
                        'policy_status': policy_status,
                        'member_suspend': member_suspended,
                        'renewal_activation_date': renewal_activation_date,
                        'program_id': program_id.id,
                        'program_plan_id': plan_id.id,
                })
            
            if record_mode == '3':
                member_values.update({
                    'record_mode' : record_mode,
                    'start_date' : start_date,
                    'end_date': end_date,
                })
            
            if record_mode == '4':
                member_values.update({
                    'record_mode' : record_mode,
                    'start_date' : start_date,
                    'end_date': end_date,
                })
            
            if record_mode in ('5','6','10','11','12','13'):
                member_values.update({
                    'record_mode' : record_mode,
                    'renewal_activation_date' : renewal_activation_date,
                    'effective_date_member': effective_date,
                    'end_date': end_date,
                    'end_policy_date': end_policy_date,
                })
            
            if record_mode == '9':
                member_values.update({
                    'record_mode' : record_mode,
                    'employment_status': employment_status,
                    'policy_status': policy_status,
                })
            
            if record_mode == '7':
                member_values.update({
                    'record_mode' : record_mode,
                        'record_type': record_type,
                        'payor_id': payor_id,
                        'member_client_id': company.id,
                        'client_branch_id' : entity.id,
                        'policy_number' : policy_number,
                        'nik': nik,
                        # 'card_number': card_number,
                        # 'member_number': member_number,
                        'suffix_id': suffix.id,
                        'name': member_name,
                        'birth_date': dob,
                        'gender': gender,
                        'join_date': join_date,
                        'start_date': start_date,
                        'effective_date_member': effective_date,
                        'end_date': end_date,
                        'end_policy_date': end_policy_date,
                        'division': division,
                        'division_id': division_code,
                        'swift_code': bank_code,
                        'bank_id': bank.id,
                        'bank_account': account_number,
                        'account_name': account_name,
                        'bank_branch': bank_branch,
                        # 'marital_status': marital_status,
                        'relationship': relationship,
                        # 'street': employee_address,
                        # 'street2': address2,
                        # 'city_id': city_id.id,
                        # 'state_id': state_id.id,
                        # 'zip': postcode,
                        # 'tlp_office': telephone_office,
                        # 'tlp_residence': telephone_resident,
                        # 'mobile': telephone_mobile,
                        # 'identification_no' : nomor_ktp,
                        # 'passport_no': passport_number,
                        # 'passport_country': passport_country,
                        # 'email': email_address,
                        # 'classification_member': classification_member,
                        'employment_status': employment_status,
                        # 'salary': salary,
                        # 'pre_existing': pre_existing,
                        # 'remarks': remarks,
                        # 'endorsement_date': endorsement_date,
                        # 'member_since': member_since,
                        'policy_status': policy_status,
                        # 'member_suspend': member_suspended,
                        'renewal_activation_date': renewal_activation_date,
                })  
            
            if record_mode == '8':
                bank = self.env['bank.master'].search([('name','=',bank_name)])
                state_id = self.env['res.country.state'].search([('name','=',state)])
                city_id = self.env['res.state.city'].search([('name','=',city)])
                # if not bank:
                #     raise ValidationError(_("Record not found for [%s] in Bank Name") % (bank_name))
                # if not state_id:
                #     raise ValidationError(_("Record not found for [%s] in State") % (state))
                # if not city_id:
                #     raise ValidationError(_("Record not found for [%s] in City") % (city))
                    
                member_values.update({
                        'record_mode' : record_mode,
                        'record_type': record_type,
                        'payor_id': payor_id,
                        'member_client_id': company.id,
                        'client_branch_id' : entity.id,
                        'policy_number' : policy_number,
                        'nik': nik,
                        # 'card_number': card_number,
                        # 'member_number': member_number,
                        'suffix_id': suffix.id,
                        'name': member_name,
                        'birth_date': dob,
                        'gender': gender,
                        'join_date': join_date,
                        'start_date': start_date,
                        'effective_date_member': effective_date,
                        'end_date': end_date,
                        'end_policy_date': end_policy_date,
                        'division': division,
                        'division_id': division_code,
                        'swift_code': bank_code,
                        'bank_id': bank.id,
                        'bank_account': account_number,
                        'account_name': account_name,
                        'bank_branch': bank_branch,
                        # 'marital_status': marital_status,
                        # 'relationship': relationship,
                        'street': employee_address,
                        # 'street2': address2,
                        'city_id': city_id.id,
                        'state_id': state_id.id,
                        'zip': postcode,
                        'tlp_office': telephone_office,
                        'tlp_residence': telephone_resident,
                        'mobile': telephone_mobile,
                        'identification_no' : nomor_ktp,
                        'passport_no': passport_number,
                        'passport_country': passport_country,
                        'language' : language,
                        'email': email_address,
                        'classification_member': classification_member,
                        'employment_status': employment_status,
                        'salary': salary,
                        'pre_existing': pre_existing,
                        'remarks': remarks,
                        'endorsement_date': date.today(),
                        'member_since': member_since,
                        'policy_status': policy_status,
                        'member_suspend': member_suspended,
                        'renewal_activation_date': renewal_activation_date,
                        'program_id': program_id.id,
                        'program_plan_id': plan_id.id,
                })
            self.create_history(member_values)
        return vals
    
    def create_history(self,member_values):
        self.env["member.history"].create({
                    'record_mode' : member_values.record_mode,
                    'member_id' : member_values._origin.id,
                    'record_type': member_values.record_type,
                    'payor_id': member_values.payor_id,
                    'member_client_id': member_values.member_client_id.id,
                    'client_branch_id' :member_values. client_branch_id.id,
                    'policy_number' : member_values.policy_number,
                    'nik': member_values.nik,
                    'card_number': member_values.card_number,
                    'member_number': member_values.member_number,
                    'suffix_id': member_values.suffix_id.id,
                    'name' : member_values.name,
                    'birth_date': member_values.birth_date,
                    'gender': member_values.gender,
                    'join_date': member_values.join_date,
                    'start_date': member_values.start_date,
                    'effective_date_member': member_values.effective_date_member,
                    'end_date': member_values.end_date,
                    'end_policy_date': member_values.end_policy_date,
                    'division': member_values.division,
                    'division_id': member_values.division_id,
                    'swift_code': member_values.swift_code,
                    'bank_id': member_values.bank_id.id,
                    'bank_account': member_values.bank_account,
                    'account_name': member_values.account_name,
                    'bank_branch': member_values.bank_branch,
                    'marital_status': member_values.marital_status,
                    'relationship': member_values.relationship,
                    'street': member_values.street,
                    # 'street2': address2,
                    'city_id': member_values.city_id.id,
                    'state_id': member_values.state_id.id,
                    'zip': member_values.zip,
                    'tlp_office': member_values.tlp_office,
                    'tlp_residence': member_values.tlp_residence,
                    'mobile': member_values.mobile,
                    'passport_no': member_values.passport_no,
                    'passport_country': member_values.passport_country,
                    'email': member_values.email,
                    'employment_status': member_values.employment_status,
                    'salary': member_values.salary,
                    'pre_existing': member_values.pre_existing,
                    'remarks': member_values.remarks,
                    'endorsement_date': member_values.endorsement_date,
                    'member_since': member_values.member_since,
                    'policy_status': member_values.policy_status,
                    'member_suspend': member_values.member_suspend,
                    'renewal_activation_date': member_values.renewal_activation_date,
                    'program_id': member_values.program_id.id,
                    'program_plan_id': member_values.program_plan_id.id,
                })
        # member_values.record_mode = 0
        return 

    def confirm_button(self):
        # member = []
        vals = self.mapping_data()
        # for rec in vals:
        #     member = self.env['res.partner'].create(rec['new_member'])
        # return {
        #         'name': "Member",
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'res.partner',
        #         'view_mode': 'tree,kanban,form',
        #         'target': 'self',
        #         'context': {'default_member': True, 'default_is_membership': 1, 'default_customer': 0},
        #         'domain' : [('member', '=', True)],
        #         # 'view_id' : view_id.id,
        #     }


class PreviewFile(models.TransientModel):
    _name = 'preview.file'
    _description = 'Preview File'
    _rec_name = 'name'

    import_id = fields.Many2one('import.member', string='Import')
    row = fields.Integer(string='Row')
    record_mode = fields.Integer(string='Record Mode')
    member_id = fields.Many2one('res.partner', string='Member ID')
    name = fields.Char(string='Name')
    nik = fields.Char(string='Employee ID (NIK)' )
    card_number = fields.Char(string='Card Number' )
    member_number = fields.Char(string='Member Number' )
    suffix_id = fields.Many2one('suffix.id', string='Suffix ID' )
    policy_number = fields.Char(string='Policy Number' )

    join_date = fields.Date(string='Join Date' , )
    start_date = fields.Date(string='Start Date' , )
    end_date = fields.Date(string='End Date' , )
    effective_date_member = fields.Date(string='Effective Date' , )
    end_policy_date = fields.Date(string='End Policy Date' , )

    #Page Work Information
    member_client_id = fields.Many2one('res.partner', string='Company ID', domain=[('client','=',True)] )
    client_branch_id = fields.Many2one('client.branch', string='Client Branch', tracking=True)
    division = fields.Char(string='Division' )
    division_id = fields.Char(string='Division ID' )
    employment_status = fields.Selection([
        ('A', 'Active'),
        ('H', 'Hold'),
        ('T', 'Terminate'),
    ], string='Employment Status' )
    salary = fields.Float(string='Salary' )

    #Page Private Information
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict' )
    state_id = fields.Many2one('res.country.state', "State", domain="[('country_id','=',country_id)]")
    city_id = fields.Many2one('res.state.city', 'Kabupaten', domain="[('state_id','=',state_id)]")
    kecamatan_id = fields.Many2one('res.city.kecamatan', 'Kecamatan', domain=[('city_id', '=', 'city_id')])
    kelurahan_id = fields.Many2one('res.kecamatan.kelurahan', 'Kelurahan', domain="[('kecamatan_id','=',kecamatan_id)]")
    street = fields.Char(string='Street' )
    street2 = fields.Char(string='Street2' )
    zip = fields.Char(change_default=True )
    mobile = fields.Char(string='Mobile')
    email = fields.Char('Email')
    tlp_office = fields.Char(string='Telephone (Office)' )
    tlp_residence = fields.Char(string='Telephone (Resident)' )
    identification_no = fields.Char(string='Identification No')
    passport_no = fields.Integer(string='Passport No' )
    passport_country = fields.Char(string='Passport Country')
    passport_country2 = fields.Many2one('res.country',string='Passport Country' )
    gender = fields.Selection([
        ('M', 'Male'),
        ('F', 'Female'),
    ], string='Gender' )
    birth_date = fields.Date(string='Date of Birth' , default=date.today(),)
    marital_status = fields.Selection([
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
    ], string='Marital Status' )
    relationship = fields.Selection([
        ('E', 'Employee'),
        ('S', 'Supouse'),
        ('C', 'Child'),
    ], string='Relationship' )
    language = fields.Selection([
        ('M', 'Malayan '),
        ('E', 'English'),
        ('C', 'Chinese'),
        ('I', 'Indian'),
        ('O', 'Others'),
    ], string='Language')


    #bank account
    bank_id = fields.Many2one('bank.master', string='Bank')
    bank_account = fields.Char(string='Bank Account' )
    bank_branch = fields.Char(string='Bank Branch' )
    account_name = fields.Char(string='Account Name' )
    swift_code = fields.Char(string='SWIFT code' )


    #Page Member Information
    record_type = fields.Selection([
        ('P', 'Principal'),
        ('D', 'Dependent'),
    ], string='Record Type' )
    payor_id = fields.Char(string='Payor ID')
    rule_bpjs = fields.Selection([
        ('Y', 'Yes'),
        ('N', 'No'),
    ], string='Rule BPJS' )
    bpjs_number = fields.Char(string='BPJS Number' )
    bpjs_classes_room = fields.Selection([
        ('1', 'Kelas Rawat 1'),
        ('2', 'Kelas Rawat 2'),
        ('3', 'Kelas Rawat 3'),
    ], string='BPJS Classes Room' )
    name_faskes_fktp = fields.Char(string='Name Faskes FKTP' )
    classification_member = fields.Selection([
        ('0', 'Reguler'),
        ('1', 'VIP/VVIP'),
    ], string='Classification Member' )
    pre_existing = fields.Char(string='Pre Existing' )
    remarks = fields.Char(string='Remarks' , size=400 )
    endorsement_date = fields.Date(string='Endorsement Date' , default=date.today(),)
    member_since = fields.Date(string='Member Since' , default=date.today(),)
    policy_status = fields.Selection([
        ('A', 'Active'),
        ('N', 'Non Active'),
    ], string='Policy Status' )
    member_suspend = fields.Selection([
        ('Y', 'Yes'),
        ('N', 'No'),
    ], string='Member Suspend' )
    renewal_activation_date = fields.Date(string='Renewal Activation Date' , default=date.today(),)
    internal_use = fields.Char(string='Internal Use' )
    option_mode = fields.Char(string='Option Mode' )

    #Page Benefit Information
    ip = fields.Char(string='IP' )
    op = fields.Char(string='OP' )
    de = fields.Char(string='DE' )
    eg = fields.Char(string='EG' )
    ma = fields.Char(string='MA' )
    mcu = fields.Char(string='MCU' )
    ot = fields.Char(string='OT' )

    #Page Plan Information
    program_id = fields.Many2one('client.program', string='Program')
    program_plan_id = fields.Many2one('client.program.plan', string='Program Plan')
    get_program_id_domain = fields.Many2many('client.program')    
    get_program_plan_id_domain = fields.Many2many('client.program.plan')
    # plan_information_line = fields.One2many('plan.information', 'partner_id', string='Plan Information')
    