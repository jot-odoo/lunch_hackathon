from odoo import _, api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _attendance_action_change(self, geo_information=None):
        attendance = super()._attendance_action_change(geo_information=geo_information)
        if attendance.check_in and not attendance.check_out: # and self.env.context.get('for_lunch'):
            attendance.check_out = attendance.check_in
        return attendance
