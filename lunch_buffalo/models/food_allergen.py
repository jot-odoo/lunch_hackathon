from odoo import models, fields

class FoodAllergen(models.Model):
    _name = 'food.allergen'
    _description = 'Food Allergen'

    name = fields.Char(required=True)