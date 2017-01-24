from openerp import models,fields, api, exceptions


class descuento_report_invoice_line(models.Model):

    _inherit = 'account.invoice.line'

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
        if self.invoice_id.partner_id.category_id:
            if self.discount >= self.invoice_id.partner_id.category_id.max_discount:
                raise exceptions.ValidationError('A sobrepasado el limite de descuento de este cliente, el cual es un ' + str(
                    self.invoice_id.partner_id.category_id.max_discount) + "%")

class descuento_report_account_invoice(models.Model):

    _inherit = 'account.invoice'


    @api.depends('invoice_line_ids.price_unit','invoice_line_ids.quantity', 'invoice_line_ids.price_subtotal','invoice_line_ids.amount_discount', 'invoice_line_ids.invoice_line_tax_ids')
    def _comute_total_dicount_grabado(self):

        for invoice in self:
            total_g = total_d = 0.0

            for line in invoice.invoice_line_ids:

                if line.amount_discount > 0:
                    total_d += (line.price_unit-line.amount_discount) * line.quantity

                if line.invoice_line_tax_ids.amount > 0:
                    total_g += line.price_subtotal

            invoice.update({
                'total_amount_discount': total_d,
                'total_grabado': total_g
            })


    total_amount_discount = fields.Float(compute='_comute_total_dicount_grabado', string='Descuento', readonly=True, store=True)
    total_grabado = fields.Float(compute='_comute_total_dicount_grabado', string='Grabado', readonly=True, store=True)