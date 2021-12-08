import re
from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError

class ReportAsbMasterProviderActivityProviderActivityXlsx(models.AbstractModel):
    _name = 'report.asb_master_provider_activity.provider_activity_xlsx'
    _description = 'Report Asb Master Provider Activity Provider Activity Xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, export_data):
        activity = self.env['provider.provider'].sudo().search([('created_date', '>=', export_data.from_date), ('created_date', '<=', export_data.to_date)])
        if not activity:
            raise ValidationError('From %s to %s not activity found!' % (export_data.from_date.strftime('%d/%m/%Y'), export_data.to_date.strftime('%d/%m/%Y')))

        created_by = []
        user = self.env['provider.provider'].sudo().search([('created_date','>=',export_data.from_date),('created_date','<=',export_data.to_date)])
        for rec in user:
            if rec.created_by not in created_by:
                created_by.append(rec.created_by)
        activity = self.env['provider.activity'].sudo().search([])

        sheet = workbook.add_worksheet('Provider Activty')
        
        # header center
        format1 = workbook.add_format({'font_size': 14, 'align': 'center', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'bg_color': '#04be14'})
        # isi
        format2 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': False, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, })
        format2a = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': False, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, })
        
        # judul
        format3 = workbook.add_format({'font_size': 20, 'align': 'left', 'bold': True})

        sheet.set_column('B:B', 5)
        sheet.set_column('C:C', 40)
        sheet.set_column('D:Q', 25)
        sheet.set_row(0, 30)
        sheet.set_margins(0.5, 0.5, 0.5, 0.5)
        sheet.merge_range('A1:Q1', ('Provider Activity  (%s to %s)' % (export_data.from_date, export_data.to_date)), format3)

        row = 3
        column = 3
        total_x = 0
        no = 1

        sheet.write(2, 1, 'No', format1)
        sheet.write(2, 2, 'Row Labels', format1)
        
        for act in activity:
            sheet.write(row, 1, no, format2a)
            sheet.write(row, 2, act.name, format2)
            for obj in created_by:
                sheet.write(2, column, obj.name, format1)
                count = self.env['provider.provider'].sudo().search_count([('created_by', '=', obj.id), ('activity_id', '=', act.id),
                                                                           ('created_date', '>=', export_data.from_date), ('created_date', '<=', export_data.to_date)])
                sheet.write(row, column, count, format2a)
                total_x = total_x + count
                column += 1
            sheet.write(row, column, total_x, format2a)
            total_x = 0
            column = 3
            row += 1
            no += 1
        
        for rec in created_by:
            total_y = self.env['provider.provider'].sudo().search_count([('created_by', '=', rec.id), ('created_date', '>=', export_data.from_date), ('created_date', '<=', export_data.to_date)])
            sheet.write(row, column, total_y, format1)
            column += 1
        
        total_xy = self.env['provider.provider'].sudo().search_count([('created_date', '>=', export_data.from_date), ('created_date', '<=', export_data.to_date)])
        row_akhir = row + 1
        
        awal = 'B%s' % row_akhir
        akhir = 'C%s' % row_akhir
        
        sheet.merge_range(('%s:%s'%(awal,akhir)), 'Grand Total', format1)
        sheet.write(2, column, 'Grand Total', format1)
        sheet.write(row, column, total_xy, format1)


        

