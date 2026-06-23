from odoo import models, fields, api


class ItAlert(models.Model):
    _name = 'it.alert'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Alerte'
    _order = 'expiration_date asc'

    name = fields.Char(string="Titre", required=True, tracking=True)
    type = fields.Selection([
        ('warranty', 'Garantie'),
        ('contract', 'Contrat'),
    ], string="Type", required=True, tracking=True)
    reference = fields.Reference([
        ('it.equipment', 'Équipement'),
        ('it.contract', 'Contrat'),
    ], string="Référence", tracking=True)
    expiration_date = fields.Date(string="Date d'expiration", required=True, tracking=True)
    read = fields.Boolean(string="Lue", default=False, tracking=True)
    alert_days = fields.Integer(string="Alerte (jours avant)", default=30)
