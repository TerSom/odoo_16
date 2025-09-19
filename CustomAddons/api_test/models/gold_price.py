from odoo import models, fields

class CurrentPrice(models.Model):
    _name = 'current.price'
    _description = 'Current Gold Price'

    mid_price = fields.Float('Mid Price')
    sell = fields.Float('Sell Price')
    buy = fields.Float('Buy Price')
    installment = fields.Float('Installment')
    updated_at = fields.Date('Updated At')
class HistoryPrice(models.Model):
    _name = 'history.price'
    _description = 'History Gold Price'

    sell = fields.Float('Sell Price')
    buy = fields.Float('Buy Price')
    installment = fields.Float('Installment')
    updated_at = fields.Date('Updated At')