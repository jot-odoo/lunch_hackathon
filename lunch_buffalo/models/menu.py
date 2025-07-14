from odoo import fields, models, api


class Menu(models.Model):
    _name = 'menu'
    _description = 'Daily Menu'

    name = fields.Char(required=True)
    food_ids = fields.Many2many(
        'product.product',
        string="Food",
    )
   
    date = fields.Datetime(
        string='Date',
        required=True,
        tracking=True)
    is_published = fields.Boolean()

    @api.model
    def create(self, vals):
        if not vals.get('name') and vals.get('date_start') and vals.get('date_end'):
            vals['name'] = f"Menu Week {vals['date_start']} to {vals['date_end']}"
        return super().create(vals)

    @api.model
    def get_current_menu(self):
        """Returns the current menu based on today's date."""
        today = fields.Date.today()
        menu = self.search([
            ('date', '=', today),
        ])
        return menu.read(['name'])