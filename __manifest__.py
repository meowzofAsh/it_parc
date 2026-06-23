{
    'name': "Gestion de Parc Informatique - it_parc",
    'summary': "Module de gestion de parc informatique pour TECHPARK CI",
    'description': """
Gestion complète du parc informatique :
- Équipements (workflow brouillon → affecté → maintenance → retiré)
- Affectations aux employés avec historique
- Interventions de maintenance
- Contrats fournisseurs
- Alertes automatiques (garanties, contrats)
- Import CSV
- Rapports PDF et exports Excel
- Dashboard OWL
    """,
    'author': "TECHPARK CI",
    'website': "",
    'category': 'Industries',
    'version': '1.0',
    'depends': ['base', 'mail', 'web', 'hr'],
    'data': [
        'security/it_parc_groups.xml',
        'security/ir.model.access.csv',
        'security/it_parc_rules.xml',
        'views/equipment_views.xml',
        'views/assignment_views.xml',
        'views/intervention_views.xml',
        'views/contract_views.xml',
        'views/alert_views.xml',
        'views/menus.xml',
        'views/dashboard_views.xml',
        'views/dashboard_templates.xml',
        'wizards/reassign_wizard_views.xml',
        'wizards/import_csv_wizard_views.xml',
        'wizards/renew_contract_wizard_views.xml',
        'wizards/excel_export_views.xml',
        'data/ir_cron_data.xml',
        'report/report_views.xml',
        'report/report_equipment_card_template.xml',
    ],
    'demo': [
        'data/it_parc_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            ('include', 'web.chartjs'),
            'it_parc/static/src/js/dashboard.js',
            'it_parc/static/src/css/dashboard.css',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
