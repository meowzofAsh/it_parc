Module Odoo 18 - Gestion de Parc Informatique (it_parc)
=====================================================

Module personnalisé Odoo 18 pour la gestion complète du parc informatique
de TECHPARK CI (Abidjan, Côte d'Ivoire).

Fonctionnalités
---------------

- **Gestion des équipements** : workflow à 4 états (Brouillon → Affecté → En maintenance → Retiré)
- **Affectations aux employés** : historique complet des affectations avec wizard de réaffectation
- **Suivi des interventions** : maintenance corrective/préventive, durée calculée, coût
- **Contrats fournisseurs** : suivi des contrats avec jours restants et wizard de renouvellement
- **Alertes automatiques** : garanties et contrats expirant dans ≤ 30 jours (tâche planifiée)
- **Import CSV** : import en masse avec détection des doublons par numéro de série
- **Rapports PDF** (QWeb) : fiche équipement, inventaire complet, historique maintenances
- **Exports Excel** (xlsxwriter) : inventaire, coûts maintenance, contrats expirants (60j)
- **Dashboard OWL** : 4 KPIs + graphique de répartition par catégorie

Installation
------------

1. Copier le dossier `it_parc` dans votre répertoire `addons` d'Odoo 18.

2. Installer la dépendance Python pour les exports Excel :
   ```
   pip install xlsxwriter
   ```

3. Redémarrer le service Odoo :
   ```
   ./odoo-bin -c odoo.conf -u it_parc
   ```
   ou sous Windows :
   ```
   python odoo-bin -c odoo.conf -u it_parc
   ```

4. Dans Odoo, aller aux Applications → Activer le mode développeur → 
   Mettre à jour la liste des modules → Chercher "it_parc" → Installer.

5. Charger les données de démonstration (optionnel mais recommandé) :
   ```
   ./odoo-bin -c odoo.conf -u it_parc --demo=all
   ```

Groupes de sécurité
-------------------

- **IT Technicien** : lecture des équipements, création et suivi de ses propres interventions
- **IT Manager** : accès complet à toutes les fonctionnalités

Structure du module
-------------------

```
it_parc/
├── __init__.py
├── __manifest__.py
├── README.md
├── controllers/
│   ├── __init__.py
│   └── controllers.py
├── data/
│   ├── ir_cron_data.xml      (tâches planifiées pour les alertes)
│   └── it_parc_demo.xml     (données de démonstration)
├── models/
│   ├── __init__.py
│   ├── alert.py
│   ├── assignment.py
│   ├── contract.py
│   ├── equipment.py
│   └── intervention.py
├── report/
│   ├── __init__.py
│   ├── report_equipment_card_template.xml
│   └── report_views.xml
├── security/
│   ├── ir.model.access.csv
│   ├── it_parc_groups.xml
│   └── it_parc_rules.xml
├── static/
│   └── src/
│       ├── css/
│       │   └── dashboard.css
│       └── js/
│           └── dashboard.js
├── views/
│   ├── alert_views.xml
│   ├── assignment_views.xml
│   ├── contract_views.xml
│   ├── dashboard_templates.xml
│   ├── dashboard_views.xml
│   ├── equipment_views.xml
│   ├── intervention_views.xml
│   ├── menus.xml
│   └── templates.xml
├── views/
│   └── ... (vues XML)
└── wizards/
    ├── __init__.py
    ├── excel_export_wizard.py
    ├── excel_export_views.xml
    ├── import_csv_wizard.py
    ├── import_csv_wizard_views.xml
    ├── reassign_wizard.py
    ├── reassign_wizard_views.xml
    ├── renew_contract_wizard.py
    └── renew_contract_wizard_views.xml
```

Données de démonstration
------------------------

Le fichier `data/it_parc_demo.xml` fournit :
- 10 équipements (postes, serveurs, imprimantes, réseau, téléphones)
- 3 contrats fournisseurs (2 actifs, 1 expiré)
- 5 interventions (3 terminées, 1 planifiée, 1 en cours)

Auteur
------
moi même je suis Operi Carla-Maria