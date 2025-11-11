from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    global_discount = fields.Monetary("Global Discount")
    total_before_global_discount = fields.Monetary("Total Before Global Discount", currency_field="currency_id", compute="_compute_total_global_discount")
    total_global_discount = fields.Monetary("Total Global Discount", currency_field="currency_id", compute="_compute_total_global_discount")
    is_allocated_global_discount = fields.Boolean("Is Allocated Global Discount")

    def allocate_global_discount(self):
        self.validate_global_discount()

    def validate_global_discount(self):
        if self.global_discount:
            TOLERANCE = 0.1
            if abs(self.global_discount - self.total_global_discount) > TOLERANCE:
                raise ValidationError(_("Global discount amount must be equal to total global discount amount."))
        self.is_allocated_global_discount = True
                
    @api.depends("global_discount", "order_line.total_before_global_discount", "order_line.global_discount_amount")
    def _compute_total_global_discount(self):
        for order in self:
            order.total_before_global_discount = sum(order.order_line.mapped("total_before_global_discount"))
            order.total_global_discount = sum(order.order_line.mapped("global_discount_amount"))


    def button_confirm(self):
        self.validate_global_discount()
        super().button_confirm()

    @api.onchange('global_discount')
    def _onchange_global_discount(self):
        if self.global_discount:
            self.is_allocated_global_discount = False