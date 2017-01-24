from openerp import models,fields, api, exceptions



class descuento_report_order_line(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    @api.depends('discount','price_unit')
    def _compute_amount_discount(self):

        for line in self:
            if line.discount > 0:
                total = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            else:
                total = line.price_unit
            line.update({
                'amount_discount': total
            })


    amount_discount = fields.Float(compute='_compute_amount_discount', string='Precio con Descuento', readonly=True, store=True)

    @api.one
    @api.constrains('discount')
    def condiciones(self):
        if self.order_id.partner_id.category_id:
            if self.discount >= self.order_id.partner_id.category_id.max_discount:
                raise exceptions.ValidationError('A sobrepasado el limite de descuento de este cliente, el cual es un '+ str(self.order_id.partner_id.category_id.max_discount) +"%")

class descuento_report_sale_order(models.Model):

    _name = 'sale.order'
    _inherit = 'sale.order'


    @api.depends('order_line.price_unit','order_line.tax_id','order_line.product_uom_qty', 'order_line.price_subtotal','order_line.amount_discount')
    def _comute_total_dicount_grabado(self):

        for order in self:
            total_g = total_d = 0.0

            for line in order.order_line:

                if line.amount_discount > 0:
                    total_d += (line.price_unit-line.amount_discount) * line.product_uom_qty

                if line.tax_id.amount > 0:
                    total_g += line.price_subtotal

            order.update({
                'total_amount_discount': total_d,
                'total_grabado': total_g
            })


    total_amount_discount = fields.Float(compute='_comute_total_dicount_grabado', string='Descuento', readonly=True, store=True)
    total_grabado = fields.Float(compute='_comute_total_dicount_grabado', string='Grabado', readonly=True, store=True)