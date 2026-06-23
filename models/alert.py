from odoo import models, fields, api, _


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

    @api.model
    def cron_generate_alerts(self):
        Alert = self.env['it.alert']
        Equipment = self.env['it.equipment']
        Contract = self.env['it.contract']

        today = fields.Date.today()

        equipments = Equipment.search([('warranty_date', '!=', False), ('state', '!=', 'retired')])
        for eq in equipments:
            delta = (eq.warranty_date - today).days
            if 0 <= delta <= 30:
                existing = Alert.search([
                    ('type', '=', 'warranty'),
                    ('expiration_date', '=', eq.warranty_date),
                    ('reference', '=', 'it.equipment,%d' % eq.id),
                ])
                if not existing:
                    Alert.create({
                        'name': _('Garantie expirant bientôt : %s') % eq.name,
                        'type': 'warranty',
                        'reference': 'it.equipment,%d' % eq.id,
                        'expiration_date': eq.warranty_date,
                    })

        contracts = Contract.search([('state', '=', 'active'), ('end_date', '!=', False)])
        for ct in contracts:
            delta = (ct.end_date - today).days
            if 0 <= delta <= 30:
                existing = Alert.search([
                    ('type', '=', 'contract'),
                    ('expiration_date', '=', ct.end_date),
                    ('reference', '=', 'it.contract,%d' % ct.id),
                ])
                if not existing:
                    Alert.create({
                        'name': _('Contrat expirant bientôt : %s') % ct.name,
                        'type': 'contract',
                        'reference': 'it.contract,%d' % ct.id,
                        'expiration_date': ct.end_date,
                    })

    def action_mark_read(self):
        self.read = True
