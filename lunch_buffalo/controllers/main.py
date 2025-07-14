from odoo import fields, http, _
from odoo.osv import expression
from odoo.http import Controller, request
from odoo.service.common import exp_version
from odoo.tools import float_round, py_to_js_locale, SQL
from odoo.addons.website.controllers.main import QueryURL


from odoo.addons.hr_attendance.controllers.main import HrAttendance
from odoo.addons.website_event.controllers.main import WebsiteEventController

class LunchAttendance(HrAttendance):

    @http.route(['/lunch_buffalo/get_current_menu'], type='json', auth="public")
    def get_current_menu(self):
        """Endpoint to get the current menu."""
        menu = request.env['event.event'].sudo().get_current_menu()

        # return [
        #     {'id': 1, 'description': "Korean BBQ beef", 'name': "Bulgogi"},
        #     {'id': 2, 'description': "Spicy fermented cabbage", 'name': "Kimchi"}
        # ]

        return menu

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


class LunchController(WebsiteEventController):

    def _get_events_search_options(self, **post):
        return {
            'displayDescription': False,
            'displayDetail': False,
            'displayExtraDetail': False,
            'displayExtraLink': False,
            'displayImage': False,
            'allowFuzzy': not post.get('noFuzzy'),
            'date': post.get('date'),
            'tags': post.get('tags'),
        }

    @http.route(['/lunch'], type='http', auth="public", website=True, sitemap=True)
    def lunch(self, page=1, **searches):
        if searches.get('tags',
                        '[]').count(',') > 0 and request.httprequest.method == 'GET' and not searches.get('prevent_redirect'):
            # Previously, the tags were searched using GET, which caused issues with crawlers (too many hits)
            # We replaced those with POST to avoid that, but it's not sufficient as bots "remember" crawled pages for a while
            # This permanent redirect is placed to instruct the bots that this page is no longer valid
            # Note: We allow a single tag to be GET, to keep crawlers & indexes on those pages
            # What we really want to avoid is combinatorial explosions
            # (Tags are formed as a JSON array, so we count ',' to keep it simple)
            # TODO: remove in a few stable versions (v19?), including the "prevent_redirect" param in templates
            return request.redirect('/event', code=301)

        Event = request.env['event.event']
        SudoEventType = request.env['event.type'].sudo()
        searches.setdefault('search', '')
        searches.setdefault('date', 'upcoming')
        searches.setdefault('tags', '')
        website = request.website

        step = 12  # Number of events per page

        options = self._get_events_search_options(**searches)
        order = 'date_begin'
        if searches.get('date', 'upcoming') == 'old':
            order = 'date_begin desc'
        order = 'is_published desc, ' + order + ', id desc'
        search = searches.get('search')
        event_count, details, fuzzy_search_term = website._search_with_fuzzy("events",
                                                                             search,
                                                                             limit=page * step,
                                                                             order=order,
                                                                             options=options)
        event_details = details[0]
        events = event_details.get('results', Event)
        events = events[(page - 1) * step:page * step]

        # count by domains without self search
        domain_search = [('name', 'ilike', fuzzy_search_term or searches['search'])] if searches['search'] else []

        no_date_domain = event_details['no_date_domain']
        dates = event_details['dates']
        for date in dates:
            if date[0] not in ['all', 'old']:
                date[3] = Event.search_count(expression.AND(no_date_domain) + domain_search + date[2])

        no_country_domain = event_details['no_country_domain']
        countries = Event.read_group(expression.AND(no_country_domain) + domain_search, ["id", "country_id"],
                                     groupby="country_id",
                                     orderby="country_id")
        countries.insert(0, {
            'country_id_count': sum([int(country['country_id_count']) for country in countries]),
            'country_id': ("all", _("All Countries"))
        })

        # search_tags = event_details['search_tags']
        current_date = event_details['current_date']
        current_type = None
        current_country = None

        pager = website.pager(url="/event", url_args=searches, total=event_count, page=page, step=step, scope=5)

        keep = QueryURL(
            '/event', **{
                key: value
                for key, value in searches.items()
                if (key == 'search' or (value != 'upcoming' if key == 'date' else value != 'all'))
            })

        searches['search'] = fuzzy_search_term or search

        values = {
            'current_date':
                current_date,
            'current_country':
                current_country,
            'current_type':
                current_type,
            'event_ids':
                events.filtered(lambda e: e.is_food_item),  # event_ids used in website_event_track so we keep name as it is
            'dates':
                dates,
            'categories':
                request.env['event.tag.category'].search([('is_published', '=', True), '|', ('website_id', '=', website.id),
                                                          ('website_id', '=', False)]),
            'countries':
                countries,
            'pager':
                pager,
            'searches':
                searches,
            'keep':
                keep,
            'search_count':
                event_count,
            'original_search':
                fuzzy_search_term and search,
            'website':
                website,
            'search_tags':
                request.env['event.tag'],
        }

        return request.render("lunch_buffalo.index", values)

        # filter = kw.get('filter', 'today')
        # today = fields.Date.today()
        # domain = [('date', '=', today)]
        # if filter == 'upcoming':
        #     domain = [('date', '>', today)]
        # elif filter == 'past':
        #     domain = [('date', '<', today)]
        # domain = expression.AND([domain, [('is_published', '=', True)]])

        # menus = request.env['menu'].search(domain)
        # values = {
        #     'menus': menus,
        #     'filter': filter,
        # }
        # return request.render("lunch_buffalo.index", values)
