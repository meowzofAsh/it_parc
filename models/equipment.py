from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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

    @api.constrains('serial_number')
    def _check_serial_unique(self):
        for rec in self:
            existing = self.search([('serial_number', '=', rec.serial_number), ('id', '!=', rec.id)])
            if existing:
                raise ValidationError(_("Ce numéro de série existe déjà : %s") % rec.serial_number)

    @api.constrains('purchase_value')
    def _check_purchase_value(self):
        for rec in self:
            if rec.purchase_value and rec.purchase_value < 0:
                raise ValidationError(_("La valeur d'achat ne peut pas être négative."))

    def action_assign(self):
        self.state = 'assigned'

    def action_maintenance(self):
        self.state = 'maintenance'

    def action_retire(self):
        self.state = 'retired'
        self.employee_id = False
        self.department_id = False

    def action_draft(self):
        self.state = 'draft'

    def action_reassign(self):
        self.ensure_one()
        return {
            'name': _('Réaffectation'),
            'type': 'ir.actions.act_window',
            'res_model': 'reassign.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_equipment_id': self.id},
        }

    def write(self, vals):
        if 'employee_id' in vals and vals.get('employee_id'):
            vals['state'] = 'assigned'
            for rec in self:
                if rec.employee_id and rec.employee_id.id != vals['employee_id']:
                    old_assignments = rec.assignment_ids.filtered(lambda a: not a.end_date)
                    old_assignments.write({'end_date': fields.Date.today()})
        return super().write(vals)

    @api.model
    def get_dashboard_data(self):
        total = self.search_count([])
        total_value = sum(self.search_read([], ['purchase_value']) or [], 0)

        Intervention = self.env['it.intervention']
        month_costs = Intervention.search_read([
            ('start_date', '>=', fields.Date.today().replace(day=1)),
            ('state', '=', 'done'),
        ], ['cost'])
        maintenance_cost = sum(m.get('cost', 0) for m in month_costs)

        top_panne = self.search_read([
            ('state', '=', 'maintenance'),
        ], ['name'])
        top_panne_count = len(top_panne)

        return {
            'total_equipments': total,
            'total_value': total_value,
            'maintenance_cost': maintenance_cost,
            'top_panne_count': top_panne_count,
        }
