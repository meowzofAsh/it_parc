import csv
import base64
from io import StringIO

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ImportCsvWizard(models.TransientModel):
    _name = 'import.csv.wizard'
    _description = "Wizard d'import CSV"

    file = fields.Binary(string="Fichier CSV", required=True)
    filename = fields.Char(string="Nom du fichier")

    def action_import(self):
        if not self.file:
            raise UserError(_("Veuillez sélectionner un fichier CSV."))

        decoded = base64.b64decode(self.file).decode('utf-8-sig')
        reader = csv.DictReader(StringIO(decoded))

        required_fields = {'name', 'serial_number', 'category'}
        if not required_fields.issubset(reader.fieldnames or []):
            raise UserError(_(
                "Le CSV doit contenir les colonnes : name, serial_number, category"
            ))

        Equipment = self.env['it.equipment']
        created = 0
        skipped = 0
        errors = []

        for line_num, row in enumerate(reader, start=2):
            try:
                serial = row.get('serial_number', '').strip()
                if not serial:
                    errors.append(f"Ligne {line_num}: numéro de série manquant")
                    continue

                existing = Equipment.search([('serial_number', '=', serial)])
                if existing:
                    skipped += 1
                    continue

                vals = {
                    'name': row.get('name', '').strip(),
                    'serial_number': serial,
                    'category': row.get('category', 'other').strip(),
                    'purchase_value': float(row.get('purchase_value', 0) or 0),
                }
                if row.get('purchase_date'):
                    vals['purchase_date'] = row['purchase_date'].strip()
                if row.get('warranty_date'):
                    vals['warranty_date'] = row['warranty_date'].strip()

                Equipment.create(vals)
                created += 1
            except Exception as e:
                errors.append(f"Ligne {line_num}: {e}")

        msg = _("Import terminé.\nCréés: %d\nIgnorés (doublons): %d\nErreurs: %d") % (
            created, skipped, len(errors))
        if errors:
            msg += "\n\nDétail:\n" + "\n".join(errors[-5:])

        return {
            'type': 'ir.actions.notify',
            'message': msg,
            'title': _('Import terminé'),
            'sticky': False,
        }
