import base64
from io import BytesIO

from datetime import timedelta

from odoo import models, fields, api, _


class ExcelExportWizard(models.TransientModel):
    _name = 'excel.export.wizard'
    _description = "Wizard d'export Excel"

    export_type = fields.Selection([
        ('inventory', 'Inventaire complet'),
        ('maintenance_cost', 'Coûts de maintenance'),
        ('expiring_contracts', 'Contrats expirants (60 jours)'),
    ], string="Type d'export", required=True, default='inventory')

    def action_export(self):
        if self.export_type == 'inventory':
            return self._export_inventory()
        elif self.export_type == 'maintenance_cost':
            return self._export_maintenance_cost()
        else:
            return self._export_expiring_contracts()

    def _export_inventory(self):
        equipment = self.env['it.equipment'].search([])
        headers = ['Nom', 'N° série', 'Catégorie', 'État', 'Valeur', "Date d'achat", 'Garantie']
        rows = []
        for eq in equipment:
            rows.append([
                eq.name, eq.serial_number,
                dict(eq._fields['category'].selection).get(eq.category, eq.category),
                dict(eq._fields['state'].selection).get(eq.state, eq.state),
                eq.purchase_value, str(eq.purchase_date or ''), str(eq.warranty_date or ''),
            ])
        return self._make_xlsx('Inventaire complet', headers, rows)

    def _export_maintenance_cost(self):
        interventions = self.env['it.intervention'].search([('state', '=', 'done')])
        headers = ['Équipement', 'Type', 'Technicien', 'Date', 'Coût']
        rows = []
        for inv in interventions:
            rows.append([
                inv.equipment_id.name,
                dict(inv._fields['type'].selection).get(inv.type, inv.type),
                inv.technician_id.name,
                str(inv.start_date or ''),
                inv.cost,
            ])
        rows.append(['', '', '', 'TOTAL', sum(r[4] for r in rows)])
        return self._make_xlsx('Coûts maintenance', headers, rows)

    def _export_expiring_contracts(self):
        today = fields.Date.today()
        contracts = self.env['it.contract'].search([
            ('state', '=', 'active'),
            ('end_date', '>=', today),
            ('end_date', '<=', today + timedelta(days=60)),
        ])
        headers = ['Nom', 'Fournisseur', 'Date fin', 'Jours restants', 'Montant']
        rows = []
        for ct in contracts:
            rows.append([
                ct.name, ct.partner_id.name, str(ct.end_date or ''),
                ct.days_remaining, ct.amount,
            ])
        return self._make_xlsx('Contrats expirants', headers, rows)

    def _make_xlsx(self, title, headers, rows):
        try:
            import xlsxwriter
        except ImportError:
            from odoo.exceptions import UserError
            raise UserError(
                _("La bibliothèque xlsxwriter est requise. Installez-la avec: pip install xlsxwriter")
            )

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet(title[:31])

        header_fmt = workbook.add_format({'bold': True, 'bg_color': '#7c7bad', 'font_color': 'white'})
        row_fmt = workbook.add_format()
        red_fmt = workbook.add_format({'bg_color': '#ffcccc'})

        for col, h in enumerate(headers):
            sheet.write(0, col, h, header_fmt)

        for r_idx, row in enumerate(rows, start=1):
            for c_idx, val in enumerate(row):
                fmt = row_fmt
                if title == 'Contrats expirants' and c_idx == 3:
                    try:
                        if int(val) <= 10:
                            fmt = red_fmt
                    except (ValueError, TypeError):
                        pass
                sheet.write(r_idx, c_idx, val, fmt)

        sheet.autofilter(0, 0, len(rows), len(headers) - 1)
        for c_idx in range(len(headers)):
            sheet.set_column(c_idx, c_idx, 20)

        workbook.close()
        output.seek(0)
        file_data = base64.b64encode(output.read()).decode()

        attachment = self.env['ir.attachment'].create({
            'name': '%s.xlsx' % title,
            'datas': file_data,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }
