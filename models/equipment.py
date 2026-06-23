from odoo import models, fields, api


class ItEquipment(models.Model):
    _name = 'it.equipment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Équipement informatique'
    _rec_name = 'name'
    _order = 'create_date desc'

    name = fields.Char(string="Nom", required=True, tracking=True)
    serial_number = fields.Char(string="Numéro de série", required=True, tracking=True)
    category = fields.Selection([
        ('workstation', 'Poste de travail'),
        ('server', 'Serveur'),
        ('printer', 'Imprimante'),
        ('network', 'Équipement réseau'),
        ('phone', 'Téléphone IP'),
        ('other', 'Autre'),
    ], string="Catégorie", required=True, default='workstation', tracking=True)
    purchase_value = fields.Float(string="Valeur d'achat", tracking=True)
    purchase_date = fields.Date(string="Date d'achat", tracking=True)
    warranty_date = fields.Date(string="Date de fin de garantie", tracking=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('assigned', 'Affecté'),
        ('maintenance', 'En maintenance'),
        ('retired', 'Retiré'),
    ], string="État", default='draft', required=True, tracking=True)
    employee_id = fields.Many2one('hr.employee', string="Employé actuel", tracking=True)
    department_id = fields.Many2one('hr.department', string="Département actuel", tracking=True)
    contract_id = fields.Many2one('it.contract', string="Contrat fournisseur")
    assignment_ids = fields.One2many('it.assignment', 'equipment_id', string="Historique des affectations")
    intervention_ids = fields.One2many('it.intervention', 'equipment_id', string="Interventions")
    note = fields.Text(string="Notes")
    active = fields.Boolean(string="Actif", default=True)
