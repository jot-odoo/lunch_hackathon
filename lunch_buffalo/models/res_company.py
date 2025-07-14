from odoo import _, api, fields, models

from werkzeug.urls import url_join


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.depends("attendance_kiosk_key")
    def _compute_attendance_kiosk_url(self):
        for company in self:
            company.attendance_kiosk_url = url_join(self.env['res.company'].get_base_url(), '/hr_attendance/%s' % company.attendance_kiosk_key)
            if self.env.context.get('for_lunch'):
                company.attendance_kiosk_url += '?for_lunch=true'
