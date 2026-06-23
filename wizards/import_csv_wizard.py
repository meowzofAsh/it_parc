from odoo import models, fields, api


class ImportCsvWizard(models.TransientModel):
    _name = 'import.csv.wizard'
    _description = 'Wizard d\'import CSV'

    file = fields.Binary(string="Fichier CSV", required=True)
    filename = fields.Char(string="Nom du fichier")

    def action_import(self):
        return {'type': 'ir.actions.act_window_close'}
