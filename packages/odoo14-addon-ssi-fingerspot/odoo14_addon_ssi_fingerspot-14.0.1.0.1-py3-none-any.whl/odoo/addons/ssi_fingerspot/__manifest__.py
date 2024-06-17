# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Fingerspot Attendance Machine Integration with Odoo",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "external_dependencies": {"python": ["pandas"]},
    "depends": [
        "ssi_master_data_mixin",
        "ssi_timesheet_attendance",
        "queue_job_batch",
        "base_automation",
    ],
    "data": [
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "data/ir_cron_import_attendance.xml",
        "data/hr_attendance_reason.xml",
        "menu.xml",
        "views/fingerspot_data_machine_views.xml",
        "views/fingerspot_attendance_machine_views.xml",
        "views/fingerspot_backend_views.xml",
        "views/res_company_views.xml",
        "views/hr_timesheet_attendance_views.xml",
        "wizard/fingerspot_attendance_machine_import_wizard_views.xml",
    ],
}
