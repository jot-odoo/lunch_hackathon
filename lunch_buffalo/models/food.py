from odoo import models, fields

class Food(models.Model):
    _inherit = 'product.product'
    _description = 'Food'
    
    description = fields.Text(string="Description")
    allergen_ids = fields.Many2many('food.allergen', string="Allergens")
    alternative_ids = fields.Many2many(
        'product.product',
        'product_food_alternative_rel',
        'product_id',
        'alternative_id',
        string="Alternative Foods"
    )
    image = fields.Image(string="Food Image", max_width=1920, max_height=1920)
