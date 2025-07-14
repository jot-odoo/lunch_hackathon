from odoo import models, fields

class Food(models.Model):
    _inherit = 'product.product'
    _description = 'Food'
    
    allergen_ids = fields.Many2many('food.allergen', string="Allergens")
    alternative_ids = fields.Many2many(
        'product.product',
        'product_food_alternative_rel',
        'product_id',
        'alternative_id',
        string="Alternative Foods"
    )
    is_food_item = fields.Boolean(string="Is Food Item")
