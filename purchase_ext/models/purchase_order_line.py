from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    gross_unit_price = fields.Float(string='Gross Unit Price', digits='Product Price')
    total_before_global_discount = fields.Float(string='Total Before Global Discount', digits='Product Price')
    global_discount_status = fields.Boolean(string='Global Discount Status', default=False)
    global_discount_amount = fields.Float(string='Global Discount Amount', digits='Product Price')
    net_amount = fields.Float(string='Net Amount', digits='Product Price')