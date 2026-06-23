from odoo import models, fields, api


class ExcelExportWizard(models.TransientModel):
    _name = 'excel.export.wizard'
    _description = 'Wizard d\'export Excel'

    export_type = fields.Selection([
        ('inventory', 'Inventaire complet'),
        ('maintenance_cost', 'Coûts de maintenance'),
        ('expiring_contracts', 'Contrats expirants'),
    ], string="Type d'export", required=True, default='inventory')

    def action_export(self):
        return {'type': 'ir.actions.act_window_close'}
