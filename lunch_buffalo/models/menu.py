from odoo import fields, models, api


class Menu(models.Model):
    # _name = 'menu'
    _inherit = 'event.event'
    # _description = 'Daily Menu'
    # _inherit = ['event.event']

    # name = fields.Char(required=True)
    food_ids = fields.Many2many(
        'product.product',
        string="Food",
    )
    is_food_item = fields.Boolean(string="Is Food Item")

    # # date = fields.Date(
    # #     string='Date',
    # #     required=True,
    # #     tracking=True)
    # is_published = fields.Boolean()

    @api.model
    def get_current_menu(self):
        """Returns the current menu based on today's date."""
        # today = fields.Datetime.today()
        menu = self.sudo().search([
            ('is_food_item', '=', True),
            # TODO: date related domain
        ], limit=1, order='date_begin desc')
        return menu.food_ids.read(['name','description'])

    @api.model
    def _search_get_detail(self, website, order, options):
        res = super(Menu, self)._search_get_detail(website, order, options)
        res['base_domain'] = res['base_domain'] + [[('is_food_item', '=', True)]]
        return res
    