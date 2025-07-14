from odoo import fields, http, _
from odoo.osv import expression
from odoo.http import Controller, request
from odoo.service.common import exp_version
from odoo.tools import float_round, py_to_js_locale, SQL


from odoo.addons.hr_attendance.controllers.main import HrAttendance
from odoo.addons.website_event.controllers.main import WebsiteEventController

class LunchAttendance(HrAttendance):

    @http.route(['/lunch_buffalo/get_current_menu'], type='json', auth="public")
    def get_current_menu(self):
        """Endpoint to get the current menu."""
        menu = request.env['menu'].sudo().get_current_menu()
        return [
            {'id': 1, 'name': "Ravioli", 'description': "Delicious ravioli with cheese filling."},
            {'id': 2, 'name': 'Coconut Soup', 'description': "Delicious coconut soup with a hint of lime."},
        ]

    # @http.route(["/hr_attendance/<token>"], type='http', auth='public', website=True, sitemap=True)
    # def open_kiosk_mode(self, token, from_trial_mode=False, for_lunch=False):
    #     if not for_lunch:
    #         return super().open_kiosk_mode(token, from_trial_mode)
    #     company = self._get_company(token)
    #     if not company:
    #         return request.not_found()
    #     else:
    #         department_list = [
    #             {"id": dep["id"], "name": dep["name"], "count": dep["total_employee"]}
    #             for dep in request.env["hr.department"]
    #             .with_context(allowed_company_ids=[company.id])
    #             .sudo()
    #             .search_read(
    #                 domain=[("company_id", "=", company.id)],
    #                 fields=["id", "name", "total_employee"],
    #             )
    #         ]
    #         has_password = self.has_password()
    #         if not from_trial_mode and has_password:
    #             request.session.logout(keep_db=True)
    #         kiosk_mode = company.attendance_kiosk_mode
    #         version_info = exp_version()
    #         return request.render(
    #             'hr_attendance.public_kiosk_mode',
    #              {
    #                 'kiosk_backend_info': {
    #                     'token': token,
    #                     'company_id': company.id,
    #                     'company_name': company.name,
    #                     'departments': department_list,
    #                     'kiosk_mode': kiosk_mode,
    #                     'from_trial_mode': from_trial_mode,
    #                     'for_lunch': for_lunch,
    #                     'barcode_source': company.attendance_barcode_source,
    #                     'lang': py_to_js_locale(company.partner_id.lang or company.env.lang),
    #                     'server_version_info': version_info.get('server_version_info'),
    #                 },
    #             }
    #         )


class LunchController(Controller):

    @http.route(['/lunch'], type='http', auth="public", website=True, sitemap=True)
    def lunch(self, **kw):
        filter = kw.get('filter', 'today')
        today = fields.Date.today()
        domain = [('date', '=', today)]
        if filter == 'upcoming':
            domain = [('date', '>', today)]
        elif filter == 'past':
            domain = [('date', '<', today)]
        domain = expression.AND([domain, [('is_published', '=', True)]])
        menus = request.env['menu'].search(domain)
        values = {
            'menus': menus,
            'filter': filter,
        }
        return request.render("lunch_buffalo.index", values)
