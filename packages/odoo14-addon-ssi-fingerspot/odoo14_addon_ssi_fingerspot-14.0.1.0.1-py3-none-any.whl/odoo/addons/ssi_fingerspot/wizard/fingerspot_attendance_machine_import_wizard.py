# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
import logging
from datetime import datetime, timedelta

import pytz
import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

_logger = logging.getLogger(__name__)

try:
    import pandas as pd
except (ImportError, IOError) as err:
    _logger.debug(err)


class FingerspotMachineTransactionWizard(models.TransientModel):
    _name = "fingerspot.attendance.machine.import.wizard"
    _description = "Import Attendance From Machine"

    @api.model
    def _get_fingerspot_backend_id(self):
        company = self.env.company
        backend = company.fingerspot_backend_id
        return backend and backend.id or False

    fingerspot_backend_id = fields.Many2one(
        string="Backend",
        comodel_name="fingerspot_backend",
        default=lambda self: self._get_fingerspot_backend_id(),
        required=True,
    )

    @api.model
    def _get_is_admin(self):
        result = False
        if self.env.user.has_group("base.group_system"):
            result = True
        return result

    is_admin = fields.Boolean(
        string="Is Admin?",
        default=lambda self: self._get_is_admin(),
    )

    machine_id = fields.Many2one(
        string="# Machine",
        comodel_name="fingerspot.data.machine",
        required=True,
    )

    date_start = fields.Date(
        string="Date Start",
        required=True,
        default=fields.Date.context_today,
    )

    date_end = fields.Date(
        string="Date End",
        required=True,
        default=fields.Date.context_today,
    )

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                strWarning = _("Date end must be greater than date start")
                if record.date_end < record.date_start:
                    raise UserError(strWarning)

    def _convert_datetime_utc(self, dt):
        if dt:
            user = self.env.user
            convert_dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            if user.tz:
                tz = pytz.timezone(user.tz)
            else:
                tz = pytz.utc
            convert_utc = tz.localize(convert_dt).astimezone(pytz.utc)
            format_utc = convert_utc.strftime("%Y-%m-%d %H:%M:%S")
            return format_utc
        else:
            return "-"

    def _import_attendance(self, date):
        self.ensure_one()
        str_group = "Import attendance Batch %s for %s" % (self.machine_id.name, date)
        batch = self.env["queue.job.batch"].get_new_batch(str_group)
        description = "Import attendance for %s" % (date)
        self.with_context(job_batch=batch).with_delay(
            description=_(description)
        )._get_attlog(date)
        batch.enqueue()

    def _get_attlog(self, date):
        self.ensure_one()
        backend = self.fingerspot_backend_id
        url = backend.base_url + backend.api_attlog
        api_token = backend.api_token
        headers = {
            "Authorization": "Bearer %s" % api_token,
        }
        payload = json.dumps(
            {
                "trans_id": "1",
                "cloud_id": self.machine_id.device_id,
                "start_date": date,
                "end_date": date,
            }
        )

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            result = response.json()
            self._get_result(result)
        except Exception as e:
            raise UserError(str(e))

    def _prepare_att_machine_data(self, data):
        self.ensure_one()
        return {
            "machine_id": self.machine_id.id,
            "scan_date": self._convert_datetime_utc(data["scan_date"]),
            "pin": data["pin"],
            "verify": str(data["verify"]),
            "status_scan": str(data["status_scan"]),
        }

    def _get_result(self, result):
        self.ensure_one()
        obj_att_machine = self.env["fingerspot.attendance.machine"]
        if result["success"]:
            result_data = result["data"]
            if result_data:
                for data in result_data:
                    criteria = [
                        ("pin", "=", data["pin"]),
                        (
                            "scan_date",
                            "=",
                            self._convert_datetime_utc(data["scan_date"]),
                        ),
                    ]
                    att_machine_ids = obj_att_machine.search(criteria)
                    if len(att_machine_ids) == 0:
                        att_machine = obj_att_machine.create(
                            self._prepare_att_machine_data(data)
                        )
                        att_machine.onchange_employee_id()

    def action_import(self):
        date_start = self.date_start
        date_list = pd.date_range(date_start, self.date_end, freq="D")
        for index in date_list.strftime("%Y-%m-%d"):
            self._import_attendance(index)

    def _cron_import_attendance(self):
        obj_data_machine = self.env["fingerspot.data.machine"]
        company = self.env.company
        fingerspot_backend_id = company.fingerspot_backend_id.id
        utc_date_now = datetime.now()
        tz = pytz.timezone(self.env.user.tz or "Asia/Jakarta")
        user_date_now = utc_date_now.astimezone(tz).date()
        date_start = user_date_now - timedelta(days=2)

        machine_ids = obj_data_machine.search([])
        if machine_ids:
            for machine in machine_ids:
                wizard = self.create(
                    {
                        "fingerspot_backend_id": fingerspot_backend_id,
                        "machine_id": machine.id,
                        "date_start": date_start,
                        "date_end": user_date_now,
                    }
                )
                wizard.action_import()
