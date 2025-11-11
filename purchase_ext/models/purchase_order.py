from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    global_discount = fields.Float("Global Discount")
    total_before_global_discount = fields.Float("Total Before Global Discount")
    total_global_discount = fields.Float("Total Global Discount")