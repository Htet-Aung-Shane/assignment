from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    gross_unit_price = fields.Monetary(string='Gross Unit Price', digits='Product Price',
                                       help="The unit price before any discounts.", compute="_compute_gross_unit_price",readonly=False, store=True)
    total_before_global_discount = fields.Monetary(
        string='Total Before Global Discount', digits='Product Price', help="The total amount before applying the global discount.", compute="_compute_total_before_global_discount", store=True)
    global_discount_status = fields.Boolean(string='Global Discount Status', default=False,
                                            help="If checked, the global discount amount will be applied to this line.", readonly=False, compute='_compute_global_discount_status')
    global_discount_amount = fields.Monetary(
        string='Global Discount Amount', digits='Product Price', help="The global discount amount to be applied to this line.")
    net_amount = fields.Monetary(string='Net Amount', digits='Product Price',
                                 help="The net amount after applying the global discount.", compute="_compute_net_amount", store=True)

    @api.depends('product_id','product_id.standard_price')
    def _compute_gross_unit_price(self):
        for line in self:
            line.gross_unit_price = line.product_id.standard_price

    @api.depends('product_id','product_id.type')
    def _compute_global_discount_status(self):
        for line in self:
            if line.product_id.type == 'service':
                line.global_discount_status = False
            else:
                line.global_discount_status = True


    @api.depends('product_qty', 'gross_unit_price', 'global_discount_status')
    def _compute_total_before_global_discount(self):
        for line in self:
            if line.global_discount_status:
                line.total_before_global_discount = line.product_qty * line.gross_unit_price
            else:
                line.total_before_global_discount = 0.0


    @api.depends('total_before_global_discount', 'global_discount_amount')
    def _compute_net_amount(self):
        for line in self:
            line.net_amount = line.total_before_global_discount - line.global_discount_amount


    @api.model
    @api.onchange('gross_unit_price', 'global_discount_amount', 'product_qty')
    def _onchange_global_discount_amount(self):
        for line in self:
            discount_unit_price = line.global_discount_amount / line.product_qty if line.product_qty > 0 else 0.0
            line.price_unit = line.gross_unit_price - discount_unit_price